# presentation - cli, commands using typer

import json
import time
import typer
from rich.console import Console
from rich.live import Live
from rich.table import Table

from p2fa.core import security, storage, service

app = typer.Typer(help="p2fa - Private, encrypted 2FA vault")
console = Console()

def get_master_passwd(

) -> str:
    return typer.prompt(
        "Enter a master password: ",
        hide_input=True
    )

@app.command(name = "add")
def add_to_vault(
    service_name: str,
) -> None:
    secret: str = typer.prompt("Enter 2FA secret", hide_input=True)

    password: str = get_master_passwd()
    salt, encrypted_data = storage.load_p2fa()

    if not salt:
        console.print("[blue]No vault has been found.\nCreating a new one[/blue]")
        salt = security.make_salt()
        vault_data = {}

    else:
        try:
            decrypted_str: str = security.decrypt_password(
                encrypted_data,
                password,
                salt,
            )

            vault_data: dict = json.loads(decrypted_str)

        except Exception:
            console.print("[red]Access denied. Incorrect master password[/red]")
            raise typer.Exit(1)

    vault_data [
        service_name
    ] = secret

    new_json: str = json.dumps(
        vault_data
    )

    new_encrypted_data: bytes = security.encrypt_password(
        new_json,
        password,
        salt
    )

    storage.save_p2fa(
        salt,
        new_encrypted_data
    )

    console.print(f"[green]Successfully added {service_name} to your vault[/green]")

@app.command()
def get_p2fa(

) -> None:

    salt, encrypted_data = storage.load_p2fa()

    if not salt:
        console.print("[red] No vault has been found. Use p2fa add to create one [/red]")
        raise typer.Exit(1)

    password: str = get_master_passwd()

    try:
        decrypted_str: str = security.decrypt_password(
            encrypted_data,
            password,
            salt
        )

        vault_data: dict = json.loads(
            decrypted_str
        )
    except Exception:
        console.print("[red]Access denied. Incorrect master password[/red]")
        raise typer.Exit(1)

    with Live(gen_table(vault_data), refresh_per_second=5, console =  console) as live:
        try:
            while True:
                time.sleep(1)

                live.update(gen_table(vault_data))
        except KeyboardInterrupt:
            console.print("[red]Vault Locked[/red]")


def gen_table(
    vault_data: dict[str, str]
) -> Table:

    remaining = 30 - (int(time.time()) % 30)

    table = Table(
        title = "p2fa live vault",
        style = "cyan",
        show_footer = False,
    )

    table.add_column(
        "Service", # Header
        style = "magenta",
        justify = "right",
    )

    table.add_column(
        "Code", # Header
        style = "green",
        justify = "center",
        width = 10,
    )

    table.add_column(
        "Expires In", # Header
        style = "yellow",
        justify = "center",
    )

    for svc_name, secret in vault_data.items():
        code: str = service.gen_code(
            secret
        )
        time_colour = "red" if remaining <= 5 else "green"
        table.add_row(
            svc_name, # renderables
            code,
            f"[{time_colour}]{remaining}s[/{time_colour}]"
        )

    return table


if __name__ == "__main__":
    app()
