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


def test_sort_by_time_orders_tasks_chronologically():
    owner = Owner(name="Jordan", available_minutes_per_day=120)
    dog = Dog(name="Mochi", species="dog")
    plan = DailyPlan(owner=owner, dog=dog)

    task1 = Task(title="Evening", duration_minutes=15, priority="low", time="18:00")
    task2 = Task(title="Morning", duration_minutes=15, priority="low", time="08:00")
    task3 = Task(title="Noon", duration_minutes=15, priority="low", time="12:00")

    owner.add_task(task1)
    owner.add_task(task2)
    owner.add_task(task3)
    plan.generate_schedule()

    plan.sort_by_time()
    assert [t.time for t in plan.scheduled_tasks] == ["08:00", "12:00", "18:00"]


def test_recurring_task_complete_enqueue_next_day():
    owner = Owner(name="Jordan", available_minutes_per_day=60)
    dog = Dog(name="Mochi", species="dog")
    plan = DailyPlan(owner=owner, dog=dog)

    task = Task(title="Daily walk", duration_minutes=20, priority="high", frequency="daily", time="09:00")
    owner.add_task(task)
    plan.generate_schedule()

    plan.mark_task_complete(task)

    assert task.completed
    next_tasks = [t for t in owner.tasks if t.title == "Daily walk" and t is not task]
    assert len(next_tasks) == 1
    next_task = next_tasks[0]
    assert not next_task.completed
    assert next_task.frequency == "daily"
    assert next_task.time == "09:00"


def test_check_conflicts_reports_duplicate_times():
    owner = Owner(name="Jordan", available_minutes_per_day=120)
    dog = Dog(name="Mochi", species="dog")
    plan = DailyPlan(owner=owner, dog=dog)

    t1 = Task(title="Feed Mochi", duration_minutes=10, priority="high", time="08:00")
    t2 = Task(title="Brush Mochi", duration_minutes=10, priority="medium", time="08:00")
    t3 = Task(title="Walk Mochi", duration_minutes=20, priority="high", time="09:00")

    owner.add_task(t1)
    owner.add_task(t2)
    owner.add_task(t3)
    plan.generate_schedule()

    conflicts = plan.check_conflicts()
    assert len(conflicts) == 1
    assert "Conflict at 08:00" in conflicts[0]

