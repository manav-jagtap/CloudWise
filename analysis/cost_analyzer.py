import pandas as pd

# Read cloud resource dataset
data = pd.read_csv("data/cloud_resources.csv")

print("===== CLOUDWISE RESOURCE DATA =====")
print(data)

print("\n===== CLOUDWISE ANALYSIS =====")

total_potential_saving = 0
total_current_cost = data["Monthly_Cost"].sum()

report_data = []

for index, row in data.iterrows():

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
        recommendation = "Review performance and consider possible upsizing"
        estimated_saving = 0

    # 4. Normal
    else:
        status = "NORMAL"
        recommendation = "No optimization required"
        estimated_saving = 0

    total_potential_saving += estimated_saving

    print("\nResource:", row["Resource_ID"])
    print("Status:", status)
    print("Monthly Cost: Rs.", monthly_cost)
    print("Recommendation:", recommendation)
    print("Estimated Saving: Rs.", estimated_saving)

    report_data.append({
        "Resource_ID": row["Resource_ID"],
        "Status": status,
        "Monthly_Cost": monthly_cost,
        "Estimated_Saving": estimated_saving,
        "Recommendation": recommendation
    })


# Final calculations
optimized_cost = total_current_cost - total_potential_saving

if total_current_cost > 0:
    saving_percentage = (
        total_potential_saving / total_current_cost
    ) * 100
else:
    saving_percentage = 0


print("\n===== CLOUDWISE SUMMARY =====")
print("Total Current Monthly Cost: Rs.", total_current_cost)
print("Total Potential Monthly Saving: Rs.", total_potential_saving)
print("Estimated Optimized Monthly Cost: Rs.", optimized_cost)
print("Potential Saving Percentage:", round(saving_percentage, 2), "%")


# Create CSV report
report_df = pd.DataFrame(report_data)

report_df.to_csv(
    "results/optimization_report.csv",
    index=False
)

print("\nOptimization report successfully created!")
print("File: results/optimization_report.csv")