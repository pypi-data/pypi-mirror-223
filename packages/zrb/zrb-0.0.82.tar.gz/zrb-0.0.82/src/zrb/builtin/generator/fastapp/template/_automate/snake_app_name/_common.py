from typing import Any
from zrb import (
    BoolInput, ChoiceInput, StrInput, Env, HTTPChecker, PortChecker
)
import jsons
import os

###############################################################################
# Constants
###############################################################################

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
RESOURCE_DIR = os.path.join(PROJECT_DIR, 'src', 'kebab-app-name')
DEPLOYMENT_DIR = os.path.join(RESOURCE_DIR, 'deployment')
DEPLOYMENT_TEMPLATE_ENV_FILE_NAME = os.path.join(
    DEPLOYMENT_DIR, 'template.env'
)
APP_DIR = os.path.join(RESOURCE_DIR, 'src')
APP_FRONTEND_DIR = os.path.join(APP_DIR, 'frontend')
APP_FRONTEND_BUILD_DIR = os.path.join(APP_FRONTEND_DIR, 'build')
APP_TEMPLATE_ENV_FILE_NAME = os.path.join(APP_DIR, 'template.env')
MODULE_CONFIG_PATH = os.path.join(CURRENT_DIR, 'config', 'modules.json')
with open(MODULE_CONFIG_PATH) as file:
    MODULE_JSON_STR = file.read()
MODULES = jsons.loads(MODULE_JSON_STR)

###############################################################################
# Functions
###############################################################################


def skip_local_microservices_execution(*args: Any, **kwargs: Any) -> bool:
    if not kwargs.get('local_snake_app_name', True):
        return True
    return kwargs.get('snake_app_name_run_mode', 'monolith') != 'microservices'


###############################################################################
# Checker Task Definitions
###############################################################################

rabbitmq_management_checker = HTTPChecker(
    name='check-rabbitmq-management',
    port='{{env.get("RABBITMQ_MANAGEMENT_HOST_PORT", "15672")}}',
    is_https='{{input.snake_app_name_https}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "rabbitmq"}}'
)

rabbitmq_checker = PortChecker(
    name='check-rabbitmq',
    port='{{env.get("RABBITMQ_HOST_PORT", "5672")}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "rabbitmq"}}'
)

redpanda_console_checker = HTTPChecker(
    name='check-redpanda-console',
    method='GET',
    port='{{env.get("REDPANDA_CONSOLE_HOST_PORT", "9000")}}',
    is_https='{{input.snake_app_name_https}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "kafka"}}'
)

kafka_plaintext_checker = PortChecker(
    name='check-kafka-plaintext',
    port='{{env.get("KAFKA_INTERNAL_HOST_PORT", "29092")}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "kafka"}}'
)

kafka_outside_checker = PortChecker(
    name='check-kafka-outside',
    port='{{env.get("KAFKA_EXTERNAL_HOST_PORT", "9092")}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "kafka"}}'
)

pandaproxy_plaintext_checker = PortChecker(
    name='check-pandaproxy-plaintext',
    port='{{env.get("PANDAPROXY_INTERNAL_HOST_PORT", "29092")}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "kafka"}}'
)

pandaproxy_outside_checker = PortChecker(
    name='check-pandaproxy-outside',
    port='{{env.get("PANDAPROXY_EXTERNAL_HOST_PORT", "9092")}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "kafka"}}'
)

app_container_checker = HTTPChecker(
    name='check-kebab-app-name-container',
    host='{{input.snake_app_name_host}}',
    url='/readiness',
    port='{{env.get("HOST_PORT", "appHttpPort")}}',
    is_https='{{input.snake_app_name_https}}'
)

app_local_checker = HTTPChecker(
    name='check-kebab-app-name',
    host='{{input.snake_app_name_host}}',
    url='/readiness',
    port='{{env.APP_PORT}}',
    is_https='{{input.snake_app_name_https}}',
    skip_execution=skip_local_microservices_execution
)

###############################################################################
# Input Definitions
###############################################################################

enable_monitoring_input = BoolInput(
    name='enable-kebab-app-name-monitoring',
    description='Enable "kebab-app-name" monitoring',
    prompt='Enable "kebab-app-name" monitoring?',
    default=False
)

local_input = BoolInput(
    name='local-kebab-app-name',
    description='Use "kebab-app-name" on local machine',
    prompt='Use "kebab-app-name" on local machine?',
    default=True
)

run_mode_input = ChoiceInput(
    name='kebab-app-name-run-mode',
    description='"kebab-app-name" run mode (monolith/microservices)',
    prompt='Run "kebab-app-name" as a monolith or microservices?',
    choices=['monolith', 'microservices'],
    default='monolith'
)

https_input = BoolInput(
    name='kebab-app-name-https',
    description='Whether "kebab-app-name" run on HTTPS',
    prompt='Is "kebab-app-name" run on HTTPS?',
    default=False
)

host_input = StrInput(
    name='kebab-app-name-host',
    description='Hostname of "kebab-app-name"',
    prompt='Hostname of "kebab-app-name"',
    default='localhost'
)

###############################################################################
# Env fDefinitions
###############################################################################

local_app_port_env = Env(
    name='APP_PORT',
    os_name='ENV_PREFIX_APP_PORT',
    default='appHttpPort'
)

local_app_broker_type_env = Env(
    name='APP_BROKER_TYPE',
    os_name='ENV_PREFIX_APP_BROKER_TYPE',
    default='rabbitmq'
)

app_enable_otel_env = Env(
    name='APP_ENABLE_OTEL',
    default='{{ "1" if input.enable_snake_app_name_monitoring else "0" }}'
)
