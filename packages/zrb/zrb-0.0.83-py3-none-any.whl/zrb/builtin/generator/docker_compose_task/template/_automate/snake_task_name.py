from zrb import DockerComposeTask, HTTPChecker, Env, EnvFile, runner
from zrb.builtin._group import project_group
import os

###############################################################################
# Constants
###############################################################################

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
RESOURCE_DIR = os.path.join(PROJECT_DIR, 'src', 'kebab-task-name')

###############################################################################
# Task Definitions
###############################################################################

snake_task_name = DockerComposeTask(
    name='kebab-task-name',
    description='human readable task name',
    group=project_group,
    cwd=RESOURCE_DIR,
    compose_cmd='composeCommand',
    compose_env_prefix='ENV_PREFIX',
    env_files=[
        EnvFile(
            env_file=os.path.join(RESOURCE_DIR, 'docker-compose.env'),
            prefix='ENV_PREFIX'
        )
    ],
    envs=[
        Env(
            name='HOST_PORT',
            os_name='ENV_PREFIX_HOST_PORT',
            default='httpPort'
        ),
    ],
    checkers=[
        HTTPChecker(
            name='check-kebab-task-name',
            port='{{env.HOST_PORT}}'
        )
    ]
)
runner.register(snake_task_name)
