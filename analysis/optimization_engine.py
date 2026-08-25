def analyze_resource(row):
    monthly_cost = row["Monthly_Cost"]

    # 1. Potentially Idle
    if row["Avg_CPU"] < 5 and row["Avg_RAM"] < 10:
        status = "POTENTIALLY IDLE"
        recommendation = "Review resource for shutdown"
        estimated_saving = monthly_cost

    # 2. Underutilized
    elif row["Avg_CPU"] < 20 and row["Avg_RAM"] < 30:
        status = "UNDERUTILIZED"
        recommendation = "Review resource for rightsizing"
        estimated_saving = monthly_cost * 0.40

    # 3. Overutilized
    elif row["Avg_CPU"] >= 70 or row["Avg_RAM"] >= 80:
        status = "OVERUTILIZED"
        recommendation = (
            "Review performance and consider possible upsizing"
        )
        estimated_saving = 0

    # 4. Normal
    else:
        status = "NORMAL"
        recommendation = "No optimization required"
        estimated_saving = 0

    return {
        "status": status,
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

        resources.append({
            "id": row["Resource_ID"],
            "provider": row["Provider"],
            "type": row["Resource_Type"],
            "cpu": row["Avg_CPU"],
            "ram": row["Avg_RAM"],
            "cost": row["Monthly_Cost"],
            "currency": row["Currency"],
            "status": result["status"],
            "saving": result["estimated_saving"],
            "recommendation": result["recommendation"],
        })

    optimized_cost = (
        total_current_cost - total_potential_saving
    )

    if total_current_cost > 0:
        saving_percentage = (
            total_potential_saving / total_current_cost
        ) * 100
    else:
        saving_percentage = 0

    return {
        "resources": resources,
        "total_cost": total_current_cost,
        "potential_saving": total_potential_saving,
        "optimized_cost": optimized_cost,
        "saving_percentage": round(saving_percentage, 2),
    }