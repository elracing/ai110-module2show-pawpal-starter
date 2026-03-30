from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low"|"medium"|"high"
    category: str = "general"  # walk/feed/meds/enrichment/grooming
    required: bool = True
    description: Optional[str] = None

    def estimate_effort(self) -> int:
        mapping = {"low": 1, "medium": 2, "high": 3}
        return mapping.get(self.priority, 1)


@dataclass
class Dog:
    name: str
    species: str
    age: Optional[int] = None
    breed: Optional[str] = None
    size: Optional[str] = None
    energy_level: Optional[str] = None  # low/medium/high
    needs_medication: bool = False

    def need_summary(self) -> str:
        return (
            f"{self.name}: {self.species}, "
            f"medication required={self.needs_medication}, "
            f"energy={self.energy_level or 'unknown'}"
        )


@dataclass
class Owner:
    name: str
    email: Optional[str] = None
    available_minutes_per_day: int = 60
    tasks: List[Task] = field(default_factory=list)
    preferences: List[str] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        self.tasks = [t for t in self.tasks if t != task]

    def get_priority_tasks(self, min_priority: str = "medium") -> List[Task]:
        order = {"low": 0, "medium": 1, "high": 2}
        thresh = order.get(min_priority, 1)
        return [t for t in self.tasks if order.get(t.priority, 0) >= thresh]


@dataclass
class DailyPlan:
    day: date = field(default_factory=date.today)
    owner: Owner = field(default_factory=Owner)
    dog: Dog = field(default_factory=Dog)
    scheduled_tasks: List[Task] = field(default_factory=list)
    total_time_minutes: int = 0
    explanation: Optional[str] = None

    def add_task(self, task: Task) -> None:
        self.scheduled_tasks.append(task)
        self.total_time_minutes += task.duration_minutes

    def remove_task(self, task: Task) -> None:
        self.scheduled_tasks = [t for t in self.scheduled_tasks if t != task]
        self.total_time_minutes = sum(t.duration_minutes for t in self.scheduled_tasks)

    def generate_schedule(self, available_minutes: Optional[int] = None) -> None:
        if available_minutes is None:
            available_minutes = self.owner.available_minutes_per_day

        order = {"low": 0, "medium": 1, "high": 2}
        sorted_tasks = sorted(
            self.owner.tasks,
            key=lambda t: order.get(t.priority, 0),
            reverse=True,
        )

        self.scheduled_tasks.clear()
        self.total_time_minutes = 0

        for task in sorted_tasks:
            if self.total_time_minutes + task.duration_minutes <= available_minutes:
                self.scheduled_tasks.append(task)
                self.total_time_minutes += task.duration_minutes

        self.explanation = (
            f"Selected {len(self.scheduled_tasks)} tasks "
            f"({self.total_time_minutes}m of {available_minutes}m)."
        )

    def explain_plan(self) -> str:
        return self.explanation or "No schedule generated yet."
