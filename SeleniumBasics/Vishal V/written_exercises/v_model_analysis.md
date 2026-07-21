# SDLC vs TDLC — V-Model & Agile QA Integration

## Task 1: V-Model Mapping

### 9. The V-Model Diagram

**Technical Definition:** The V-Model (Verification and Validation Model) is an SDLC/TDLC model where each development phase on the left side has a corresponding testing phase on the right side, connected by a horizontal line — forming a "V" shape. Development moves downward (getting more detailed) until it hits **Coding** at the bottom, then testing moves upward (getting broader again) as the system gets validated against each earlier design phase.

**In simple terms:** Imagine building a house. First you plan broadly (what rooms do we need?), then you get more and more detailed (exact wiring, exact pipes), then you actually build it. After building, you test it in the reverse order — first check individual components (does this switch work?), then check rooms together (does the kitchen and bathroom plumbing connect properly?), then the whole house, then finally you ask the family: "Does this house actually meet what you wanted?" That reverse-order checking is exactly what the V-Model represents.

**Flow of the V-Model:**

**Requirements** -> **System Design** -> **Architecture Design** -> **Module Design** -> `Coding`
 
`Coding` -> **Unit Testing** -> **Integration Testing** -> **System Testing** -> **Acceptance Testing**.

```
DEVELOPMENT (Left)                              TESTING (Right)

Requirements  --------------------------------  Acceptance Testing
      \                                              /
       \                                            /
   System Design  ------------------------  System Testing
         \                                        /
          \                                      /
    Architecture Design  --------------  Integration Testing
             \                                /
              \                              /
        Module Design  --------------  Unit Testing
                \                          /
                 \                        /
                  \                      /
                   \                    /
                    \                  /
                     \                /
                      \              /
                       \            /
                        \          /
                         \        /
                          \      /
                           \    /
                            \  /
                             \/
                          CODING
                       (Bottom Vertex)
```

Each dashed horizontal line represents a **direct relationship** — the development phase on the left defines what will be verified by the testing phase on the right.

---

### 10. Test Artifacts Produced Per Phase

| SDLC Phase (Left) | TDLC Phase (Right) | Test Artifact Produced During Development Phase | Simple Explanation |
|---|---|---|---|
| **Requirements** | Acceptance Testing | Acceptance Test Plan / User Acceptance Test Cases | While the business analyst is writing "what the system should do," QA is already writing "how we'll prove it does that" — e.g., an Acceptance Test Plan for the Course Management API confirming an admin can create, view, and manage courses. |
| **System Design** | System Testing | System Test Plan | While architects decide how the whole system fits together (API + DB + Auth service), QA drafts a plan for testing the complete end-to-end flow, e.g., "create course → verify in DB → retrieve via GET." |
| **Architecture Design** | Integration Testing | Integration Test Plan | While the team decides how components (API layer, database layer, authentication service) will talk to each other, QA prepares a plan to test those connections, e.g., testing that the API layer correctly calls the database layer. |
| **Module Design** | Unit Testing | Unit Test Cases / Unit Test Plan | While developers design individual functions/modules (e.g., `validate_course_name()`), test cases are drafted for each function in isolation. |

**Simple takeaway:** Notice the pattern — **test planning happens at the same time as the matching development phase, not after it.** This is one of the earliest hints of the "Shift-Left" principle we'll cover in Task 2: you don't wait until coding is done to start thinking about tests.

---

### 11. Entry & Exit Criteria for All Four Testing Levels

**Technical Definitions:**
- **Entry Criteria** = the conditions that must be satisfied before a testing phase can *begin*.
- **Exit Criteria** = the conditions that must be satisfied before a testing phase can be considered *complete/done*.

**In simple terms:** Entry criteria is like a checklist you must complete before you're "allowed" to start a task (e.g., before you can start cooking, you need all ingredients ready). Exit criteria is the checklist that proves you're actually "done" (e.g., the dish is cooked through, tastes right, and is plated).

#### a) Unit Testing

| | Criteria |
|---|---|
| **Entry Criteria** | - Module/function code is complete and compiles without errors.<br>- Unit test cases have been written/reviewed.<br>- Developer has access to a local/dev environment to run tests. |
| **Exit Criteria** | - All planned unit test cases have been executed.<br>- Code coverage meets the agreed threshold (e.g., 80%).<br>- No critical/high-severity defects remain open in the unit under test. |

