from openenv.core.env_server import create_fastapi_app

from environment import CustomerSupportEnv
from models import SupportAction, SupportObservation

app = create_fastapi_app(
    CustomerSupportEnv,
    SupportAction,
    SupportObservation
)