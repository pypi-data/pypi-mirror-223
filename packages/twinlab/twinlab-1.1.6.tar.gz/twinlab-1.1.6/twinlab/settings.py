# Standard imports
from typing import Optional

# Third-party imports
from pydantic import BaseSettings

#  Project imports
from ._version import __version__


class Environment(BaseSettings):
    TWINLAB_TRAINING_SERVER: Optional[str]
    TWINLAB_SERVER: str
    TWINLAB_GROUPNAME: str
    TWINLAB_USERNAME: str
    TWINLAB_TOKEN: str

    class Config:
        env_prefix = ""
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


ENV = Environment()

print()
print("         === TwinLab Client Initialisation ===")
if ENV.TWINLAB_TRAINING_SERVER:
    print(f"         Training : {ENV.TWINLAB_TRAINING_SERVER}")
print(f"         Server   : {ENV.TWINLAB_SERVER}")
print(f"         Group    : {ENV.TWINLAB_GROUPNAME}")
print(f"         User     : {ENV.TWINLAB_USERNAME}")
print(f"         Version  : {__version__}")
print()
