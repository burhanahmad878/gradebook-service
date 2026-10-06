# Task 2 & Task 8: Failure Investigation Notes

## 1. Initial Test Requests Results (Task 2)

- **(a) GET /students/NOPE**
  - **Status:** `200 OK`
  - **Response:** `{"error": "not found"}`

- **(b) POST /students with body "5"**
  - **Status:** Server crashed (`Empty reply from server`).

- **(c) Invalid mark score "abc"**
  - **Status:** `200 OK`
  - **Response:** Accepted string score `"abc"` without validation.

- **(d) Assessment with total "0"**
  - **Status:** `200 OK`
  - **Response:** Created assessment with total "0".

- **(e) POST mark for non-existent assessment**
  - **Status:** `200 OK`
  - **Response:** Created mark for non-existent assessment.

---

## 2. Why deleting gradebook.json was necessary

Deleting `gradebook.json` between tests cleared saved corrupted data from previous tests so that it did not interfere with subsequent test cases.

---

## 3. Bare `except:` Clauses Found (Task 2)

- **Line 19:** In `load()` catching all exceptions during file loading.
- **Line 28:** In `save()` catching all exceptions and passing silently.
- **Line 84:** In POST body parsing catching all JSON decoding errors.

---

## 4. Post-Fix Test Request Results (Task 8)

- **(a) GET /students/NOPE**
  - **Status:** `404 Not Found`
  - **Response:** `{"error": "Student 'NOPE' not found."}`

- **(b) POST /students with body 5**
  - **Status:** `400 Bad Request`
  - **Response:** `{"error": "Payload must be a JSON object."}`

- **(c) POST mark with score "abc"**
  - **Status:** `400 Bad Request`
  - **Response:** `{"error": "Field 'score' must be a valid number."}`

- **(d) POST assessment with total "0"**
  - **Status:** `400 Bad Request`
  - **Response:** `{"error": "Assessment total must be greater than 0."}`

- **(e) POST mark for non-existent assessment**
  - **Status:** `404 Not Found`
  - **Response:** `{"error": "Assessment 'A1' does not exist."}`
