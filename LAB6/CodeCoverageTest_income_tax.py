import pytest
from income_tax import taxable_income, tax_due, refund_status

# Student Details:
# Name: Andey Hemanth
# SRN: PES2UG24CS061
# Lab 6: Code Coverage Test Cases

def test_taxable_negative_gross():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-100, "new", 0)

def test_taxable_new_regime():
    assert taxable_income(500000, "new", 0) == 425000

def test_taxable_old_regime_capped():
    # Only tests investments > 150000 (executes lines 6, 7, 8, 9)
    # Note: Branch where investments <= 150000 is intentionally left uncovered
    assert taxable_income(600000, "old", 200000) == 400000

def test_taxable_invalid_regime():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "other", 0)

def test_taxable_negative_result():
    assert taxable_income(50000, "new", 0) == 0

def test_tax_due_negative():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-500, 30)

def test_tax_due_super_senior():
    assert tax_due(600000, 85) == 5000

def test_tax_due_senior():
    assert tax_due(400000, 65) == 5000

def test_tax_due_regular_high_slab():
    assert tax_due(600000, 30) == 32500

def test_tax_due_below_exempt():
    assert tax_due(200000, 30) == 0

def test_refund_positive_on_time():
    assert refund_status(50000, 40000, True) == "refund"

def test_refund_positive_delayed():
    assert refund_status(50000, 40000, False) == "refund delayed"

def test_refund_negative_on_time():
    assert refund_status(40000, 50000, True) == "pay balance"

def test_refund_negative_penalty():
    assert refund_status(40000, 50000, False) == "pay balance with penalty"

def test_refund_settled():
    assert refund_status(50000, 50000, True) == "settled"
