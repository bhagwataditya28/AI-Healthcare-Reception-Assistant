import os
import pandas as pd
from datetime import datetime

DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "enquiries.csv")

COLUMNS = [
    "timestamp",
    "enquiry",
    "category",
    "intent",
    "response",
    "requires_human_review",
    "reason"
]


def initialize_data():
    """Create the data directory and CSV file if needed."""
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(CSV_FILE):
        pd.DataFrame(columns=COLUMNS).to_csv(CSV_FILE, index=False)


def save_enquiry(enquiry: str, result: dict):
    """Save an enquiry and its AI analysis to CSV."""

    initialize_data()

    new_record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "enquiry": enquiry,
        "category": result.get("category", ""),
        "intent": result.get("intent", ""),
        "response": result.get("response", ""),
        "requires_human_review": result.get(
            "requires_human_review", True
        ),
        "reason": result.get("reason", "")
    }

    df = pd.DataFrame([new_record])
    df.to_csv(CSV_FILE, mode="a", header=False, index=False)


def get_all_enquiries():
    """Return all saved enquiry records."""

    initialize_data()
    return pd.read_csv(CSV_FILE)


def get_enquiry_count():
    """Return the total number of saved enquiries."""

    return len(get_all_enquiries())