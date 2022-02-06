import os
import os.path
from xmlrpc.client import boolean
import typer
import toml 
from pathlib import *
from typing import *

def load_conf(base_dir: Path, up_levels: int = 0) -> dict:
    # Suche vom aktuellen Directory aus nach oben.
    # In jedem dieser Verzeichnisse kann es ein Unterverzeichnis .mossel geben.
    # Im .mossel Verzeichnis suche nach commands.toml
    base_dir = base_dir.resolve()
    commands_files: list[Path] = []
    for level, path in enumerate([base_dir] + list(base_dir.parents)):
        commands_toml_path = path / ".mossel" / "commands.toml"
        if commands_toml_path.is_file():
            commands_files.append(commands_toml_path)
        if level >= up_levels: 
            break
    commands_conf = toml.load(commands_files)
    return commands_conf

def prompt():
    typer.echo("\U0001F41A", nl="")

def i_replace(text, env):
    match text:
        case Path(p):
            return Path(i_replace(str(p)))
        case str(s):
            if not "{" in s:
                return s
            out = ""
            varname = ""
            in_var = False
            for ch in s:
                if in_var:
                    if ch == "}":
                        in_var = False
                        out += env.get(varname, "")
                    else:
                        varname += ch
                else:
                    if ch == "{":
                        in_var = True
                        varname = ""
                    else:
                        out += ch
            return out
        case _:
            print("Error")

class Shell:

    builtins = ["dir", "cd", "set", "echo"]
    env: dict[str, str]
    cwd: Path

    def __init__(self, env=None, cwd: Optional[Path] = None):
        if env is None:
            env = os.environ.copy()
        self.env = env
        self.cwd = (cwd or Path(os.getcwd())).resolve()

    def parse_and_execute(self, command_line: str|list[str]) -> boolean:
        command: str
        args: list[str]
        if isinstance(command_line, str):
            args = self.split_command_line(command_line)
            command = args.pop(0)
        else:
            args = command_line[1:]
            command = command_line[0]
        command = self.replace_vars(command)
        args = [self.replace_vars(arg) for arg in args]

        print(f"{command=} {args=}")

        if command == "exit":
            return False
        if command in self.builtins:
            f = getattr(self, "handle_" + command)
            f(args)
        else:
            self.fail(f"Unknown command: {command}")
        return True
        
    def repl(self):
        while True:
            self.prompt()
            command_line = input()
            if not self.parse_and_execute(command_line):
                break

    def replace_vars(self, input):
        env = self.env
        match input:
            case str(s):
                return i_replace(s, env)
            case Path(p):
                return i_replace(p, env)
            case list(L):
                return [i_replace(s, env) for s in L]
            case _:
                self.fail("Internal error")
                return ""

    def split_command_line(self, command_line):
        return command_line.strip().split()

    def prompt(self):
        prompt()
        typer.echo(f"{self.cwd}\u276f")

    def fail(self, message: str):
        typer.echo("ERROR: " + message)

    def handle_dir(self, args):
        options = []
        directories: list[Path] = []
        if not args:
            args = ["."]
        for arg in args:
            match arg:
                case str(s):
                    directories.append(Path(s))
                case Path(p):
                    directories.append(p)
                case list(L):
                    directories += L
                case _:
                    self.fail(f"dir rgument must be str, Path or list, but found {repr(arg)}")
                    return
        for d in directories:
            typer.echo(f"Contents of {d}:")
            for child in d.iterdir():
                typer.echo(child)

    def handle_set(self, args):
        if len(args) != 2:
            self.fail("Syntax error")
            return
        [name, value] = args
        self.env[name] = value

    def handle_cd(self, args):
        if len(args) != 1:
            self.fail("Syntax error")
            return
        try:
            cwd = (self.cwd / args[0]).resolve()
            os.chdir(cwd)
            self.cwd = cwd
        except OSError as e:
            self.fail(f"cd failed: {e}")

    def handle_echo(self, args):
        separator = " "
        for i, arg in enumerate(args):
            if i > 0:
                typer.echo(separator, nl=False)
            match arg:
                case Path(p):
                    typer.echo(p, nl=False)
                case str(s):
                    typer.echo(s, nl=False)
                case list(L):
                    typer.echo("[", nl=False)
                    self.echo(L)
                    typer.echo("]", nl=True)
                case _:
                    self.fail("Internal Error")
        typer.echo()


def main(name: str):
    load_conf(Path("."))
    prompt()
    typer.echo(f"Hello {name}")
    shell = Shell()
    shell.repl()


if __name__ == "__main__":
    typer.run(main)
