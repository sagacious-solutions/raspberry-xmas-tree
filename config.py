from pathlib import Path
from dotenv import dotenv_values

CREDENTIALS_DIRECTORY = Path.cwd() / "credentials"
secrets = dotenv_values(CREDENTIALS_DIRECTORY / ".env")
