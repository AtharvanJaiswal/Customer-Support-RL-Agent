from openenv.core.env_server import create_fastapi_app
from fastapi import Request

from environment import CustomerSupportEnv
from models import SupportAction, SupportObservation

# Create OpenEnv app (THIS is the main app)
app = create_fastapi_app(
    CustomerSupportEnv,
    SupportAction,
    SupportObservation
)

# ✅ Inject root route INTO SAME APP
@app.get("/")
async def root():
    return {
        "message": "Customer Support RL Agent is running 🚀",
        "docs": "/docs",
        "reset": "/reset",
        "step": "/step"
    }