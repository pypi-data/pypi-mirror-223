import json

from aws_glue_interactive_sessions_kernel.glue_kernel_configs.ConfigRetriever import ConfigRetriever
from aws_glue_interactive_sessions_kernel.glue_kernel_utils.GlueSessionsConstants import \
    SAGEMAKER_STUDIO_NOTEBOOK_IDENTIFIERS, GLUE_PREFIX, GLUE_VERSION, REGION, SESSION_ID_PREFIX, SPARK_CONF, TAGS, \
    SESSION_TYPE, GLUE_JOB_TYPE, IAM_ROLE, GLUE_ROLE_ARN

import os
import subprocess


class SystemEnvConfigRetriever(ConfigRetriever):

    def __init__(self, request_origin=None):
        self.request_origin = request_origin

    def _retrieve_os_env_variable(self, key):
        if self.request_origin not in SAGEMAKER_STUDIO_NOTEBOOK_IDENTIFIERS:
            return os.environ.get(key)
        else:
            _, output = subprocess.getstatusoutput(f"echo ${key}")
            return os.getenv(key, output)

    def get_config_variable(self, config_name):
        # Special handling for these configs which are already used.
        # Accept both the old and new values to have a gradual migration.
        if config_name in [GLUE_VERSION, REGION, SPARK_CONF, SESSION_ID_PREFIX, GLUE_JOB_TYPE]:
            return self._retrieve_os_env_variable(config_name) \
                if self._retrieve_os_env_variable(config_name) is not None \
                else self._retrieve_os_env_variable(GLUE_PREFIX + config_name)
        if config_name == IAM_ROLE:
            return self._retrieve_os_env_variable(GLUE_PREFIX + IAM_ROLE) \
                if self._retrieve_os_env_variable(GLUE_PREFIX + IAM_ROLE) is not None \
                else self._retrieve_os_env_variable(GLUE_ROLE_ARN)
        if config_name == TAGS:
            return self._retrieve_tags_from_env_variable(GLUE_PREFIX + TAGS)
        return self._retrieve_os_env_variable(GLUE_PREFIX + config_name)

    def _retrieve_tags_from_env_variable(self, tags_key):
        tags = self._retrieve_os_env_variable(tags_key)
        if isinstance(tags, str):
            tags_dict = json.loads(tags)
            return tags_dict
        else:
            return tags
