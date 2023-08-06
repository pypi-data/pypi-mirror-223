# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
from urllib.parse import urlparse

from contrast import AGENT_CURR_WORKING_DIR

from contrast.agent.exclusions import Exclusions, TsExclusion, ExclusionType
from contrast.agent.framework import Framework, Server
from contrast.agent.protect.mixins.REP_settings import SettingsREPMixin
from contrast.agent.reaction_processor import ReactionProcessor
from contrast.agent.protect.rule import ProtectionRule
from contrast.configuration import AgentConfig, SamplingLockConfig
from contrast.utils.decorators import cached_property
from contrast.utils.loggers.logger import reset_agent_logger
from contrast.utils.singleton import Singleton
from contrast.utils.string_utils import truncate
from contrast.utils.timer import now_ms
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

ASSESS_STACKTRACES = "assess.stacktraces"


class ServerFeatures:
    def __init__(self, features):
        self.features = features or {}

    @cached_property
    def log_file(self):
        return self.features.get("features", {}).get("logFile", "")

    @cached_property
    def log_level(self):
        return self.features.get("features", {}).get("logLevel", "")

    @cached_property
    def assess_enabled(self):
        return (
            self.features.get("features", {})
            .get("assessment", {})
            .get("enabled", False)
        )

    @cached_property
    def protect_enabled(self):
        return self.features.get("features", {}).get("defend", {}).get("enabled", False)


class ApplicationSettings:
    def __init__(self, settings_json=None):
        self._raw_settings = settings_json or {}

    @cached_property
    def disabled_assess_rules(self):
        return (
            self._raw_settings.get("settings", {})
            .get("assessment", {})
            .get("disabledRules", [])
        )

    @cached_property
    def protection_rules(self):
        return [
            ProtectRule(r)
            for r in self._raw_settings.get("settings", {})
            .get("defend", {})
            .get("protectionRules", [])
        ]

    @cached_property
    def session_id(self):
        return (
            self._raw_settings.get("settings", {})
            .get("assessment", {})
            .get("session_id", None)
        )

    @cached_property
    def sensitive_data_masking_policy(self):
        return self._raw_settings.get("settings", {}).get(
            "sensitive_data_masking_policy"
        )

    @cached_property
    def exclusions(self):
        """
        Build and return a plain list of TsExclusions based on raw application settings.
        TsExclusions represent the exclusions more or less exactly as they were given to
        us by teamserver.

        The list returned by this property will be converted into our own Exclusions
        class later, which is more useful when processing exclusion rules.
        """
        ts_exclusions = self._raw_settings.get("settings", {}).get("exceptions")
        if ts_exclusions is None:
            return None

        exclusions = []

        for exclusion in ts_exclusions.get("urlExceptions", []):
            exclusions.append(
                TsExclusion(
                    ExclusionType.URL_EXCLUSION_TYPE,
                    exclusion.get("name", ""),
                    exclusion.get("modes", []),
                    exclusion.get("matchStrategy", ""),
                    exclusion.get("protectionRules", []),
                    exclusion.get("assessmentRules", []),
                    exclusion.get("urls", []),
                )
            )

        for exclusion in ts_exclusions.get("inputExceptions", []):
            exclusions.append(
                TsExclusion(
                    ExclusionType.INPUT_EXCLUSION_TYPE,
                    exclusion.get("name", ""),
                    exclusion.get("modes", []),
                    exclusion.get("matchStrategy", ""),
                    exclusion.get("protectionRules", []),
                    exclusion.get("assessmentRules", []),
                    exclusion.get("urls", []),
                    exclusion.get("inputType", ""),
                    exclusion.get("inputName", ""),
                )
            )

        return exclusions

    # note: there are more fields on ApplicationSettings that we currently don't use


class ProtectRule:
    def __init__(self, protect_rule_json):
        self._raw_rule = protect_rule_json or {}

    @cached_property
    def id(self):
        return self._raw_rule.get("id", "")

    @cached_property
    def mode(self):
        raw_mode = self._raw_rule.get("mode", "OFF")
        raw_block_at_entry = self._raw_rule.get("blockAtEntry", False)
        return {
            "MONITORING": ProtectionRule.MONITOR,
            "BLOCKING": (
                ProtectionRule.BLOCK_AT_PERIMETER
                if raw_block_at_entry
                else ProtectionRule.BLOCK
            ),
            "OFF": ProtectionRule.OFF,
        }[raw_mode]


