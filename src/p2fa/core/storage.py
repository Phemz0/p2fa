# Reading / writing the encrypted JSON

import os
from pathlib import Path

# /home/user/.p2fa_vault.enc
secure_path = Path.home() / ".p2fa_path.enc"

def save_p2fa(
        salt: bytes,
        encrypted_password: bytes,
) -> None:

    with open (
        secure_path,
        "wb"
    ) as f:

        f.write(salt)
        f.write(encrypted_password)

    # owner only permissions
    os.chmod(secure_path, 0o600)

    def load_p2fa(

    ) -> tuple[bytes, bytes]:

        if not secure_path.exists():
            return b"", b""

        with open(
            secure_path,
            "rb"
        ) as f: # noqa

            salt = f.read( # noqa
                16
            )

            password = f.read()

        return (
            salt,
            password
        )
