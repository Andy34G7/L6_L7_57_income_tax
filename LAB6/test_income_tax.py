# SRN: PES2UG24CS061
# Student: Andey Hemanth
# Lab 6: Code and Branch Coverage Test Suite

import pytest
from income_tax import taxable_income, tax_due, refund_status

# ==============================================================================
# 1. Tests for taxable_income(gross, regime, investments)
# ==============================================================================

def test_taxable_income_negative_gross():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)

def test_taxable_income_new_regime_positive():
    assert taxable_income(500000, "new", 0) == 425000

def test_taxable_income_new_regime_negative_result():
    assert taxable_income(50000, "new", 0) == 0

def test_taxable_income_old_regime_investment_capped():
    assert taxable_income(800000, "old", 200000) == 600000

def test_taxable_income_old_regime_investment_within_limit():
    assert taxable_income(800000, "old", 100000) == 650000

def test_taxable_income_old_regime_investment_boundary():
    assert taxable_income(800000, "old", 150000) == 600000

def test_taxable_income_unknown_regime():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "corporate", 0)

# ==============================================================================
# 2. Tests for tax_due(taxable, age)
# ==============================================================================

def test_tax_due_negative_taxable():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-100, 35)

def test_tax_due_super_senior_exempt():
    assert tax_due(500000, 80) == 0

def test_tax_due_super_senior_above_exempt_low_slab():
    assert tax_due(600000, 85) == 5000

def test_tax_due_senior_exempt():
    assert tax_due(300000, 60) == 0

def test_tax_due_senior_above_exempt():
    assert tax_due(450000, 65) == 7500

def test_tax_due_regular_exempt():
    assert tax_due(250000, 59) == 0

def test_tax_due_regular_low_slab():
    assert tax_due(500000, 30) == 12500

def test_tax_due_regular_high_slab():
    assert tax_due(600000, 30) == 32500

# ==============================================================================
# 3. Tests for refund_status(tax_paid, tax_due_amount, filed_on_time)
# ==============================================================================

def test_refund_status_excess_paid_on_time():
    assert refund_status(60000, 50000, True) == "refund"

def test_refund_status_excess_paid_late():
    assert refund_status(60000, 50000, False) == "refund delayed"

def test_refund_status_deficit_on_time():
    assert refund_status(40000, 50000, True) == "pay balance"

def test_refund_status_deficit_late():
    assert refund_status(40000, 50000, False) == "pay balance with penalty"

def test_refund_status_exact_match():
    assert refund_status(50000, 50000, True) == "settled"
