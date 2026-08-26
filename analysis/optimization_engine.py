def analyze_resource(row):
    monthly_cost = row["Monthly_Cost"]

    avg_cpu = row["Avg_CPU"]
    peak_cpu = row["Peak_CPU"]
    avg_ram = row["Avg_RAM"]
    runtime_hours = row["Runtime_Hours"]

    # 1. Potentially Idle
    if (
        avg_cpu < 5
        and avg_ram < 10
        and peak_cpu < 20
    ):
        status = "POTENTIALLY IDLE"
        priority = "HIGH"

        if runtime_hours >= 500:
            recommendation = (
                "Resource shows very low utilization for long runtime. "
                "Review whether it can be stopped or decommissioned."
            )
        else:
            recommendation = (
                "Resource shows very low utilization. "
                "Review usage schedule and consider scheduled shutdown."
            )

        estimated_saving = monthly_cost

    # 2. Underutilized
    elif (
        avg_cpu < 20
        and avg_ram < 30
        and peak_cpu < 60
    ):
        status = "UNDERUTILIZED"
        priority = "MEDIUM"

        recommendation = (
            "Resource utilization is consistently low. "
            "Review for rightsizing to a smaller configuration."
        )

        # Prototype saving estimate
        estimated_saving = monthly_cost * 0.40

    # 3. Overutilized
    elif (
        avg_cpu >= 70
        or avg_ram >= 80
        or peak_cpu >= 90
    ):
        status = "OVERUTILIZED"
        priority = "HIGH"

        recommendation = (
            "High resource utilization detected. "
            "Review workload performance and consider scaling or upsizing."
        )

        estimated_saving = 0

    # 4. Normal
    else:
        status = "NORMAL"
        priority = "LOW"

        recommendation = (
            "Resource utilization appears within normal range."
        )

        estimated_saving = 0

    # -----------------------------------
    # CloudWise Priority Score
    # -----------------------------------

    if status == "POTENTIALLY IDLE":

        priority_score = 80

        if monthly_cost >= 10000:
            priority_score += 15

        elif monthly_cost >= 5000:
            priority_score += 10

    elif status == "OVERUTILIZED":

        priority_score = 75

        if avg_cpu >= 90 or avg_ram >= 90:
            priority_score += 15

        elif peak_cpu >= 95:
            priority_score += 10

    elif status == "UNDERUTILIZED":

        priority_score = 50

        if estimated_saving >= 5000:
            priority_score += 15

        elif estimated_saving >= 2000:
            priority_score += 10

    else:

        priority_score = 10

    # Score maximum 100
    priority_score = min(priority_score, 100)

    return {
        "status": status,
        "priority": priority,
        "priority_score": priority_score,
        "recommendation": recommendation,
        "estimated_saving": estimated_saving,
    }


def analyze_cloud_data(data):

    resources = []

    total_potential_saving = 0
    total_current_cost = data["Monthly_Cost"].sum()

    for index, row in data.iterrows():

        result = analyze_resource(row)

        total_potential_saving += result["estimated_saving"]

        # Full resource ID
        resource_id = str(row["Resource_ID"])

        # Short readable resource name
        resource_name = (
            resource_id
            .rstrip("/")
            .split("/")[-1]
        )

        resources.append({
            "id": resource_name,
            "full_id": resource_id,
            "provider": row["Provider"],
            "type": row["Resource_Type"],

            "cpu": row["Avg_CPU"],
            "peak_cpu": row["Peak_CPU"],
            "ram": row["Avg_RAM"],
            "runtime_hours": row["Runtime_Hours"],

            "cost": row["Monthly_Cost"],
            "currency": row["Currency"],

            "status": result["status"],
            "priority": result["priority"],
            "priority_score": result["priority_score"],

            "saving": result["estimated_saving"],
            "recommendation": result["recommendation"],
        })

    # -----------------------------------
    # Final Cost Calculations
    # -----------------------------------

    optimized_cost = (
        total_current_cost
        - total_potential_saving
    )

    if total_current_cost > 0:

        saving_percentage = (
            total_potential_saving
            / total_current_cost
        ) * 100

    else:

        saving_percentage = 0

    # Sort resources by priority score (highest first)
    resources = sorted(
        resources,
        key=lambda resource: resource["priority_score"],
        reverse=True
    )

    # Top 3 optimization opportunities
    top_opportunities = resources[:3]

    return {
        "resources": resources,
        "top_opportunities": top_opportunities,
        "total_cost": total_current_cost,
        "potential_saving": total_potential_saving,
        "optimized_cost": optimized_cost,
        "saving_percentage": round(
            saving_percentage,
            2
        ),
    }