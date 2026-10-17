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
// ============================================================== (LAB 04)
# Lab 04 - Proving the tests can fail
I changed the / to * in pct() and ran the tests:
3 failed, 25 passed

After undoing the change:
28 passed

## Which double is which
- Stub: fixed_now in tests/test_add_mark.py. It always returns the same time,
  so the expected "at" value is known.
- Fake: the state fixture in tests/conftest.py. It is a plain dict that works
  like the real gradebook. The files in tests/test_storage.py are real files
  in tmp_path.
- Mock: Mock() passed as save in tests/test_add_mark.py. It records the call,
  so the tests can check "called once" and "not called".

## Why I did not mock pct() or the file in Task 5
- pct() is plain logic inside my own program. I can call it directly, and
  mocking it would hide the very calculation under test.
- tmp_path gives a real, empty file for each test. Testing load() and save()
  against it checks what really happens (JSON written and read back, a
  missing file, a corrupt file). A mock would only check that I called open.