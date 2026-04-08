import uvicorn
from openenv.core.env_server import create_fastapi_app

from environment import CustomerSupportEnv
from models import SupportAction, SupportObservation

app = create_fastapi_app(
    CustomerSupportEnv,
    SupportAction,
    SupportObservation
)


def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()