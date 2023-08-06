import json

from aws_glue_interactive_sessions_kernel.glue_kernel_configs.ConfigRetriever import ConfigRetriever

import botocore

from aws_glue_interactive_sessions_kernel.glue_kernel_utils.GlueSessionsConstants import GLUE_PREFIX, GLUE_VERSION, \
    REGION, SPARK_CONF, SESSION_ID_PREFIX, TAGS, GLUE_JOB_TYPE, IAM_ROLE, GLUE_ROLE_ARN


class AWSFileConfigRetriever(ConfigRetriever):
    def __init__(self, profile=None):
        self.profile = profile

    def get_profile(self):
        # Attempt to retrieve default profile if a profile is not already set
        if not self.profile and botocore.session.Session().full_config["profiles"].get("default"):
            self.profile = "default"
        return self.profile

    def _retrieve_from_aws_config(self, key):
        custom_profile_session = botocore.session.Session(profile=self.get_profile())
        return custom_profile_session.full_config["profiles"][self.get_profile()].get(key)

    def get_config_variable(self, config_name):
        # Special handling for these configs where the configs are already used by customers and cannot be changed
        if config_name in [GLUE_VERSION, REGION, SPARK_CONF, SESSION_ID_PREFIX, GLUE_JOB_TYPE]:
            return self._retrieve_from_aws_config(config_name) \
                if self._retrieve_from_aws_config(config_name) is not None \
                else self._retrieve_from_aws_config(GLUE_PREFIX + config_name)
        if config_name == IAM_ROLE:
            return self._retrieve_from_aws_config(GLUE_PREFIX + IAM_ROLE) \
                if self._retrieve_from_aws_config(GLUE_PREFIX + IAM_ROLE) is not None \
                else self._retrieve_from_aws_config(GLUE_ROLE_ARN)
        if config_name == TAGS:
            return self._retrieve_tags_from_aws_config(GLUE_PREFIX + TAGS)
        return self._retrieve_from_aws_config(GLUE_PREFIX + config_name)

    def _retrieve_tags_from_aws_config(self, tags_key):
        tags = self._retrieve_from_aws_config(tags_key)
        if isinstance(tags, str):
            tags_dict = json.loads(tags)
            return tags_dict
        else:
            return tags

