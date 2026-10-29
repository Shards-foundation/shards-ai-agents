"""Test utilities for Shards-ai-agents tests."""

import asyncio
from concurrent.futures import ThreadPoolExecutor


def wait_for_event_handlers(timeout: float = 5.0) -> None:
    """Wait for all pending event handlers to complete.

    This helper ensures all sync and async handlers finish processing before
    proceeding. Useful in tests to make assertions deterministic.

    Args:
        timeout: Maximum time to wait in seconds.
    """
    from shards_ai_agents.events.event_bus import shards_ai_agents_event_bus

    loop = getattr(shards_ai_agents_event_bus, "_loop", None)

    if loop and not loop.is_closed():

        async def _wait_for_async_tasks() -> None:
            tasks = {
                t for t in asyncio.all_tasks(loop) if t is not asyncio.current_task()
            }
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

        future = asyncio.run_coroutine_threadsafe(_wait_for_async_tasks(), loop)
        try:
            future.result(timeout=timeout)
        except Exception:  # noqa: S110
            pass

    # Guard against lazy-initialized executor (may not exist if no events were emitted)
    if getattr(shards_ai_agents_event_bus, "_executor_initialized", False):
        shards_ai_agents_event_bus._sync_executor.shutdown(wait=True)
        shards_ai_agents_event_bus._sync_executor = ThreadPoolExecutor(
            max_workers=10,
            thread_name_prefix="ShardsAgentsSyncHandler",
        )
