from openenv.core.env_server import create_fastapi_app

from environment import CustomerSupportEnv
from models import SupportAction, SupportObservation

# Create OpenEnv app
app = create_fastapi_app(
    CustomerSupportEnv,
    SupportAction,
    SupportObservation
)

# ✅ ADD ROOT ROUTE HERE (THIS IS THE REAL FIX)
@app.get("/")
def root():
    return {
        "message": "Customer Support RL Agent is running 🚀",
        "docs": "/docs",
        "reset": "/reset",
        "step": "/step"
    }