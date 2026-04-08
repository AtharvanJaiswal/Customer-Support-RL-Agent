from typing import Optional
from openenv.core.env_server import Action, Observation, State

class SupportAction(Action):
    category: str
    priority: str
    response: str

class SupportObservation(Observation):
    ticket_id: str
    customer_query: str
    done: bool = False
    reward: Optional[float] = None

class SupportState(State):
    episode_id: Optional[str] = None  # ✅ FIX: was missing, used in environment.py reset()
    step_count: int = 0
    tickets_processed: int = 0
    total_tickets: int = 0