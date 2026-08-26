def normalize_azure_data(data):

    normalized_data = data.copy()

    # Map Azure-style columns to CloudWise common columns
    normalized_data = normalized_data.rename(columns={
        "ResourceId": "Resource_ID",
        "ResourceType": "Resource_Type",
        "VCpu": "vCPU",
        "RamGB": "RAM_GB",
        "AverageCpu": "Avg_CPU",
        "PeakCpu": "Peak_CPU",
        "AverageMemory": "Avg_RAM",
        "RuntimeHours": "Runtime_Hours",
        "CostInBillingCurrency": "Monthly_Cost",
        "BillingCurrency": "Currency",
    })

    # Add provider name
    normalized_data["Provider"] = "Azure"

    required_columns = [
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

    missing_columns = [
        column
        for column in required_columns
        if column not in normalized_data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required Azure columns after normalization: "
            + ", ".join(missing_columns)
        )

    return normalized_data[required_columns]