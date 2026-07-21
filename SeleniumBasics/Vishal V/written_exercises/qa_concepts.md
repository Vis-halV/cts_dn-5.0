# QA Concepts, Functional Testing & Defect Lifecycle

## Task 1: Map Testing Types to a Real System

### 1. Test Levels — Unit, Integration, System, UAT

Before jumping into test cases, here's what each level means in plain words:

| Test Level | Technical Definition | Layman's Terms |
|---|---|---|
| **Unit Testing** | Testing a single function/module in isolation, without its dependencies | Checking one small "ingredient" works before cooking the whole dish — e.g., does the function that validates a course name actually reject an empty name? |
| **Integration Testing** | Testing how two or more components work together | Checking that the ingredients combine properly — e.g., does the API endpoint actually save data correctly into the database? |
| **System Testing** | Testing the complete, end-to-end flow of the application as a whole | Tasting the entire dish after cooking — e.g., a user sends a request from the app and gets the correct final response back. |
| **User Acceptance Testing (UAT)** | Testing done by/for the actual end user to confirm the system meets real business needs | Serving the dish to the customer and asking "is this what you wanted?" — e.g., does a college admin actually find the course creation process easy and correct? |

Now applying these to our **Course Management API**:

#### a) Unit Testing
**Test Case:** Test the `validate_course_name()` function in isolation.
- **What we do:** Call the function directly with an empty string `""` as input.
- **Expected Result:** Function returns `False` or raises a `ValidationError`, without needing the API or database running at all.
- **In simple terms:** We're not testing the whole app — just this one small piece of logic, like checking if a single Lego brick is the right shape before building anything with it.

#### b) Integration Testing
**Test Case:** Test that `POST /api/courses/` correctly saves a new course into the database.
- **What we do:** Send a valid POST request with course data, then directly query the database to confirm the record was actually inserted.
- **Expected Result:** The database contains a new row matching the submitted data.
- **In simple terms:** We're checking if two parts (the API and the database) are talking to each other correctly — like checking if you order food (API) and it actually reaches the kitchen (database).

#### c) System Testing
**Test Case:** Test the full flow — a client sends `POST /api/courses/` with valid data, and the client receives back a `201 Created` response containing the correct course details, and that course is then retrievable via `GET /api/courses/{id}`.
- **What we do:** Simulate a complete user journey from request to final confirmation.
- **Expected Result:** The entire chain works — creation, storage, and retrieval — without any manual intervention.
- **In simple terms:** This is like testing the entire restaurant experience — from placing the order to the food arriving at your table correctly. Nothing is checked in isolation; it's the whole journey.

#### d) User Acceptance Testing (UAT)
**Test Case:** A college admin logs in, creates a new course called "Data Structures" with correct details, and confirms it appears correctly in the admin dashboard's course list.
- **What we do:** Have an actual (or simulated) admin user perform their real daily task.
- **Expected Result:** The admin can complete the task without confusion, and the course appears exactly as expected.
- **In simple terms:** This isn't about code at all — it's about whether a real person, doing their real job, is happy with how the system behaves.

---

### 2. Functional vs Non-Functional Classification

| Test Case | Classification | Why |
|---|---|---|
| Unit test — validate course name | **Functional** | It checks *what* the system does (rejects invalid input) |
| Integration test — course saved to DB | **Functional** | It checks *what* the system does (correct data storage) |
| System test — full create-and-retrieve flow | **Functional** | It checks *what* the system does (correct end-to-end behavior) |
| UAT — admin creates a course | **Functional** | It checks *what* the system does from a user's perspective |

**Non-Functional Test Example:**
- **Test Case:** Send 100 concurrent `POST /api/courses/` requests and measure the average response time.
- **Expected Result:** Average response time should stay under 500ms even under load, and no requests should fail or time out.
- **Classification:** **Non-Functional** — specifically a **Performance** test.
- **In simple terms:** Functional testing asks "does the doorbell ring when I press it?" Non-functional testing asks "does it still ring in 2 seconds even if 100 people press it at once, and does it survive rain?" It's about *quality* and *behavior under conditions*, not just correctness.

