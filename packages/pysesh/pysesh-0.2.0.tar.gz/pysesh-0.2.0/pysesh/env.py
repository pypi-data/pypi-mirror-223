from pysesh import os, console, color, DIRECTORY, col, cpr


def create_new_env(name):
    env_path = os.path.join(DIRECTORY, f"{name}.env")
    if os.path.exists(env_path):
        cpr(f"\n[bold {col['d']}][-][/bold {col['d']}] Environment '[bold {col['w']}]'{name}'[/bold {col['w']}] already exists.\n")
        return
    with open(env_path, 'w') as env_file:
        env_file.write("# Environment variables for session")
        cpr(f"\n[bold {col['s']}][+][/bold {col['s']}] Environment '[bold {col['w']}]'{name}'[/bold {col['w']}] created successfully.\n")


def list_envs():
    envs = [file[:-4] for file in os.listdir(DIRECTORY) if file.endswith('.env')]
    for env in envs:
        cpr(f"\n[bold {col['n']}] Available environments:[/bold {col['n']}]\n")
        cpr(f"[bold {col['s']}]  -[/bold {col['s']}] {env}\n")


def delete_env(name):
    env_path = os.path.join(DIRECTORY, f"{name}.env")
    if not os.path.exists(env_path):
        cpr(f"\n[bold {col['d']}][[/bold {col['d']}][bold {col['w']}]![/bold {col['w']}][bold {col['d']}]][/bold {col['d']}] Environment '[bold {col['w']}]'{name}'[/bold {col['w']}] does not exist.\n")
        return
    os.remove(env_path)
    cpr(f"\n[bold {col['s']}][-][/bold {col['s']}] Environment '[bold {col['w']}]'{name}'[/bold {col['w']}] deleted successfully.\n")


def associate_env_to_session(sessions, session_name, env_name):
    env_path = os.path.join(DIRECTORY, f"{env_name}.env")
    if not os.path.exists(env_path):
        cpr(f"\n[bold {col['d']}][[/bold {col['d']}][bold {col['w']}]![/bold {col['w']}][bold {col['d']}]][/bold {col['d']}] Environment '[bold {col['w']}]'{env_name}'[/bold {col['w']}] does not exist.\n")
        return
    if session_name not in sessions:
        sessions[session_name]['env_path'] = env_path
        cpr(f"\n[bold {col['s']}][+][/bold {col['s']}] Environment '[bold {col['w']}]'{env_name}'[/bold {col['w']}] associated to session '[bold {col['w']}]'{session_name}'[/bold {col['w']}] successfully.\n")
    else:
        cpr(f"\n[bold {col['d']}][[/bold {col['d']}][bold {col['w']}]![/bold {col['w']}][bold {col['d']}]][/bold {col['d']}] Session '[bold {col['w']}]'{session_name}'[/bold {col['w']}] does not exist.\n")

