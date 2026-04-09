import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn
from pydantic import BaseModel

from openenv.core.env_server import create_fastapi_app

try:
    from server.environment import CustomerSupportEnv
    from models import SupportAction, SupportObservation
    from task_definitions import TASKS, grade
except ImportError:
    from environment import CustomerSupportEnv
    from models import SupportAction, SupportObservation
    from task_definitions import TASKS, grade

# Core OpenEnv app (provides /reset, /step, /state, /health)
app = create_fastapi_app(
    CustomerSupportEnv,
    SupportAction,
    SupportObservation
)


# ── /tasks endpoint ───────────────────────────────────────────────────────────

@app.get("/tasks")
def list_tasks():
    return {
        "tasks": [
            {
                "id": t["id"],
                "name": t["name"],
                "description": t["description"],
                "difficulty": t["difficulty"],
                "sample_query": t["sample_query"],
            }
            for t in TASKS.values()
        ]
    }


# ── /grader endpoint ──────────────────────────────────────────────────────────

class GraderRequest(BaseModel):
    task_id: str
    action: dict


@app.post("/grader")
def grader(request: GraderRequest):
    score = grade(request.task_id, request.action)
    return {
        "task_id": request.task_id,
        "score": score,
        "passed": score > 0.5,
    }


# ── entry point ───────────────────────────────────────────────────────────────

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)  # ✅ HF Spaces port


if __name__ == "__main__":
    main()