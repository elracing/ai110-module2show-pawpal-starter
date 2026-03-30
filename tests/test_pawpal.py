import pytest
from pawpal_system import DailyPlan, Dog, Owner, Task


def test_task_mark_complete_sets_completed_flag():
    task = Task(title="Test task", duration_minutes=10, priority="low")
    assert not task.completed

    task.mark_complete()
    assert task.completed


def test_dog_add_task_increases_task_count():
    dog = Dog(name="Mochi", species="dog")
    assert dog.task_count == 0

    t1 = Task(title="Walk", duration_minutes=20, priority="high")
    t2 = Task(title="Feed", duration_minutes=10, priority="medium")

    dog.add_task(t1)
    assert dog.task_count == 1

    dog.add_task(t2)
    assert dog.task_count == 2


def test_recurring_task_creates_next_occurrence_on_complete():
    owner = Owner(name="Jordan", available_minutes_per_day=60)
    dog = Dog(name="Mochi", species="dog")
    plan = DailyPlan(owner=owner, dog=dog)

    task = Task(
        title="Daily walk",
        duration_minutes=20,
        priority="high",
        frequency="daily",
        time="09:00",
    )

    owner.add_task(task)
    plan.generate_schedule()

    assert task in plan.scheduled_tasks

    plan.mark_task_complete(task)

    # original task removed from today's schedule
    assert task not in plan.scheduled_tasks
    # completed flag is set on original task
    assert task.completed

    # new daily task should be added back to owner tasks (for the next day)
    assert any(t.title == "Daily walk" and not t.completed for t in owner.tasks)

