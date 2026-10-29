"""Base event listener for Shards-ai-agents event system."""

from abc import ABC, abstractmethod

from shards_ai_agents.events.event_bus import (
    ShardsAgentsEventsBus,
    shards_ai_agents_event_bus,
)


class BaseEventListener(ABC):
    """Abstract base class for event listeners."""

    verbose: bool = False

    def __init__(self) -> None:
        """Initialize the event listener and register handlers."""
        super().__init__()
        self.setup_listeners(shards_ai_agents_event_bus)
        shards_ai_agents_event_bus.validate_dependencies()

    @abstractmethod
    def setup_listeners(
        self, shards_ai_agents_event_bus: ShardsAgentsEventsBus
    ) -> None:
        """Setup event listeners on the event bus.

        Args:
            shards_ai_agents_event_bus: The event bus to register listeners on.
        """
