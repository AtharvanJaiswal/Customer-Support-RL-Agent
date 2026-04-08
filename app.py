from openenv.core.env_server import create_fastapi_app

from environment import CustomerSupportEnv
from models import SupportAction, SupportObservation

app = create_fastapi_app(
    env_class=CustomerSupportEnv,
    action_type=SupportAction,
    observation_type=SupportObservation
)