Other examples of non-functional testing (for context):
- **Security:** Can an unauthenticated user access `POST /api/courses/`? (Should be blocked.)
- **Reliability:** Does the API stay up and consistent after running for 24 hours straight?

---

### 3. Black-Box Testing vs White-Box Testing

| | Technical Definition | Layman's Terms |
|---|---|---|
| **Black-Box Testing** | Testing the software's functionality without any knowledge of its internal code, logic, or structure — based purely on inputs and expected outputs | You're a customer testing a vending machine. You don't care what wires or chips are inside — you just press a button and check if you get the right snack. |
| **White-Box Testing** | Testing with full knowledge of the internal code structure, logic paths, and implementation — checking internal workings like loops, conditions, and code branches | You're the technician who opens up the vending machine and checks if every wire, sensor, and internal mechanism works correctly for every possible path. |

**Who typically performs which:**
- **Black-Box Testing** is typically performed by **QA Testers** — they test the application from a user's point of view, without needing to read the source code. This matches the QA role of validating behavior against requirements.
- **White-Box Testing** is typically performed by **Developers** — since it requires deep knowledge of the internal code (e.g., writing unit tests that check specific `if/else` branches or loops inside a function).

**Simple example using our API:**
- Black-Box: A QA tester sends a POST request with a course name of 200 characters and checks if the API correctly returns a "400 Bad Request" — without knowing *how* the validation is coded internally.
- White-Box: A developer writes a unit test that specifically checks whether the `if len(name) > 150` condition inside the validation function is triggered correctly, ensuring every line and branch of that function is executed at least once.

---

### 4. Formal Test Cases — `POST /api/courses/`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC_COURSE_001 | Verify that a course is created successfully with valid data | API server is running; admin is authenticated with a valid token | 1. Send `POST /api/courses/` with valid JSON body (`name`, `code`, `credits`, `duration`) 2. Observe the response | API returns `201 Created` with the newly created course object, including a generated `id` | | |
| TC_COURSE_002 | Verify that creating a course with a missing required field (`name`) is rejected | API server is running; admin is authenticated with a valid token | 1. Send `POST /api/courses/` with JSON body missing the `name` field 2. Observe the response | API returns `400 Bad Request` with an error message indicating `name` is required; no record is created in the database | | |
| TC_COURSE_003 | Verify that an unauthenticated user cannot create a course | API server is running; no authentication token is provided | 1. Send `POST /api/courses/` with valid course data but without an Authorization header 2. Observe the response | API returns `401 Unauthorized`; no record is created in the database | | |

*(Note: "Actual Result" and "Pass/Fail" columns are intentionally left blank, to be filled in during actual test execution.)*

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. The Defect Lifecycle

**Technical Definition:** The defect lifecycle is the series of states a bug passes through, from the moment it is discovered to the moment it is confirmed fixed and closed.

**In simple terms:** Think of a defect like a support ticket you raise for a broken appliance — it goes through stages until it's fixed and you confirm it's actually working.

**Main Path:**

```
New → Assigned → Open → Fixed → Retest → Verified → Closed
```

1. **New** — A tester finds a bug and logs it for the first time. *(Like calling the repair company and describing the problem.)*
2. **Assigned** — A lead or manager assigns the bug to a specific developer to fix. *(The repair company assigns a technician to your case.)*
3. **Open** — The developer has accepted the bug and is actively working on understanding/fixing it. *(The technician has started diagnosing the problem.)*
4. **Fixed** — The developer has made a code change believed to resolve the issue and marks it as fixed. *(Technician says "I've repaired it.")*
5. **Retest** — QA re-tests the specific scenario to confirm the fix actually works. *(You test the appliance yourself to see if it's really fixed.)*
6. **Verified** — QA confirms the fix works as expected and no new issues were introduced. *(You confirm: "Yes, it works now.")*
7. **Closed** — The defect is formally closed and considered resolved. *(Case closed, ticket archived.)*

**Alternate Paths:**

- **Rejected** — The developer/lead reviews the bug and determines it's not actually a bug (e.g., it's expected behavior, a duplicate, or a misunderstanding by the tester). *(Like the technician saying, "This isn't actually broken — that's how the appliance is designed to work.")*
- **Deferred** — The bug is valid, but the team decides to fix it in a later release/sprint due to low priority, time constraints, or resource limits. *(The technician says, "I see the issue, but we'll address it during your next scheduled maintenance visit, not now.")*
- If a bug is sent back from **Retest** because the fix didn't actually work, it typically goes back to **Open** or **Reopened** status, restarting the fix cycle.

