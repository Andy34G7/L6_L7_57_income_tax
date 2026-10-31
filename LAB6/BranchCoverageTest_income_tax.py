import pytest
from income_tax import taxable_income, tax_due, refund_status

# Student Details:
# Name: Andey Hemanth
# SRN: PES2UG24CS061
# Lab 6: Branch Coverage Test Cases (100% Branch & Decision Coverage)

# ==============================================================================
# 1. Tests for taxable_income(gross, regime, investments)
# Decisions & Branches:
#   - gross < 0: True / False
#   - regime == "new": True / False
#   - regime == "old": True / False (else -> raise ValueError)
#   - investments > 150000: True / False
#   - taxable < 0: True / False
# ==============================================================================

def test_taxable_income_negative_gross():
    """Branch: gross < 0 is True -> ValueError('invalid income')."""
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)

def test_taxable_income_new_regime_positive():
    """Branches: gross < 0 is False; regime == 'new' is True; taxable < 0 is False."""
    # deduction = 75000; taxable = 500000 - 75000 = 425000
    assert taxable_income(500000, "new", 0) == 425000

def test_taxable_income_new_regime_zero_or_negative_result():
    """Branch: taxable < 0 is True -> returns 0."""
    # deduction = 75000; 50000 - 75000 = -25000 < 0 -> returns 0
    assert taxable_income(50000, "new", 0) == 0

def test_taxable_income_old_regime_investment_capped():
    """Branch: regime == 'old' is True; investments > 150000 is True (capped to 150000)."""
    # investments capped at 150000 -> deduction = 50000 + 150000 = 200000
    assert taxable_income(800000, "old", 200000) == 600000

def test_taxable_income_old_regime_investment_within_limit():
    """Branch: regime == 'old' is True; investments > 150000 is False."""
    # investments = 100000 -> deduction = 50000 + 100000 = 150000
    assert taxable_income(800000, "old", 100000) == 650000

def test_taxable_income_old_regime_investment_boundary():
    """Branch boundary: investments == 150000."""
    assert taxable_income(800000, "old", 150000) == 600000

def test_taxable_income_unknown_regime():
    """Branch: regime not in ('new', 'old') -> ValueError('unknown regime')."""
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "corporate", 0)


# ==============================================================================
# 2. Tests for tax_due(taxable, age)
# Decisions & Branches:
#   - taxable < 0: True / False
#   - age >= 80: True / False
#   - age >= 60: True / False (else -> age < 60)
#   - taxable <= exempt: True / False
#   - slab <= 250000: True / False
# ==============================================================================

def test_tax_due_negative_taxable():
    """Branch: taxable < 0 is True -> ValueError('invalid amount')."""
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-100, 35)

def test_tax_due_super_senior_exempt():
    """Branch: age >= 80 is True (boundary 80); taxable <= exempt (500000)."""
    assert tax_due(500000, 80) == 0

def test_tax_due_super_senior_above_exempt_low_slab():
    """Branch: age >= 80 (85); slab (100000) <= 250000."""
    # exempt = 500000; slab = 600000 - 500000 = 100000 -> 100000 * 5 // 100 = 5000
    assert tax_due(600000, 85) == 5000

def test_tax_due_senior_exempt():
    """Branch: age >= 60 is True (boundary 60); taxable <= exempt (300000)."""
    assert tax_due(300000, 60) == 0

def test_tax_due_senior_above_exempt():
    """Branch: age >= 60 is True (65); slab (150000) <= 250000."""
    # exempt = 300000; slab = 450000 - 300000 = 150000 -> 150000 * 5 // 100 = 7500
    assert tax_due(450000, 65) == 7500

def test_tax_due_regular_exempt():
    """Branch: age < 60 (59, boundary); taxable <= exempt (250000)."""
    assert tax_due(250000, 59) == 0

def test_tax_due_regular_low_slab():
    """Branch: age < 60 (30); slab == 250000 (boundary)."""
    # exempt = 250000; taxable = 500000; slab = 250000 -> 250000 * 5 // 100 = 12500
    assert tax_due(500000, 30) == 12500

def test_tax_due_regular_high_slab():
    """Branch: age < 60 (30); slab > 250000."""
    # exempt = 250000; taxable = 600000; slab = 350000 -> 12500 + 100000 * 20 // 100 = 32500
    assert tax_due(600000, 30) == 32500


# ==============================================================================
# 3. Tests for refund_status(tax_paid, tax_due_amount, filed_on_time)
# Decisions & Branches:
#   - difference > 0: True (with filed_on_time True / False) / False
#   - difference < 0: True (with filed_on_time True / False) / False
#   - difference == 0: settled
# ==============================================================================

def test_refund_status_excess_paid_on_time():
    """Branch: difference > 0 is True; filed_on_time is True -> 'refund'."""
    assert refund_status(60000, 50000, True) == "refund"

def test_refund_status_excess_paid_late():
    """Branch: difference > 0 is True; filed_on_time is False -> 'refund delayed'."""
    assert refund_status(60000, 50000, False) == "refund delayed"

def test_refund_status_deficit_on_time():
    """Branch: difference < 0 is True; filed_on_time is True -> 'pay balance'."""
    assert refund_status(40000, 50000, True) == "pay balance"

def test_refund_status_deficit_late():
    """Branch: difference < 0 is True; filed_on_time is False -> 'pay balance with penalty'."""
    assert refund_status(40000, 50000, False) == "pay balance with penalty"

def test_refund_status_exact_match():
    """Branch: difference == 0 -> 'settled'."""
    assert refund_status(50000, 50000, True) == "settled"
