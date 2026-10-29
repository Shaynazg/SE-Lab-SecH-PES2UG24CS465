
import pytest
from airline_baggage import (
    baggage_fee,
    carry_on_ok,
    check_in_status,
)


# Baggage fee: validation and allowance branches

def test_unknown_cabin():
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee("first", 10, "domestic", False)


def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        baggage_fee("economy", -1, "domestic", False)


def test_non_member_within_allowance():
    assert baggage_fee("economy", 15, "domestic", False) == 0


def test_member_extra_allowance():
    assert baggage_fee("economy", 25, "domestic", True) == 0


def test_business_member_no_extra_allowance():
    assert baggage_fee("business", 40, "domestic", True) == 0


# Baggage fee: excess and route branches

def test_domestic_route():
    assert baggage_fee("economy", 20, "domestic", False) == 100


def test_non_domestic_route():
    assert baggage_fee("economy", 20, "international", False) == 225


def test_excess_exactly_twenty_does_not_double_rate():
    assert baggage_fee("economy", 35, "domestic", False) == 400


def test_excess_over_twenty_doubles_domestic_rate():
    assert baggage_fee("economy", 40, "domestic", False) == 1000


def test_excess_over_twenty_international_surcharge():
    assert baggage_fee("economy", 40, "international", False) == 2500


def test_excess_over_twenty_other_route():
    assert baggage_fee("economy", 40, "other", False) == 2250


# Carry-on branches

def test_infant_allowed_with_two_items():
    assert carry_on_ok(10, 2, True) is True


def test_infant_rejected_with_more_than_two_items():
    assert carry_on_ok(5, 3, True) is False


def test_non_infant_rejected_over_seven_kg():
    assert carry_on_ok(8, 1, False) is False


def test_non_infant_allowed_at_seven_kg():
    assert carry_on_ok(7, 1, False) is True


def test_non_infant_rejected_with_two_items():
    assert carry_on_ok(5, 2, False) is False


# Check-in branches

def test_domestic_baggage_open():
    assert check_in_status(60, True, False) == "open"


def test_domestic_baggage_late():
    assert check_in_status(45, True, False) == "late"


def test_domestic_baggage_closed():
    assert check_in_status(44, True, False) == "closed"


def test_domestic_no_baggage_open():
    assert check_in_status(45, False, False) == "open"


def test_domestic_no_baggage_late():
    assert check_in_status(30, False, False) == "late"


def test_domestic_no_baggage_closed():
    assert check_in_status(29, False, False) == "closed"


def test_international_open():
    assert check_in_status(105, False, True) == "open"


def test_international_late():
    assert check_in_status(90, False, True) == "late"


def test_international_closed():
    assert check_in_status(89, False, True) == "closed"
