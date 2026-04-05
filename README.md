# p2fa

A self-hosted, encrypted CLI tool for managing two factor authentication tokens. Built with Python, `uv`, `cryptography`, and `rich`.

---

## Overview

p2fa provides a secure way to store and retrieve your 2FA secrets locally. All data is encrypted at rest and only accessible via your master password, no cloud sync, no external transmission.

---

## Installation

Ensure you have `uv` installed, then navigate to the project root (the directory containing `pyproject.toml`) and run:

```bash
cd /path/to/p2fa
uv python install 3.13
uv pip install -e .
```

---

## Usage

| Action | Command |
|---|---|
| Add a service | `uv run p2fa add [service_name]` |
| View vault (live) | `uv run p2fa get-p2fa` |
| Reset vault | `rm ~/.p2fa_path.enc` |

### Adding a service

```bash
uv run p2fa add Google
```

You will be prompted to enter your 2FA secret and master password interactively. The secret is **never passed as a CLI argument**, so it won't appear in your shell history.

> **Note:** Your 2FA secret must be a valid Base32 string (e.g. `JBSWY3DPEHPK3PXP`). Copy it exactly, no spaces or special characters.

### Viewing your vault

```bash
uv run p2fa get-p2fa
```

Displays a live updating table of all your 2FA codes with a 30 second countdown timer. The timer turns red when under 5 seconds. Press `Ctrl+C` to lock the vault.

---

## Security Architecture

| Feature | Detail |
|---|---|
| **Master password** | Derived via Scrypt, never stored on disk |
| **Key derivation** | Scrypt with high memory and CPU cost, resistant to hardware acceleration attacks |
| **Encryption** | AES-256 via Fernet (CBC mode) with a 128-bit HMAC for authentication |
| **Secret input** | All sensitive input is entered interactively and hidden — never passed as CLI arguments |
| **File permissions** | Vault file is set to `chmod 600` — readable by owner only |
| **Storage** | Fully local, no cloud synchronisation or external data transmission |

---

## Troubleshooting

### `uv: command not found`

Install `uv` by following the instructions at [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

### `Error: Incorrect padding`

The 2FA secret you entered is not a valid Base32 string. Make sure you're copying it exactly from your authenticator app or service — no spaces, no special characters.

Reset the vault and try again with the correct secret:

```bash
rm ~/.p2fa_path.enc
uv run p2fa add myservice
```

### `Access denied. Incorrect master password`

You've entered the wrong master password. There is no password recovery — if the master password is lost, the vault cannot be decrypted.

**Reset vault (destructive):**

```bash
rm ~/.p2fa_path.enc
```

---

## Customisation

Add an alias to your `.bashrc` or `.zshrc` for faster access:

```bash
alias vault="uv run p2fa get-p2fa"
```

Restart your terminal, then use `vault` to open your codes directly.

---
