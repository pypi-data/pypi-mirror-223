import os
import sys
from json import JSONDecodeError

from pydantic import ValidationError

from tons.config import ConfigNotFoundError
from tons.tonsdk.utils import setup_default_decimal_context
from tons.ui._background import BackgroundTaskManager
from tons.ui._utils import init_shared_object, setup_app
from tons.ui.interactive_cli._exceptions import EscButtonPressed
from tons.ui.interactive_cli._sets import EntrypointSet
from tons.ui.interactive_cli._utils import echo_error, echo_success


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    setup_default_decimal_context()

    try:
        context = init_shared_object()
        setup_app(context.config)

    except (FileNotFoundError, JSONDecodeError, ConfigNotFoundError, ValidationError, PermissionError) as e:
        echo_error(e)
        return

    if len(sys.argv) == 2 and sys.argv[1] == "--debug":
        context.debug_mode = True

    context.ton_daemon.start()

    context.background_task_manager = BackgroundTaskManager(context)
    context.background_task_manager.start()

    workdir_abspath = os.path.abspath(context.config.tons.workdir)
    echo_success(f"Current working directory: {workdir_abspath}")

    try:
        EntrypointSet(context).show()
    except (EscButtonPressed, KeyboardInterrupt):
        pass


if __name__ == '__main__':
    main()
