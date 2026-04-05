# TOTP generation logic
import pyotp

def base_32(
    secret: str,
) -> str:
    secret = secret.replace(
        " ",
        ""
    ).upper()

    # base32 strings MUST be a multiple of 8 characters
    padding = len(
        secret
    ) % 8

    # Adds the missing "=" padding
    if padding:
        secret += "=" * (8 - padding)

    return secret


def gen_code (
        secret: str
) -> str:

    fixed_secret = base_32(
        secret
    )

    totp = pyotp.TOTP(
        fixed_secret
    )
    # Takes the 2fa secret and returns an otp (6 digit code)
    return totp.now()