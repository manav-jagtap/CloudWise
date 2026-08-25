def normalize_gcp_data(data):

    normalized_data = data.copy()

    normalized_data = normalized_data.rename(columns={
        "resource_name": "Resource_ID",
        "resource_type": "Resource_Type",
        "vcpus": "vCPU",
        "memory_gb": "RAM_GB",
        "avg_cpu_utilization": "Avg_CPU",
        "peak_cpu_utilization": "Peak_CPU",
        "avg_memory_utilization": "Avg_RAM",
        "runtime_hours": "Runtime_Hours",
        "monthly_cost": "Monthly_Cost",
        "currency": "Currency",
    })

    normalized_data["Provider"] = "GCP"

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
            "Missing required GCP columns after normalization: "
            + ", ".join(missing_columns)
        )

    return normalized_data[required_columns]