#### b) Integration Testing

| | Criteria |
|---|---|
| **Entry Criteria** | - Unit testing is complete for all individual modules involved.<br>- Interfaces/APIs between modules (e.g., API layer ↔ database layer) are defined and available.<br>- Test environment with all integrated components is set up (e.g., API + test database). |
| **Exit Criteria** | - All planned integration test cases have been executed.<br>- All module-to-module data flows (e.g., API → DB) work correctly.<br>- No critical/high-severity defects remain open. |

#### c) System Testing

| | Criteria |
|---|---|
| **Entry Criteria** | - Integration testing is complete and stable.<br>- The full application (API + database + authentication, etc.) is deployed in a test/staging environment resembling production.<br>- System test cases and test data are ready. |
| **Exit Criteria** | - All planned system test cases have been executed.<br>- All major end-to-end flows work correctly (e.g., full course creation-to-retrieval flow).<br>- Defect count is below the agreed threshold, with no open critical/high defects. |

#### d) Acceptance Testing (UAT)

| | Criteria |
|---|---|
| **Entry Criteria** | - System testing is complete and the system is stable.<br>- A UAT environment is available, closely resembling production.<br>- Business/end users (e.g., college admin representatives) are available and briefed on what to test. |
| **Exit Criteria** | - All acceptance criteria/user stories have been validated by the end user.<br>- The end user formally signs off that the system meets business needs.<br>- No open critical/high defects that block real-world usage. |

---

### 12. Two Early QA Engagement Points (Beyond Just Testing Phases)

The hint reminds us: QA shouldn't wait until "testing phases" begin — QA should be involved on the **left side of the V** too. Here are two concrete places for the Course Management API project:

1. **Requirements Review Stage:**
   QA reviews the requirement "Admin should be able to create a course" and asks clarifying questions *before any code is written*: "What happens if the course code already exists? Is course name mandatory? What's the max length for course name? What HTTP status code should be returned on validation failure?" Catching these ambiguities here is far cheaper than discovering them during System Testing, when developers would need to rework already-built code.

2. **Architecture/API Design Review Stage:**
   QA reviews the proposed API contract (e.g., the OpenAPI/Swagger spec) for `POST /api/courses/` before development starts — checking that response codes, error formats, and required fields are clearly and consistently defined. This allows QA to also start writing integration test cases in parallel with development, instead of waiting until the API is built.

**In simple terms:** It's like a chef tasting and questioning the recipe *before* cooking starts (checking if ingredients and quantities make sense) rather than only tasting the final dish. Catching a mistake in the recipe is far cheaper than remaking the whole dish.

---

## Task 2: Agile QA and Shift-Left Testing

### 13. Three Problems Caused by Waterfall Testing (Testing After Development)

In traditional Waterfall, **testing only starts after the entire development phase is "complete."** For the Course Management API project, this causes:

1. **Defects Are Found Too Late (and Too Expensive to Fix):**
   If a requirement ambiguity (e.g., "should course codes be unique?") isn't caught until system testing, the API, database schema, and validation logic may all need significant rework — instead of a one-line clarification during requirements review. Late-found bugs are exponentially more expensive to fix.

2. **No Time Buffer Before Release (Testing Gets Compressed):**
   Since testing only starts after coding wraps up, if development runs late (which is common), the testing phase gets squeezed into whatever time is left before the deadline. This often leads to rushed testing, skipped test cases, or the Course Management API going live with unverified edge cases (e.g., duplicate course codes never actually being tested).

3. **Poor Visibility Into Quality Until Very Late:**
   Since there's no continuous testing feedback, stakeholders have no real idea whether the Course Management API is on track for quality until testing begins — often weeks or months into the project. If major issues are then discovered (e.g., the entire authentication flow is broken), it can be a major shock late in the project timeline, with little room to react.

**In simple terms:** Waterfall testing is like never tasting your food until it's fully cooked and plated for the guests — if it turns out to be way too salty, it's too late to fix easily, you've wasted time, and the guests now see a bad result with no time to redo it.

---

### 14. QA's Role in Agile Ceremonies

