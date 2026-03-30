import streamlit as st
from pawpal_system import Owner, Dog, Task, DailyPlan

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This is now wired to the core PawPal scheduling model.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
owner_available = st.number_input("Available minutes per day", min_value=10, max_value=1440, value=120)

if "pets" not in st.session_state:
    st.session_state.pets = []

with st.expander("Add a Pet"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=30, value=3)
    energy_level = st.selectbox("Energy level", ["low", "medium", "high"], index=2)

    if st.button("Add Pet"):
        pet = Dog(name=pet_name, species=species, age=age, energy_level=energy_level)
        st.session_state.pets.append(pet)

if st.session_state.pets:
    st.write("Pets:")
    for i, pet in enumerate(st.session_state.pets, start=1):
        st.write(f"{i}. {pet.name} ({pet.species}, energy {pet.energy_level})")

st.markdown("### Tasks")
st.caption("Add a task to the chosen owner/pet and schedule it.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority, "required": True}
    )

    # use Owner.add_task method from domain model
    if "owner" in st.session_state and isinstance(st.session_state.owner, Owner):
        st.session_state.owner.add_task(
            Task(title=task_title, duration_minutes=int(duration), priority=priority, required=True)
        )

    # assign task to first pet if available
    if st.session_state.pets:
        st.session_state.pets[0].add_task(
            Task(title=task_title, duration_minutes=int(duration), priority=priority, required=True)
        )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Click to generate the daily plan from your tasks.")

if st.button("Generate schedule"):
    if not owner_name.strip() or not pet_name.strip():
        st.error("Owner and pet names must be provided")
    elif not st.session_state.tasks:
        st.error("Please add at least one task")
    else:
        if "owner" in st.session_state and isinstance(st.session_state.owner, Owner):
            owner = st.session_state.owner
        else:
            owner = Owner(name=owner_name, available_minutes_per_day=int(owner_available))
            st.session_state.owner = owner

        if st.session_state.pets and isinstance(st.session_state.pets[0], Dog):
            dog = st.session_state.pets[0]
        else:
            # fallback if no pet added
            dog = Dog(name=pet_name, species=species)
            if "pets" not in st.session_state:
                st.session_state.pets = []
            st.session_state.pets.append(dog)

        owner.tasks.clear()
        for raw in st.session_state.tasks:
            task = Task(
                title=raw["title"],
                duration_minutes=int(raw["duration_minutes"]),
                priority=raw["priority"],
                required=raw.get("required", True),
            )
            owner.add_task(task)
            dog.add_task(task)

        plan = DailyPlan(owner=owner, dog=dog)
        try:
            plan.generate_schedule()
            plan.sort_by_time()

            st.success("Schedule generated")
            st.markdown("### Plan explanation")
            st.text(plan.explain_plan())

            conflicts = plan.check_conflicts()
            if conflicts:
                st.warning("Task conflicts detected. Fix overlapping times for safer pet care:")
                for c in conflicts:
                    st.warning(c)
            else:
                st.success("No conflicts detected.")

            st.markdown("### Scheduled tasks (sorted by time)")
            st.table(
                [
                    {
                        "time": t.time or "unscheduled",
                        "title": t.title,
                        "duration": t.duration_minutes,
                        "priority": t.priority,
                        "category": t.category,
                        "required": t.required,
                        "completed": t.completed,
                    }
                    for t in plan.scheduled_tasks
                ]
            )
        except Exception as exc:
            st.error(f"Failed to generate schedule: {exc}")

        try:
            plan.generate_schedule()
            st.success("Schedule generated")
            st.markdown("### Plan explanation")
            st.text(plan.explain_plan())

            st.markdown("### Scheduled tasks")
            st.table(
                [
                    {
                        "title": t.title,
                        "duration": t.duration_minutes,
                        "priority": t.priority,
                        "category": t.category,
                        "required": t.required,
                    }
                    for t in plan.scheduled_tasks
                ]
            )
        except Exception as exc:
            st.error(f"Failed to generate schedule: {exc}")
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
