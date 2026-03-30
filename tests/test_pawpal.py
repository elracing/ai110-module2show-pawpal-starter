import pytest
from pawpal_system import Dog, Task


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
