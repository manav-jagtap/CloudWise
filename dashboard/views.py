import pandas as pd
from django.shortcuts import render


def home(request):
    data = pd.read_csv("data/cloud_resources.csv")

    total_current_cost = data["Monthly_Cost"].sum()
    total_potential_saving = 0

    for index, row in data.iterrows():

        monthly_cost = row["Monthly_Cost"]

        if row["Avg_CPU"] < 5 and row["Avg_RAM"] < 10:
            estimated_saving = monthly_cost

        elif row["Avg_CPU"] < 20 and row["Avg_RAM"] < 30:
            estimated_saving = monthly_cost * 0.40

        else:
            estimated_saving = 0

        total_potential_saving += estimated_saving

    optimized_cost = total_current_cost - total_potential_saving

    saving_percentage = (
        total_potential_saving / total_current_cost
    ) * 100

    context = {
        "total_cost": total_current_cost,
        "potential_saving": total_potential_saving,
        "optimized_cost": optimized_cost,
        "saving_percentage": round(saving_percentage, 2),
    }

    return render(request, "dashboard/home.html", context)