# Lab 7: Fuzzing for Input Validation Bugs

**Student Name:** Andey Hemanth  
**SRN:** PES2UG24CS061  
**Course:** Software Engineering (UE24CS351A)  
**Lab Assignment:** Lab 7 — Fuzzing for Input Validation Bugs  
**Target Module:** `LAB7/income_tax_parser.py`  
**Test Suite:** `LAB7/test_income_tax_parser.py`

---

## 1. Objective

The objective of this lab is to use fuzz testing to detect and resolve input validation vulnerabilities in `income_tax_parser.py`.
We use the **Hypothesis** property-based testing library with `pytest` to:
- Generate pseudo-random, unexpected, and boundary inputs.
- Expose unhandled exceptions, malformed input crashes, and boundary defects.
- Harden all parser functions using defensive programming patterns.

---

## 2. Test Execution & Screenshots Summary

| Screenshot | Description | Status |
| :--- | :--- | :--- |
| **SS1** (`ss1_buggy_run.png`) | Execution of `income_tax_parser.py` on buggy code with standard inputs. | Normal inputs pass. |
| **SS2** (`ss2_fuzz_failing.png`) | Fuzz test execution (`pytest test_income_tax_parser.py`) on buggy code. | 3 failures detected by Hypothesis. |
| **SS3** (`ss3_fixed_run.png`) | Execution of hardened `income_tax_parser.py` on standard inputs. | Normal inputs pass safely. |
| **SS4** (`ss4_fuzz_passing.png`) | Fuzz test execution (`pytest test_income_tax_parser.py`) on fixed code. | 3 passed (100% fuzz tests passing). |

---

## 3. Reflection Questions (ASD-STE100 to ~80%)

### Question 1: What unexpected inputs caused the initial functions to crash, and what exceptions did they raise?

The initial code assumed that all inputs were non-empty strings with perfect delimiters.
Hypothesis automatically generated failing counterexamples:

1. **`clean_pan(pan)`**:
   - **Input:** `pan = None`
   - **Crash:** `AttributeError: 'NoneType' object has no attribute 'strip'`
2. **`parse_amount(text)`**:
   - **Input:** `text = None`
   - **Crash:** `AttributeError: 'NoneType' object has no attribute 'replace'`
   - **Input:** `text = ""` (empty string)
   - **Crash:** `ValueError: invalid literal for int() with base 10: ''`
3. **`parse_tax_slab(line)`**:
   - **Input:** `line = None`
   - **Crash:** `AttributeError: 'NoneType' object has no attribute 'split'`
   - **Input:** `line = ""` or `line = ":"` (missing colon or dash delimiter)
   - **Crash:** `ValueError: not enough values to unpack (expected 2, got 1)`
   - **Input:** `line = "abc-def:ghi"`
   - **Crash:** `ValueError: invalid literal for int() with base 10: 'abc'`

---

### Question 2: How does property-based fuzz testing with Hypothesis compare to example-based unit testing?

- **Example-based unit testing:**
  The developer tests only explicit values that they anticipate.
  Edge cases (e.g. Unicode surrogates, control characters, empty strings, and type mismatches) are frequently overlooked.
- **Property-based fuzz testing:**
  The developer defines invariants (properties), such as *"the parser must never raise an unhandled exception for any text or None input"*.
  Hypothesis generates hundreds of varied inputs automatically.
  When a test fails, Hypothesis applies **input shrinking** to find the minimal reproducer (such as `None` or `""`), making root-cause analysis fast and deterministic.

---

### Question 3: How did defensive programming resolve these bugs, and how do they apply to production systems?

We applied three core defensive programming practices:

1. **Type Guards:**
   We verified `isinstance(val, str)` before performing string methods. Non-string inputs immediately return safe defaults.
2. **Structural Validation:**
   We verified the presence of required delimiters (`:` and `-`) and verified split counts before unpacking.
3. **Safe Exception Handling & Default Fallbacks:**
   We wrapped `int(...)` conversions in `try-except ValueError` blocks and returned neutral fallbacks (`""`, `0`, or `(0, 0, 0)`).

In production environments, all external inputs are untrusted. Defensive input validation prevents process crashes, unhandled 500 errors, and Denial of Service (DoS) attacks.

---

## 4. Deliverables

- `income_tax_parser.py`: Hardened parser script.
- `test_income_tax_parser.py`: Completed Hypothesis fuzz tests.
- `PES2UG24CS061_Andey_Hemanth_LAB7.pdf`: Formatted report with screenshots SS1–SS4 and reflection responses.
