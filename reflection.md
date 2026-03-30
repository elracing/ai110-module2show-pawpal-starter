# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

User should be able to add a pet, schedule feeding and make daily plans for pets. I chose the class pet, owner, task and daily plan which will detail the pet, the owner, the task and the daily plan comprissed of tasks for a pet.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

no

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

scheduler uses time and priority, they re given a priority number depnending on effort

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

scheduler fills all the required tasks first then optional, its reasonale as required are assumed essentials.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

it helped me write the classes, the skeleton creation was most helpful

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Tested for conflict resolutiion the most, as there are multiple priorities set in place for the scheduler.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Im confident it works, as it ran tests better than I could. It also works when used manually. I would test for non animal edge cases next.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
how helpful AI was to make this quickly.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
better UI redesign. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
AI does some great testing.
