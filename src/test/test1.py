from pathlib import Path
import typer

import mossel

def main():
    commands_conf = mossel.load_conf(Path("."))
    mossel.prompt()
    typer.echo(f"{commands_conf=}")

if __name__ == "__main__":
    typer.run(main)

