# Lab 6 - Code and Branch Coverage Analysis Report

**Student Name:** Andey Hemanth  
**SRN:** PES2UG24CS061  
**Course:** Software Engineering (UE24CS351A)  
**Lab Assignment:** Lab 6 — Code and Branch Coverage Analysis  
**Target Module:** `LAB6/income_tax.py`

---

## 1. Objective

The objective of this lab is to measure and improve test coverage for an income tax calculation module.
We use `pytest` and `coverage` to perform two levels of analysis:
- **Code Coverage (Line Coverage):** Measure the percentage of source statements executed by tests.
- **Branch Coverage:** Measure the percentage of control-flow branches (decision outcomes) executed by tests.

---

## 2. Initial Baseline Analysis

We evaluated the initial test file (`test_income_tax.py`) against `income_tax.py`:

```
Name                 Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------
income_tax.py           39     24     28      7    33%   3, 6-11, 14, 20, 22, 24, 29-32, 36-45
test_income_tax.py       6      0      0      0   100%
----------------------------------------------------------------
TOTAL                   45     24     28      7    38%
```

### Initial Observations
- Only **38%** of statements in `income_tax.py` were executed.
- Only **33%** of branches were evaluated.
- Missing lines included input validation, senior citizen tax slabs, and all refund logic.

---

## 3. Code Coverage (Line Coverage) Analysis

We created `CodeCoverageTest_income_tax.py` to target statement coverage.
The test suite contains 15 unit tests that execute each function statement at least once.

### Execution Command
```bash
coverage run -m pytest CodeCoverageTest_income_tax.py
coverage report -m
```

### Results
```
Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
CodeCoverageTest_income_tax.py      35      0   100%
income_tax.py                       39      0   100%
--------------------------------------------------------------
TOTAL                               74      0   100%
```

- **Statement Coverage Achieved:** **100%** (39 / 39 statements in `income_tax.py`).
- **Test Results:** 15 passed in 0.04s.
- **Screenshot:** Saved as `code_coverage_screenshot.png`.

### Key Limitation of Line Coverage
Line coverage asks only if execution reached a line.
When we test line 8 (`investments = 150000`) with an investment of 200,000, line 8 executes.
However, this test never evaluates the condition when `investments <= 150000`.
Running branch analysis on this suite reveals:
```
income_tax.py      39      0     28      1    99%   7->9
```
Branch `7->9` remains untested. This confirms that 100% line coverage does not ensure complete testing.

---

## 4. Branch Coverage Analysis

We created `BranchCoverageTest_income_tax.py` to evaluate every logical decision path.
The test suite contains 20 comprehensive unit tests that test both `True` and `False` outcomes for all 28 branches.

### Execution Command
```bash
coverage run --branch -m pytest BranchCoverageTest_income_tax.py
coverage report -m
```

### Results
```
Name                               Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------------------
BranchCoverageTest_income_tax.py      45      0      0      0   100%
income_tax.py                         39      0     28      0   100%
------------------------------------------------------------------------------
TOTAL                                 84      0     28      0   100%
```

- **Branch Coverage Achieved:** **100%** (28 / 28 branches in `income_tax.py`).
- **Statement Coverage Achieved:** **100%** (39 / 39 statements in `income_tax.py`).
- **Test Results:** 20 passed in 0.04s.
- **Screenshot:** Saved as `branch_coverage_screenshot.png`.

---

## 5. Decision and Branch Mapping

The table below lists all decision points in `income_tax.py` and the corresponding tests in `BranchCoverageTest_income_tax.py`:

| Function | Decision Condition | True Path Test | False Path Test |
| :--- | :--- | :--- | :--- |
| `taxable_income` | `gross < 0` | `test_taxable_income_negative_gross` | `test_taxable_income_new_regime_positive` |
| `taxable_income` | `regime == "new"` | `test_taxable_income_new_regime_positive` | `test_taxable_income_old_regime_investment_within_limit` |
| `taxable_income` | `regime == "old"` | `test_taxable_income_old_regime_investment_within_limit` | `test_taxable_income_unknown_regime` |
| `taxable_income` | `investments > 150000` | `test_taxable_income_old_regime_investment_capped` | `test_taxable_income_old_regime_investment_within_limit` |
| `taxable_income` | `taxable < 0` | `test_taxable_income_new_regime_zero_or_negative_result` | `test_taxable_income_new_regime_positive` |
| `tax_due` | `taxable < 0` | `test_tax_due_negative_taxable` | `test_tax_due_regular_exempt` |
| `tax_due` | `age >= 80` | `test_tax_due_super_senior_above_exempt_low_slab` | `test_tax_due_senior_above_exempt` |
| `tax_due` | `age >= 60` | `test_tax_due_senior_above_exempt` | `test_tax_due_regular_low_slab` |
| `tax_due` | `taxable <= exempt` | `test_tax_due_regular_exempt` | `test_tax_due_regular_low_slab` |
| `tax_due` | `slab <= 250000` | `test_tax_due_regular_low_slab` | `test_tax_due_regular_high_slab` |
| `refund_status` | `difference > 0` | `test_refund_status_excess_paid_on_time` | `test_refund_status_deficit_on_time` |
| `refund_status` | `difference > 0` (on time) | `test_refund_status_excess_paid_on_time` | `test_refund_status_excess_paid_late` |
| `refund_status` | `difference < 0` | `test_refund_status_deficit_on_time` | `test_refund_status_exact_match` |
| `refund_status` | `difference < 0` (on time) | `test_refund_status_deficit_on_time` | `test_refund_status_deficit_late` |

---

## 6. Conclusion and Takeaways

1. **Line coverage detects dead code:** Line coverage ensures that execution reaches every statement. It helps eliminate unreached functions or blocks.
2. **Branch coverage verifies program logic:** Line coverage can be 100% while critical logical paths remain unexecuted. Branch coverage tests all control outcomes.
3. **Boundary values matter:** Testing boundary values (such as `age=60`, `age=80`, `investments=150000`, and `taxable=exempt`) ensures that inequality operators (`>=`, `<=`) behave as expected.
4. **Summary:** Both test suites achieved their targets (>90% threshold), with final branch coverage reaching 100%.