---

### 6. Severity & Priority Classification for Hypothetical Bugs

**Quick definitions before we classify:**
- **Severity** = How badly does this bug damage the system's functionality? (a technical/impact measure)
- **Priority** = How urgently must this be fixed? (a business/scheduling measure)

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| **a) `POST /api/courses/` returns 500 for all requests** | **Critical** | **P1** | This completely breaks the core functionality of the API — no course can be created at all. It blocks all users and has no workaround. Both impact and urgency are at their highest. |
| **b) Course names longer than 150 characters are silently truncated without error** | **Medium** | **P3** | The feature technically still "works" (data is saved), but silently truncating data without warning the user is a data-integrity issue. It doesn't crash the system or block usage, so it's not urgent, but it should be fixed soon since it can lead to incorrect/misleading data over time. |
| **c) `/docs` Swagger page has a typo in the API description** | **Low** | **P4** | This is purely cosmetic — it doesn't affect functionality, data, or usage in any way. It can be fixed whenever convenient, with no rush. |
| **d) Login with correct credentials occasionally returns 401 on first attempt (intermittent)** | **High** | **P1/P2** | Even though it doesn't happen every time, this is a core authentication flow failure. Intermittent bugs are dangerous because they're hard to reproduce and often point to deeper issues (e.g., race conditions, token timing issues). Because it affects the ability to log in — a critical function — it needs urgent investigation despite its "sometimes" nature. |

---

### 7. Formal Defect Report — Bug (a)

| Field | Details |
|---|---|
| **Defect ID** | DEF-2026-0142 |
| **Title** | `POST /api/courses/` returns HTTP 500 Internal Server Error for all requests |
| **Environment** | Staging Environment — Ubuntu 24.04, Python 3.11, FastAPI backend |
| **Build Version** | v1.4.2-staging |
| **Severity** | Critical |
| **Priority** | P1 |
| **Steps to Reproduce** | 1. Authenticate as an admin user and obtain a valid token. 2. Send a `POST` request to `/api/courses/` with a valid JSON body containing `name`, `code`, `credits`, and `duration`. 3. Observe the API response. |
| **Expected Result** | API should return `201 Created` along with the newly created course object in the response body. |
| **Actual Result** | API returns `500 Internal Server Error` with no course data, and no record is created in the database. |
| **Attachments** | screenshot of 500 error |

---

### 8. Severity vs Priority — With a Real-World Example

**Technical Definitions:**
- **Severity** measures the *technical impact* of a defect on the system — how badly it breaks functionality, data integrity, or stability.
- **Priority** measures the *business urgency* of fixing a defect — how soon it needs to be addressed, based on factors like visibility, deadlines, and stakeholder impact.

**In simple terms:** Severity asks *"how bad is the damage?"*. Priority asks *"how fast do we need to act?"*. They often go together, but not always — that's the tricky part beginners often miss.

**Real-world example of High Severity ≠ High Priority:**

Imagine a **payment gateway crashes only during a rarely-used "print invoice as fax" feature** (yes, an old legacy feature almost nobody uses anymore).

- **Severity:** High — it's a full crash (500 error), which is technically a serious failure.
- **Priority:** Low (P3/P4) — because almost no users use this feature, it doesn't affect the business, revenue, or daily operations. The team can safely postpone the fix.

**Reverse example — Low Severity but High Priority:**

Now imagine a **typo appears on the company CEO's personal dashboard homepage**, visible every time they log in.

- **Severity:** Low — it's just a cosmetic text issue; nothing is broken functionally.
- **Priority:** High (P1/P2) — because it's highly visible to a key stakeholder, and the business wants it fixed immediately to avoid embarrassment or complaints, even though it causes zero technical harm.

**Takeaway for freshers:** Never assume severity and priority are always the same. Always ask two separate questions when triaging a bug: *"How badly is it broken?"* (severity) and *"How urgently must someone act on it?"* (priority). A good QA report should have both fields filled in independently, with clear justification for each.
