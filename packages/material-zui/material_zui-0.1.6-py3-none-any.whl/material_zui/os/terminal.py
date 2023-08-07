import os


def execute(command: str) -> int: return os.system(command)


def execute_with_terminal(command: str) -> int:
    '''
    Open terminal then execute command
    '''
    return os.system(f"gnome-terminal -e 'bash -c \"{command};bash\"'")
    # return os.system(f"gnome-terminal --command 'bash -c \"{command};bash\"'")
