from openenv.core.env_client import EnvClient
from openenv.core.client_types import StepResult
from models import SupportAction, SupportObservation, SupportState

class CustomerSupportClient(EnvClient[SupportAction, SupportObservation, SupportState]):

    def _step_payload(self, action: SupportAction):
        return {
            "category": action.category,
            "priority": action.priority,
            "response": action.response
        }

    def _parse_result(self, payload):
        obs = payload.get("observation", {})
        return StepResult(
            observation=SupportObservation(
                ticket_id=obs.get("ticket_id", ""),
                customer_query=obs.get("customer_query", ""),
                done=payload.get("done", False),
                reward=payload.get("reward")
            ),
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload):
        return SupportState(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
            tickets_processed=payload.get("tickets_processed", 0),
            total_tickets=payload.get("total_tickets", 0),
        )