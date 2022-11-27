from pathlib import Path
from dotenv import dotenv_values

CREDENTIALS_DIRECTORY = Path.cwd() / "credentials"
secrets = dotenv_values(CREDENTIALS_DIRECTORY / ".env")
https_key = CREDENTIALS_DIRECTORY / "cloudflare_cert.key"
https_cert = CREDENTIALS_DIRECTORY / "cloudflare_cert.pem"
