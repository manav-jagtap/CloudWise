import pandas as pd
from django.shortcuts import render

from normalizers.offline import normalize_offline_data
from normalizers.azure import normalize_azure_data
from normalizers.aws import normalize_aws_data
from normalizers.gcp import normalize_gcp_data

from analysis.optimization_engine import analyze_cloud_data


def home(request):

    selected_provider = None
    selected_provider_name = None

    resources = []
    total_current_cost = 0
    total_potential_saving = 0
    optimized_cost = 0
    saving_percentage = 0
    error_message = None

    provider_names = {
        "offline": "Offline / Manual Data",
        "azure": "Microsoft Azure",
        "aws": "Amazon Web Services (AWS)",
        "gcp": "Google Cloud Platform (GCP)",
    }

    if request.method == "POST" and request.FILES.get("cloud_file"):

        selected_provider = request.POST.get("provider")

        selected_provider_name = provider_names.get(
            selected_provider,
            selected_provider
        )

        uploaded_file = request.FILES["cloud_file"]

        try:

            file_name = uploaded_file.name.lower()

            # Read uploaded file according to format
            if file_name.endswith(".csv"):
                data = pd.read_csv(uploaded_file)

            elif file_name.endswith(".json"):
                data = pd.read_json(uploaded_file)

            elif file_name.endswith(".parquet"):
                data = pd.read_parquet(uploaded_file)

            else:
                error_message = (
                    "Unsupported file format. "
                    "Please upload CSV, JSON, or Parquet."
                )
                data = None

            if data is not None:

                # Normalize provider-specific data
                if selected_provider == "offline":
                    data = normalize_offline_data(data)

                elif selected_provider == "azure":
                    data = normalize_azure_data(data)

                elif selected_provider == "aws":
                    data = normalize_aws_data(data)

                elif selected_provider == "gcp":
                    data = normalize_gcp_data(data)

                else:
                    raise ValueError(
                        "Please select a valid data source."
                    )

                # Send normalized data to optimization engine
                analysis_result = analyze_cloud_data(data)

                resources = analysis_result["resources"]
                total_current_cost = analysis_result["total_cost"]
                total_potential_saving = analysis_result["potential_saving"]
                optimized_cost = analysis_result["optimized_cost"]
                saving_percentage = analysis_result["saving_percentage"]

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
        "saving_percentage": saving_percentage,
        "error_message": error_message,
        "selected_provider": selected_provider,
        "selected_provider_name": selected_provider_name,
    }

    return render(
        request,
        "dashboard/home.html",
        context
    )