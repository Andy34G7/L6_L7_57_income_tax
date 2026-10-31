# L6_L7_57 — Income Tax Calculator

**Lab 6: Code and Branch Coverage Analysis**  
**Student:** Andey Hemanth (PES2UG24CS061)

## Overview

This repository contains the income tax calculation module and comprehensive test suites for Lab 6.
We measure and verify both code coverage (line coverage) and branch coverage.

## Project Structure

```
LAB6/
├── income_tax.py                    # Application under test
├── test_income_tax.py               # Main test suite (20 tests, 100% branch coverage)
├── CodeCoverageTest_income_tax.py   # Code coverage test suite (15 tests, 100% line coverage)
├── BranchCoverageTest_income_tax.py # Branch coverage test suite (20 tests, 100% branch coverage)
├── code_coverage_screenshot.png     # Terminal screenshot for code coverage
├── branch_coverage_screenshot.png   # Terminal screenshot for branch coverage
├── report.md                        # Detailed analysis report
└── README.md                        # Documentation
```

## Running the Tests and Coverage

### 1. Code Coverage (Line Coverage)
```bash
coverage run -m pytest CodeCoverageTest_income_tax.py
coverage report -m
```
- **Line Coverage:** 100% (39/39 statements)

### 2. Branch Coverage
```bash
coverage run --branch -m pytest BranchCoverageTest_income_tax.py
coverage report -m
```
- **Branch Coverage:** 100% (28/28 branches, 39/39 statements)

### 3. Running All Tests with Pytest
```bash
pytest test_income_tax.py -v
```
