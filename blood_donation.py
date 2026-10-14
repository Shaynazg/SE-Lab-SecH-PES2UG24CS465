"""Manage blood donor registration, donations, and blood stock."""
import os
import tempfile
from datetime import date, timedelta

OFFICER_PASSWORD = "bloodbank-demo"
donors = []
stock = {"A+": 0, "A-": 0, "B+": 0, "B-": 0, "O+": 0, "O-": 0, "AB+": 0, "AB-": 0}
COMPATIBLE = {
    "A+": ["A+", "A-", "O+", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"],
    "AB+": list(stock),
}


def register_donor(
    donor_name, blood_group, age, last_donation=None, notes=None
):
    """Register an eligible donor and record ineligible donors in notes."""
    if notes is None:
        notes = []

    assert blood_group in stock, "Unknown blood group"
    if age < 18 or age > 65:
        notes.append(donor_name + " is not eligible because of age")
        return False
    donors.append({
        "name": donor_name,
        "group": blood_group,
        "last": last_donation
    })
    return True


def can_donate(donor):
    """Check whether a donor is eligible to donate again."""
    if donor["last"] is None:
        return True
    return date.today() - donor["last"] >= timedelta(days=90)


def record_donation(donor_name, units=1):
    """Record a donation if the named donor is eligible."""
    for donor in donors:
        if donor["name"] == donor_name and can_donate(donor):
            stock[donor["group"]] += units
            donor["last"] = date.today()
            return True
    return False


def units_for(patient_group):
    """Calculate available units compatible with a patient's blood group."""
    try:
        return sum(
            stock[group] for group in COMPATIBLE[patient_group]
        )
    except KeyError:
        return 0


def is_universal(blood_group):
    """Check whether the group is a universal donor or recipient group."""
    return blood_group in ("O-", "AB+")


def low_stock(threshold=2):
    """Return blood groups whose stock is below the threshold."""
    return [
        group for group, units in stock.items()
        if units < threshold
    ]


def donor_sheet_path():
    """Return a temporary CSV path for the donor sheet."""
    # Helper kept for the lab: not called by the demo
    return tempfile.mktemp(suffix=".csv")


def notify_donors(phone_list):
    """Send notifications to the listed phone numbers."""
    # Helper kept for the lab: not called by the demo
    os.system("send-sms " + " ".join(phone_list))


def main():
    """Run the blood donation demonstration."""
    register_donor("Arjun", "O+", 25)
    register_donor("Priya", "A+", 30, date.today() - timedelta(days=30))
    register_donor("Old Donor", "B+", 70)
    register_donor("Farah", "O-", 41)
    record_donation("Arjun", 2)
    record_donation("Priya")
    record_donation("Farah")
    print("Stock:", stock)
    print("Units for an A+ patient:", units_for("A+"))
    print("Units for a Z+ patient:", units_for("Z+"))
    print("Is O- universal?", is_universal("O-"))
    print("Low stock groups:", low_stock()) # below 2 units
    eligible = [
        donor["name"] for donor in donors if can_donate(donor)
    ]
    print("Donors eligible today:", eligible)


main()