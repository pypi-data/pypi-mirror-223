import sys
import os
from pysesh import cpr, col, args, parser, DIRECTORY
from pysesh.session import load_sessions, save_sessions, select_session, load_session, create_new_session, list_sessions, delete_session
from pysesh.env import create_new_env, list_envs, delete_env, associate_env_to_session

if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)


def ask(question: str, default: str = 'Y') -> bool:

    if default not in ['Y', 'N']:
        raise ValueError("Default must be either 'Y' or 'N'.")

    if default == 'Y':
        question += ' [Y/n] '
    else:
        question += ' [y/N] '

    while True:
        answer = input(question).strip().lower()
        if answer == '':
            return True if default == 'Y' else False
        elif answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            return False
        else:
            cpr(f"[bold {col['d']}][-][/bold {col['d']}] Invalid answer. '[{col['w']}]y[/{col['w']}]' or '[{col['w']}]n[/{col['w']}]' expected.")



def main():
    sessions = load_sessions()
    if not args.command:
        if not sessions:
            cpr(f"\n[bold {col['w']}][!][/bold {col['w']}] No sessions exist. Please run 'pysesh new [name]' to create one.\n")
            return
        session_to_load = select_session(sessions)
        if session_to_load:
            load_session(sessions, session_to_load)
    elif args.command == 'new':
        create_new_session(sessions, args.name)
    elif args.command == 'load':
        cpr(f"\n[bold {col['s']}][+][/bold {col['s']}] Session '[{col['w']}]{name}[/{col['w']}]' loaded!\n")
        load_session(sessions, args.name)
    elif args.command == 'list':
        list_sessions(sessions)
    elif args.command == 'delete':
        delete_session(sessions, args.name)
    elif args.command == 'env-create':
        create_new_env(args.name)  # You need to define this function
    elif args.command == 'env-list':
        list_envs()  # You need to define this function
    elif args.command == 'env-delete':
        delete_env(args.name)  # You need to define this function
    elif args.command == 'env-associate':
        associate_env_to_session(args.session, args.env)  # You need to define this function
    else:
        cpr(f"\n[bold {col['d']}][-][/bold {col['d']}] Invalid command '[{col['w']}]{args.command}[/{col['w']}]'.\n")
        parser.print_help()
        sys.exit(1)

    save_sessions(sessions)


if __name__ == "__main__":
    main()
