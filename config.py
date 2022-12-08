from pathlib import Path
from dotenv import dotenv_values
from simple_logging import get_basic_logger


CREDENTIALS_DIRECTORY = Path.cwd() / "credentials"
secrets = dotenv_values(CREDENTIALS_DIRECTORY / ".env")

# Creates a logging object to use
log = get_basic_logger()
