from pawpal_system import Owner, Dog, Task, DailyPlan


def main():
    owner = Owner(name="Jordan", available_minutes_per_day=180)

    pet1 = Dog(name="Mochi", species="dog", age=3, energy_level="high")
    pet2 = Dog(name="Whiskers", species="cat", age=5, energy_level="medium")

    owner.add_task(
        Task(
            title="Morning walk for Mochi",
            duration_minutes=30,
            priority="high",
            category="walk",
            description="Mochi",
        )
    )
    owner.add_task(
        Task(
            title="Feed Mochi",
            duration_minutes=10,
            priority="high",
            category="feed",
            description="Mochi",
        )
    )
    owner.add_task(
        Task(
            title="Play with Whiskers",
            duration_minutes=20,
            priority="medium",
            category="enrichment",
            description="Whiskers",
        )
    )

    daily_plan = DailyPlan(owner=owner, dog=pet1)
    daily_plan.generate_schedule()

    print("Today's Schedule")
    print("===============")
    print(daily_plan.explain_plan())
    print()
    print("Tasks scheduled:")
    for t in daily_plan.scheduled_tasks:
        print(f"- {t.title} ({t.duration_minutes}m) [{t.priority}] for {t.description or 'unknown pet'}")


if __name__ == "__main__":
    main()
