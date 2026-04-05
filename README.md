# p2fa

A self-hosted, encrypted CLI tool for managing two-factor authentication tokens. Built with Python, `uv`, `cryptography`, and `rich`.

---

## Overview

p2fa provides a secure way to store and retrieve your 2FA secrets locally. All data is encrypted at rest and only accessible via your master password - no cloud sync, no external transmission.

---

## Installation

The `p2fa` command must be registered with your system before use. Navigate to the project root (the directory containing `pyproject.toml`) and run:

```bash
cd /path/to/p2fa
uv pip install -e .
```

---

## Usage

| Action | Command |
|---|---|
| Add a service | `uv run p2fa add [service_name] [secret_token]` |
| View vault (live) | `uv run p2fa get` |
| Reset vault | `rm ~/.p2fa_path.enc` |

### Example

```bash
uv run p2fa add Google JBSWY3DPEHPK3PXP
```

---

## Security Architecture

| Feature | Detail |
|---|---|
| **Master password** | Derived via Scrypt, never stored on disk |
| **Key derivation** | Scrypt with high memory and CPU cost, resistant hardware acceleration attacks |
| **Encryption** | AES-256 via Fernet (CBC mode) with a 128-bit HMAC for authentication |
| **Storage** | Fully local, no cloud synchronisation or external data transmission |

---

## Troubleshooting

### `Error: Failed to spawn (os error 2)`

This occurs when the terminal cannot locate the `p2fa` executable, typically after moving the project directory or running commands from the wrong folder.

**Fix:** Return to the project root and re-link:

```bash
cd /path/to/p2fa
uv pip install -e .
```

---

## Customisation

Add an alias to your `.bashrc` or `.zshrc` for faster access:

```bash
alias p2fa="uv run p2fa"
```

Restart your terminal, then use `p2fa get` directly.

---
