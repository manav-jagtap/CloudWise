import pandas as pd
from django.shortcuts import render


def home(request):

    resources = []
    total_current_cost = 0
    total_potential_saving = 0
    optimized_cost = 0
    saving_percentage = 0
    error_message = None

    if request.method == "POST" and request.FILES.get("cloud_file"):

        uploaded_file = request.FILES["cloud_file"]

        try:
            file_name = uploaded_file.name.lower()

            # Detect file format
            if file_name.endswith(".csv"):
                data = pd.read_csv(uploaded_file)

            elif file_name.endswith(".json"):
                data = pd.read_json(uploaded_file)

            elif file_name.endswith(".parquet"):
                data = pd.read_parquet(uploaded_file)

            else:
                error_message = (
                    "Unsupported file format. "
                    "Please upload a CSV, JSON or Parquet file."
                )
                data = None
                
            if data is not None:

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

                missing_columns = [
                    column
                    for column in required_columns
                    if column not in data.columns
                ]

                if missing_columns:

                    error_message = (
                        "Missing required columns: "
                        + ", ".join(missing_columns)
                    )

                else:

                    total_current_cost = data["Monthly_Cost"].sum()

                    for index, row in data.iterrows():

                        monthly_cost = row["Monthly_Cost"]

                        # Potentially Idle
                        if row["Avg_CPU"] < 5 and row["Avg_RAM"] < 10:
                            status = "POTENTIALLY IDLE"
                            recommendation = "Review resource for shutdown"
                            estimated_saving = monthly_cost

                        # Underutilized
                        elif row["Avg_CPU"] < 20 and row["Avg_RAM"] < 30:
                            status = "UNDERUTILIZED"
                            recommendation = "Review resource for rightsizing"
                            estimated_saving = monthly_cost * 0.40

                        # Overutilized
                        elif row["Avg_CPU"] >= 70 or row["Avg_RAM"] >= 80:
                            status = "OVERUTILIZED"
                            recommendation = (
                                "Review performance and consider possible upsizing"
                            )
                            estimated_saving = 0

                        # Normal
                        else:
                            status = "NORMAL"
                            recommendation = "No optimization required"
                            estimated_saving = 0

                        total_potential_saving += estimated_saving

                        resources.append({
                            "id": row["Resource_ID"],
                            "cpu": row["Avg_CPU"],
                            "ram": row["Avg_RAM"],
                            "cost": monthly_cost,
                            "status": status,
                            "saving": estimated_saving,
                            "recommendation": recommendation,
                        })

                    optimized_cost = (
                        total_current_cost
                        - total_potential_saving
                    )

                    if total_current_cost > 0:
                        saving_percentage = (
                            total_potential_saving
                            / total_current_cost
                        ) * 100

        except Exception as error:

            error_message = (
                "Unable to analyze uploaded file: "
                + str(error)
            )

    context = {
        "resources": resources,
        "total_cost": total_current_cost,
        "potential_saving": total_potential_saving,
        "optimized_cost": optimized_cost,
        "saving_percentage": round(saving_percentage, 2),
        "error_message": error_message,
    }

    return render(
        request,
        "dashboard/home.html",
        context
    )