| Agile Ceremony | QA Engineer's Role |
|---|---|
| **Sprint Planning** | QA works with the Product Owner and dev team to **define clear acceptance criteria** for each user story before it's committed to the sprint. For example, for "Admin creates a course," QA ensures the criteria clearly state what should happen for duplicate course codes, missing fields, etc. — so everyone has a shared, testable definition of "done." |
| **Daily Standup** | QA reports **testing progress and any blocking issues** — e.g., "I can't test the course creation flow because the staging environment is down" or "Found a blocker: the API doesn't return the expected error format for validation failures." This keeps the whole team aware of quality risks in real time, not just at the end of the sprint. |
| **Sprint Review** | QA supports **demo testing** — helping showcase that the completed features (e.g., course creation) actually work as expected in front of stakeholders, and may highlight what was tested vs. what's still pending. |
| **Retrospective** | QA contributes to **process improvement discussions** — e.g., "We found too many defects late in the sprint; let's get QA involved earlier in story refinement next sprint," or "Our test environment kept breaking — let's fix that as a team going forward." |

**In simple terms:** In Agile, QA isn't a "checkpoint at the end" — QA is a **teammate throughout the entire sprint**, from planning what "done" looks like, to raising issues daily, to demoing results, to helping the team get better next time.

---

### 15. Shift-Left Testing Practices Applied to the Course Management API

**Technical Definition:** Shift-Left Testing means moving testing activities **earlier** in the SDLC — instead of testing only after coding is complete, testing-related activities happen in parallel with (or even before) development.

**In simple terms:** Instead of only checking your work at the very end, you check continuously as you go — like proofreading each paragraph as you write an essay, instead of only reading it once at the very end.

| Practice | How It Applies to the Course Management API |
|---|---|
| **(a) Reviewing Requirements for Testability** | Before coding starts, QA reviews the requirement "Admin can create a course" and flags that it's not testable yet — asking, "What's the expected response code? Is course code uniqueness enforced?" This forces the requirement to be clarified into something concrete and verifiable before any code is written. |
| **(b) Writing Test Cases Before Code (TDD/BDD)** | Before the `POST /api/courses/` endpoint is coded, the team writes test cases like "creating a course with a duplicate code should return 409 Conflict" first. Developers then write code specifically to pass these pre-defined tests, ensuring requirements are met by design rather than checked as an afterthought. |
| **(c) Static Code Analysis** | Tools (e.g., linters, SonarQube, pylint) automatically scan the Course Management API's codebase for issues like unhandled exceptions, security vulnerabilities, or code smells — *before* the code is even run or tested manually. This catches problems the moment code is written, not weeks later. |
| **(d) API Contract Testing Before Integration** | Before the front-end team integrates with the Course Management API, the agreed API contract (e.g., an OpenAPI spec defining request/response formats) is tested in isolation — confirming the API returns exactly the structure promised (correct field names, types, status codes) — before any other team builds on top of it, preventing mismatched expectations later. |

---

### 16. Acceptance Criteria in Given-When-Then (Gherkin) Format

**User Story:** *As a college admin, I want to create a new course, so that students can enroll in it.*

```gherkin
Feature: Course Creation
  As a college admin
  I want to create a new course
  So that students can enroll in it

  Scenario: Successfully create a new course (Happy Path)
    Given I am logged in as an authenticated college admin
    And I provide valid course details (name, unique course code, credits, duration)
    When I submit a request to create the course
    Then the system should respond with a 201 Created status
    And the new course should be visible in the course list

  Scenario: Attempt to create a course with a duplicate course code
    Given I am logged in as an authenticated college admin
    And a course with the code "CS101" already exists in the system
    When I submit a request to create a new course using the code "CS101"
    Then the system should respond with a 409 Conflict status
    And an error message should indicate that the course code already exists
    And no duplicate course should be created in the database

  Scenario: Attempt to create a course with missing required fields
    Given I am logged in as an authenticated college admin
    And I do not provide a course name in the request
    When I submit a request to create the course
    Then the system should respond with a 400 Bad Request status
    And an error message should indicate that the course name is required
    And no course should be created in the database
```

**In simple terms:** "Given" sets the starting situation, "When" is the action taken, and "Then" is what should happen as a result. Writing criteria this way means both developers and QA understand *exactly* what "correct behavior" looks like — and these Gherkin scenarios can later be turned directly into automated tests using tools like Cucumber or Behave, saving double effort.
