from __future__ import annotations

from typing import TYPE_CHECKING, Final

from shards_ai_agents.utilities.constants import _NotSpecified


if TYPE_CHECKING:
    from shards_ai_agents.task import Task
    from shards_ai_agents.tasks.task_output import TaskOutput


DIVIDERS: Final[str] = "\n\n----------\n\n"


def aggregate_raw_outputs_from_task_outputs(task_outputs: list[TaskOutput]) -> str:
    """Generate string context from the task outputs.

    Args:
        task_outputs: List of TaskOutput objects.

    Returns:
        A string containing the aggregated raw outputs from the task outputs.
    """

    return DIVIDERS.join(output.raw for output in task_outputs)


def aggregate_raw_outputs_from_tasks(tasks: list[Task] | _NotSpecified) -> str:
    """Generate string context from the tasks.

    Args:
        tasks: List of Task objects or _NotSpecified.

    Returns:
        A string containing the aggregated raw outputs from the tasks.
    """

    task_outputs = (
        [task.output for task in tasks if task.output is not None]
        if isinstance(tasks, list)
        else []
    )

    return aggregate_raw_outputs_from_task_outputs(task_outputs)
