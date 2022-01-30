import os
import os.path
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


def main(name: str):
    load_conf(Path("."))
    prompt()
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
