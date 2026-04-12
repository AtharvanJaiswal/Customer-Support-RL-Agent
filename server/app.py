from openenv.core.env_server import create_fastapi_app
from environment import CustomerSupportEnv
from models import SupportAction, SupportObservation
import uvicorn

app = create_fastapi_app(
    CustomerSupportEnv,
    SupportAction,
    SupportObservation
)

@app.get("/")
def root():
    return {
        "message": "Customer Support RL Agent is running 🚀",
        "docs": "/docs",
        "reset": "/reset",
        "step": "/step"
    }

# ✅ ADD THIS (CRITICAL FIX)
@app.get("/tasks")
def get_tasks():
    return []

# ✅ REQUIRED for OpenEnv
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

# ✅ ENTRY POINT
if __name__ == "__main__":
    main()