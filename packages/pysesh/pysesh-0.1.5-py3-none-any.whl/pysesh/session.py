import inquirer
from pysesh import os, pickle, console, color, col, sys, inquirer, REPOSITORY, cpr

STATE_DIR = os.path.dirname(REPOSITORY)
if not os.path.exists(STATE_DIR):
    os.makedirs(STATE_DIR)


def load_sessions():
    try:
        with open(REPOSITORY, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}


def save_sessions(sessions):
    with open(REPOSITORY, 'wb') as f:
        pickle.dump(sessions, f)


def create_new_session(sessions, name):
    if name in sessions:
        cpr(f"\n[bold {col['d']}][-][/bold {col['d']}] Session '[bold {col['w']}]{name}[/bold {col['w']}]' already exists.\n")
        return
    sessions[name] = {'name': name, 'state': {}}
    cpr(f"\n[bold {col['s']}][+][/bold {col['s']}] Session '[bold {col['w']}]{name}[/bold {col['w']}]' created successfully.\n")


def list_sessions(sessions):
    for session in sessions:
        cpr(f"\n[bold {col['n']}] Available sessions:[/bold {col['n']}]\n")
        cpr(f"[bold {col['s']}]  -[/bold {col['s']}][bold {col['w']}] {session}[/bold {col['w']}]\n")


def delete_session(sessions, name):
    if name not in sessions:
        cpr(f"\n[bold {col['d']}][[/bold {col['d']}][bold {col['w']}]![/bold {col['w']}][bold {col['d']}]][/bold {col['d']}] Session '[bold {col['w']}]{name}[/bold {col['w']}]' does not exist.\n")
        return
    del sessions[name]
    cpr(f"\n[bold {col['s']}][-][/bold {col['s']}] Session '[bold {col['w']}]{name}[/bold {col['w']}]' deleted successfully.\n")


def load_session(sessions, name):
    if name not in sessions:
        cpr(f"\n[bold {col['d']}][[/bold {col['d']}][bold {col['w']}]![/bold {col['w']}][bold {col['d']}]][/bold {col['d']}] Session '[bold {col['w']}]{name}[/bold {col['w']}]' does not exist.\n")
        return

    current_session_state = sessions[name]['state']

    sys.ps1 = ''
    sys.ps2 = ''

    try:
        cpr(f"[bold {col['n']}]Now running in '[bold {col['w']}]{name}[/bold {col['w']}]', press Ctrl+C to save state and exit.[/bold {col['n']}]\n")
        while True:
            code_input = input()
            if code_input.strip().lower() == 'exit()':
                break
            exec(code_input, current_session_state)
    except KeyboardInterrupt:
        cpr(f"\n[bold {col['s']}][+][/bold {col['s']}][bold {col['l']}] Session state for '[bold {col['w']}]{name}[/bold {col['w']}]' has been saved.[/bold {col['l']}]\n")
    except Exception as e:
        cpr(f"\n[bold {col['d']}][[/bold {col['d']}][bold {col['w']}]![/bold {col['w']}][bold {col['d']}]][/bold {col['d']}] Session '[bold {col['w']}]{name}[/bold {col['w']}]' state has not been saved.\n")



def select_session(sessions):
    choices = list(sessions.keys())
    cpr('')
    questions = [
        inquirer.List('selected_session',
                      message="Select a session",
                      choices=choices,
                      )
    ]
    answers = inquirer.prompt(questions)
    return answers["selected_session"] if answers else None

