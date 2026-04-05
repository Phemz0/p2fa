# presentation - cli, commands using typer

import json
from logging import exception

import typer
from rich.console import Console
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
    secret: str
) -> None:

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

            vault_data: dict = json.loads(
                decrypted_str
            )

        except exception:
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

) -> str:

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

    table = Table(
        title = "2FA Codes",
        style = "cyan"
    )

    table.add_column(
        "Service", # header
        style = "magenta",
        justify = "right"
    )

    table.add_column(
        "Code", # header
        style = "green",
        justify = "center",
        width = 10
    )

    for svc_name, secret in vault_data.items():
        code = service.gen_code(
            secret
        )
        table.add_row(
            svc_name,
            code
        )

    console.print(
        table
    )


if __name__ == "__main__":
    app()
