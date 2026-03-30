from pawpal_system import Owner, Dog, Task, DailyPlan


def main():
    """Run a sample PawPal daily scheduling demo in console output."""
    owner = Owner(name="Jordan", available_minutes_per_day=180)

    pet1 = Dog(name="Mochi", species="dog", age=3, energy_level="high")
    pet2 = Dog(name="Whiskers", species="cat", age=5, energy_level="medium")

    owner.add_task(
        Task(
            title="Lunch for Whiskers",
            duration_minutes=15,
            priority="medium",
            category="feed",
            description="Whiskers",
            time="12:00",
        )
    )
    owner.add_task(
        Task(
            title="Brush Whiskers",
            duration_minutes=10,
            priority="low",
            category="grooming",
            description="Whiskers",
            time="12:00",
        )
    )
    owner.add_task(
        Task(
            title="Evening walk for Mochi",
            duration_minutes=30,
            priority="high",
            category="walk",
            description="Mochi",
            time="18:00",
        )
    )
    owner.add_task(
        Task(
            title="Morning feed Mochi",
            duration_minutes=10,
            priority="high",
            category="feed",
            description="Mochi",
            time="08:00",
        )
    )

    daily_plan = DailyPlan(owner=owner, dog=pet1)
    daily_plan.generate_schedule()

    # mark one task complete for filtering demo
    if daily_plan.scheduled_tasks:
        daily_plan.scheduled_tasks[1].mark_complete()

    print("Today's Schedule")
    print("===============")
    print(daily_plan.explain_plan())
    print()

    # demo sort_by_time using lambda key to sort HH:MM strings
    daily_plan.sort_by_time()
    print("\nSorted schedule by time:")
    for t in daily_plan.scheduled_tasks:
        print(f"- {t.time} {t.title} [{t.category}]")

    # demo filtering: completed tasks
    completed_tasks = daily_plan.filter_tasks(completed=True)
    print("\nCompleted tasks:")
    for t in completed_tasks:
        print(f"- {t.title} (completed={t.completed})")

    # demo filtering: by pet name
    mochis_tasks = daily_plan.filter_tasks(pet_name="Mochi")
    print("\nTasks for Mochi:")
    for t in mochis_tasks:
        print(f"- {t.title} (desc={t.description})")

    # conflict detection
    conflicts = daily_plan.check_conflicts()
    if conflicts:
        print("\nConflict warnings:")
        for warn in conflicts:
            print(f"- {warn}")
    else:
        print("\nNo conflicts detected.")


if __name__ == "__main__":
    main()
