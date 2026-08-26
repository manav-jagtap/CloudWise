import pandas as pd


# CloudWise common data structure
CLOUDWISE_COLUMNS = [
    "Provider",
    "Resource_ID",
    "Resource_Type",
    "vCPU",
    "RAM_GB",
    "Avg_CPU",
    "Peak_CPU",
    "Avg_RAM",
    "Runtime_Hours",
    "Monthly_Cost",
    "Currency",
]


def normalize_offline_data(data):

    # Work on a copy so original uploaded data is not modified
    normalized_data = data.copy()

    # Add provider information
    normalized_data["Provider"] = "Offline"

    # Add default currency if not supplied
    if "Currency" not in normalized_data.columns:
        normalized_data["Currency"] = "INR"

    # Required columns for resource analysis
    required_columns = [
        "Resource_ID",
        "Resource_Type",
        "vCPU",
        "RAM_GB",
        "Avg_CPU",
        "Peak_CPU",
        "Avg_RAM",
        "Runtime_Hours",
        "Monthly_Cost",
    ]

    # Find missing columns
    missing_columns = [
        column
        for column in required_columns
        if column not in normalized_data.columns
    ]

    # Stop normalization if important data is missing
    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    # Return data in CloudWise common format
    normalized_data = normalized_data[CLOUDWISE_COLUMNS]

    return normalized_data