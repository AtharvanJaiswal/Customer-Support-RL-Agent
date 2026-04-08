from openenv.core.env_server import create_fastapi_app

from environment import CustomerSupportEnv
from models import SupportAction, SupportObservation

# ✅ FIX: create_fastapi_app takes positional args (env instance, action_cls, observation_cls)
# NOT keyword args like env_class=, action_type=, observation_type=
app = create_fastapi_app(CustomerSupportEnv, SupportAction, SupportObservation)