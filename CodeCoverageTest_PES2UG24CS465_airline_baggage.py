
import pytest
from airline_baggage import (
    baggage_fee,
    carry_on_ok,
    check_in_status,
)


# Baggage fee tests

def test_invalid_cabin():
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee("first", 10, "domestic", False)


def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        baggage_fee("economy", -1, "domestic", False)


def test_within_free_allowance():
    assert baggage_fee("economy", 10, "domestic", False) == 0


def test_exact_free_allowance():
    assert baggage_fee("economy", 15, "domestic", False) == 0


def test_member_economy_allowance():
    assert baggage_fee("economy", 25, "domestic", True) == 0


def test_member_premium_allowance():
    assert baggage_fee("premium", 35, "domestic", True) == 0


def test_business_member_gets_no_extra_allowance():
    assert baggage_fee("business", 40, "domestic", True) == 0


def test_domestic_fee():
    assert baggage_fee("economy", 20, "domestic", False) == 100


def test_international_fee():
    assert baggage_fee("economy", 20, "international", False) == 225


def test_high_excess_domestic_fee():
    assert baggage_fee("economy", 40, "domestic", False) == 1000


def test_high_excess_international_fee():
    assert baggage_fee("economy", 40, "international", False) == 2500


def test_high_excess_non_international_route():
    assert baggage_fee("economy", 40, "other", False) == 2250


# Carry-on tests

def test_infant_with_two_items():
    assert carry_on_ok(10, 2, True) is True


def test_infant_with_more_than_two_items():
    assert carry_on_ok(5, 3, True) is False


def test_non_infant_over_weight_limit():
    assert carry_on_ok(8, 1, False) is False


def test_non_infant_at_weight_limit():
    assert carry_on_ok(7, 1, False) is True


def test_non_infant_with_too_many_items():
    assert carry_on_ok(5, 2, False) is False


def test_non_infant_with_zero_items():
    assert carry_on_ok(5, 0, False) is True


# Check-in status tests

def test_checkin_open_with_baggage():
    assert check_in_status(60, True, False) == "open"


def test_checkin_late_with_baggage():
    assert check_in_status(45, True, False) == "late"


def test_checkin_closed_with_baggage():
    assert check_in_status(44, True, False) == "closed"


def test_checkin_open_without_baggage():
    assert check_in_status(45, False, False) == "open"


def test_checkin_late_without_baggage():
    assert check_in_status(30, False, False) == "late"


def test_checkin_closed_without_baggage():
    assert check_in_status(29, False, False) == "closed"


def test_checkin_open_international():
    assert check_in_status(120, False, True) == "open"



def test_checkin_late_international():
    assert check_in_status(90, False, True) == "late"


def test_checkin_closed_international():
    assert check_in_status(89, False, True) == "closed"