class Settings(Singleton, SettingsREPMixin):
    def init(self, app_name=None, framework_name=None):
        """
        Agent settings for the entire lifetime of the agent.

        Singletons should override init, not __init__.
        """
        self.config = None
        self.config_features = {}
        self.exclusions = None
        self.last_server_update_time_ms = 0
        self.last_app_update_time_ms = 0
        self.heartbeat = None
        self.server_settings_poll = None
        self.framework = Framework(framework_name)
        self.server = Server()
        self.sys_module_count = 0

        # Server
        self.server_name = None
        self.server_path = None
        self.server_type = None

        self.exclusion_matchers = []

        # Rules
        self.protect_rules = dict()

        # circular import
        from contrast.agent.assess.rules.response.autocomplete_missing_rule import (
            AutocompleteMissingRule,
        )
        from contrast.agent.assess.rules.response.cache_controls_rule import (
            CacheControlsRule,
        )
        from contrast.agent.assess.rules.response.clickjacking_rule import (
            ClickjackingRule,
        )

        from contrast.agent.assess.rules.response.x_content_type_rule import (
            XContentTypeRule,
        )

        from contrast.agent.assess.rules.response.csp_header_missing_rule import (
            CspHeaderMissingRule,
        )

        from contrast.agent.assess.rules.response.x_xss_protection_disabled_rule import (
            XXssProtectionDisabledRule,
        )

        from contrast.agent.assess.rules.response.hsts_header_rule import HstsHeaderRule

        from contrast.agent.assess.rules.response.csp_header_insecure_rule import (
            CspHeaderInsecureRule,
        )

        from contrast.agent.assess.rules.response.parameter_pollution_rule import (
            ParameterPollutionRule,
        )

        self.assess_response_rules = [
            AutocompleteMissingRule(),
            CacheControlsRule(),
            ClickjackingRule(),
            XContentTypeRule(),
            CspHeaderMissingRule(),
            XXssProtectionDisabledRule(),
            HstsHeaderRule(),
            CspHeaderInsecureRule(),
            ParameterPollutionRule(),
        ]

        # Initialize config
        self.config = AgentConfig()

        self.direct_teamserver_server_features = None
        self.direct_ts_app_settings = ApplicationSettings()

        self.disabled_assess_rules = set(
            self.config.get("assess.rules.disabled_rules", [])
        )

        # Initialize application metadata
        self.app_name = self.get_app_name(app_name)

        self.agent_runtime_window = now_ms()

        logger.info("Contrast Agent finished loading settings.")

    def _is_defend_enabled_in_server_features(self):
        return bool(
            self.direct_teamserver_server_features
            and self.direct_teamserver_server_features.protect_enabled
        )

    @cached_property
    def is_proxy_enabled(self):
        return self.config.get("api.proxy.enable")

    @cached_property
    def proxy_url(self):
        return self.config.get("api.proxy.url")

    @cached_property
    def proxy_scheme(self):
        scheme = urlparse(self.proxy_url).scheme or "http"
        return scheme

    @cached_property
    def is_cert_verification_enabled(self):
        return self.config.get("api.certificate.enable")

    @cached_property
    def ignore_cert_errors(self):
        return self.config.get("api.certificate.ignore_cert_errors")

    @cached_property
    def ca_file(self):
        return self.config.get("api.certificate.ca_file")

    @cached_property
    def client_cert_file(self):
        return self.config.get("api.certificate.cert_file")

    @cached_property
    def client_private_key(self):
        return self.config.get("api.certificate.key_file")

    @cached_property
    def api_service_key(self):
        return self.config.get("api.service_key")

    @cached_property
    def api_url(self):
        """Normalizes the URL to remove any whitespace or trailing slash"""
        return self.config.get("api.url").strip().rstrip("/")

    @cached_property
    def api_key(self):
        return self.config.get("api.api_key")

    @cached_property
    def api_user_name(self):
        return self.config.get("api.user_name")

    def is_agent_config_enabled(self):
        if self.config is None:
            return True

        return self.config.get("enable", True)

    @cached_property
    def is_rewriter_enabled(self):
        return self.config.get("agent.python.rewrite")

    @cached_property
    def is_policy_rewriter_enabled(self):
        return self.is_rewriter_enabled and not self.config.get(
            "agent.python.disable_policy_rewrites"
        )

    @cached_property
    def is_profiler_enabled(self):
        return self.config.get("agent.python.enable_profiler")

    @cached_property
    def max_sources(self):
        return self.config.get("assess.max_context_source_events")

    @cached_property
    def max_propagation(self):
        return self.config.get("assess.max_propagation_events")

    @cached_property
    def max_vulnerability_count(self):
        """Max number of vulnerabilities per rule type to report for one
        agent run `time_limit_threshold` time period"""
        return self.config.get("assess.max_rule_reported")

    @cached_property
    def agent_runtime_threshold(self):
        return self.config.get("assess.time_limit_threshold")

    @cached_property
    def app_path(self):
        return self.config.get("application.path")

    @cached_property
    def app_version(self):
        return self.config.get("application.version")

    @property
    def pid(self):
        """
        pid is used in our CMDi protect rule.

        pid must be unique for each worker process of an app.
        :return: int current process id
        """
        return os.getpid()

    def get_app_name(self, app_name):
        if self.config.get("application.name"):
            return self.config.get("application.name")

        return app_name if app_name else "root"

    def establish_heartbeat(self):
        """
        Initialize Heartbeat between Agent and TS if it has not been already initialized.
        """
        if self.heartbeat is None:
            # Circular import
            from contrast.agent.heartbeat_thread import HeartbeatThread

            self.heartbeat = HeartbeatThread()
            self.heartbeat.start()

    def establish_server_settings_poll(self):
        """
        Initialize Server Settings poll between Agent and TS if it has not been already initialized.
        """
        if self.server_settings_poll is None:
            # Circular import
            from contrast.agent.server_settings_poll import ServerSettingsPoll

            self.server_settings_poll = ServerSettingsPoll()
            self.server_settings_poll.start()

    def apply_ts_feature_settings(self, response_body):
        self.direct_teamserver_server_features = ServerFeatures(response_body)

        if (
            self.direct_teamserver_server_features.features.get("features", {})
            .get("assessment", {})
            .get("sampling")
        ):
            self.update_sampling()

        self.update_logger_from_features()

        self.log_server_features(self.direct_teamserver_server_features)

        self.set_protect_rules()

        self.last_server_update_time_ms = now_ms()

    def process_ts_reactions(self, response_body):
        # App startup/activity wrap reactions in a settings dict whereas
        # Server startup/activity has it at the top level response dict
        reactions = response_body.get("settings", {}).get("reactions", None)

        if not reactions:
            reactions = response_body.get("reactions", None)

        if not reactions:
            return

        ReactionProcessor.process(reactions, self)

    def log_server_features(self, server_features):
        """
        Record server features received from teamserver
        """
        logger.debug(
            "Received updated server features logFile=%s logLevel=%s Protect=%s Assess=%s",
            server_features.log_file,
            server_features.log_level,
            server_features.protect_enabled,
            server_features.assess_enabled,
        )

    @property
    def code_exclusion_matchers(self):
        return [x for x in self.exclusion_matchers if x.is_code]

    def load_exclusions_from_server(self, exclusions):
        if exclusions:
            self.exclusions = Exclusions(exclusions)

    def evaluate_exclusions(self, context, path):
        if self.exclusions:
            if self.exclusions.evaluate_url_exclusions(context, path):
                # Stop analyzing this endpoint since the URL exclusion applies
                return True

            if self.exclusions.input_exclusions:
                self.exclusions.set_input_exclusions_by_url(context, path)

        return False

    def apply_ts_app_settings(self, response_json):
        self.direct_ts_app_settings = ApplicationSettings(response_json)
        if self.direct_ts_app_settings.exclusions:
            self.load_exclusions_from_server(self.direct_ts_app_settings.exclusions)

        # This is the only place session_id is set by TS.
        # If session id is set in the config, that value will be echoed back by TS
        if self.direct_ts_app_settings.session_id:
            self.config.session_id = self.direct_ts_app_settings.session_id

    def update_logger_from_features(self):
        if self.direct_teamserver_server_features is not None:
            logger_reset = reset_agent_logger(
                self.direct_teamserver_server_features.log_file,
                self.direct_teamserver_server_features.log_level,
            )
        else:
            logger_reset = False

        if logger_reset:
            self.config.log_config()

    def is_inventory_enabled(self):
        """
        inventory.enable = false: Disables both route coverage and library analysis and reporting
        """
        return self.config.get("inventory.enable", True)

    def is_analyze_libs_enabled(self):
        """
        inventory.analyze_libraries = false: Disables only library analysis/reporting
        """
        return (
            self.config is not None
            and self.config.get("inventory.analyze_libraries", True)
            and self.is_inventory_enabled()
        )

    def is_assess_enabled(self):
        """
        We do not allow assess and defend to be on at the same time. As defend
        is arguably the more important of the two, it will take precedence

        The agent config may enable assess even if it is turned off in TS. This
        allows unlicensed apps to send findings to TS, where they will appear
        as obfuscated results.
        """

        # https://contrast.atlassian.net/browse/PROD-530
        if self.config is None:
            return False

        assess_enabled = self.config.get("assess.enable", None)
        if assess_enabled is not None:
            return assess_enabled

        return (
            self.direct_teamserver_server_features
            and self.direct_teamserver_server_features.assess_enabled
        )

    def is_protect_enabled(self):
        """
        Protect is enabled only if both configuration and server features enable it.
        """
        if self.config is None:
            return False
        config_protect_enabled = self.config.get("protect.enable", None)
        if config_protect_enabled is not None:
            return config_protect_enabled

        return self._is_defend_enabled_in_server_features()

    def set_protect_rules(self):
        if not self._is_defend_enabled_in_server_features():
            self.protect_rules = dict()
            return

        from contrast.agent.protect.rule.rules_builder import build_protect_rules

        self.protect_rules = build_protect_rules()

    def get_server_name(self):
        """
        Hostname of the server

        Default is socket.gethostname() or localhost
        """
        if self.server_name is None:
            self.server_name = self.config.get("server.name")

        return self.server_name

    def get_server_path(self):
        """
        Working Directory of the server

        Default is root
        """
        if self.server_path is None:
            self.server_path = self.config.get("server.path") or truncate(
                AGENT_CURR_WORKING_DIR
            )

        return self.server_path

    def get_server_type(self):
        """
        Web Framework of the Application either defined in common config or via discovery.
        """
        if self.server_type is None:
            self.server_type = (
                self.config.get("server.type") or self.framework.name_lower
            )

        return self.server_type

    @property
    def response_scanning_enabled(self):
        return self.is_assess_enabled() and self.config.get(
            "assess.enable_scan_response"
        )

    def is_assess_rule_disabled(self, rule_id):
        """
        Rules disabled in config override all disabled rules from TS per common config
        """
        app_settings = self.direct_ts_app_settings

        return (
            rule_id in self.disabled_assess_rules
            if self.disabled_assess_rules
            else app_settings and rule_id in app_settings.disabled_assess_rules
        )

    def enabled_response_rules(self):
        return [
            rule
            for rule in self.assess_response_rules
            if not self.is_assess_rule_disabled(rule.name)
        ]

    def is_collect_stacktraces_all(self):
        return self.config is not None and self.config.get(ASSESS_STACKTRACES) == "ALL"

    def is_collect_stacktraces_some(self):
        return self.config is not None and self.config.get(ASSESS_STACKTRACES) == "SOME"

    def is_collect_stacktraces_none(self):
        return self.config is not None and self.config.get(ASSESS_STACKTRACES) == "NONE"

    def build_proxy_url(self):
        if self.proxy_url:
            return {self.proxy_scheme: self.proxy_url}

        return {}

    def update_sampling(self):
        server_sampling = (
            self.direct_teamserver_server_features.features.get("features")
            .get("assessment")
            .get("sampling")
        )

        sampling_lock_config = SamplingLockConfig()

        if not sampling_lock_config.lock_enable:
            self.config.put("assess.sampling.enable", server_sampling.get("enable"))

        if not sampling_lock_config.lock_baseline:
            self.config.put("assess.sampling.baseline", server_sampling.get("baseline"))

        if not sampling_lock_config.lock_frequency:
            self.config.put(
                "assess.sampling.request_frequency", server_sampling.get("frequency")
            )

        if not sampling_lock_config.lock_window:
            self.config.put("assess.sampling.window_ms", server_sampling.get("window"))

        logger.debug(
            "Updated sampling setting with TeamServer sampling settings: %s",
            server_sampling,
        )
