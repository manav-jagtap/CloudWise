import csv
import pandas as pd

from django.conf import settings
from django.http import FileResponse, Http404

from django.http import HttpResponse
from django.shortcuts import render

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from normalizers.offline import normalize_offline_data
from normalizers.azure import normalize_azure_data
from normalizers.aws import normalize_aws_data
from normalizers.gcp import normalize_gcp_data

from analysis.optimization_engine import analyze_cloud_data


def home(request):

    resources = []
    top_opportunities = []
    status_counts = {}

    selected_provider = None
    selected_provider_name = None

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

            max_file_size = 10 * 1024 * 1024

            if uploaded_file.size > max_file_size:
                raise ValueError(
                    "File is too large. Maximum allowed size is 10 MB."
                )

            file_name = uploaded_file.name.lower()

            # -----------------------------
            # Read uploaded file
            # -----------------------------

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

            # -----------------------------
            # Normalize provider data
            # -----------------------------

            if data is not None:

                if data.empty:
                    raise ValueError(
                        "Uploaded file is empty."
                    )
                valid_providers = ["offline", "azure", "aws", "gcp"]

                if selected_provider not in valid_providers:
                    raise ValueError(
                        "Please select a valid cloud data source."
                    )

            if data is not None:

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

                # -----------------------------
                # Analyze normalized data
                # -----------------------------

                numeric_columns = [
                    "vCPU",
                    "RAM_GB",
                    "Avg_CPU",
                    "Peak_CPU",
                    "Avg_RAM",
                    "Runtime_Hours",
                    "Monthly_Cost",
                ]

                for column in numeric_columns:
                    data[column] = pd.to_numeric(
                        data[column],
                        errors="coerce"
                    )

                if data[numeric_columns].isnull().any().any():
                    raise ValueError(
                        "Some numeric fields contain invalid or non-numeric values."
                    )

                if (
                        (data["Avg_CPU"] < 0).any()
                        or (data["Avg_CPU"] > 100).any()
                        or (data["Peak_CPU"] < 0).any()
                        or (data["Peak_CPU"] > 100).any()
                        or (data["Avg_RAM"] < 0).any()
                        or (data["Avg_RAM"] > 100).any()
                ):
                    raise ValueError(
                        "CPU and RAM utilization values must be between 0 and 100."
                    )

                if (
                        (data["vCPU"] < 0).any()
                        or (data["RAM_GB"] < 0).any()
                        or (data["Runtime_Hours"] < 0).any()
                        or (data["Monthly_Cost"] < 0).any()
                ):
                    raise ValueError(
                        "vCPU, RAM, runtime hours, and monthly cost cannot be negative."
                    )

                if data["Resource_ID"].duplicated().any():
                    raise ValueError(
                        "Duplicate Resource_ID values found. "
                        "Each resource must be unique."
                    )

                analysis_result = analyze_cloud_data(data)

                resources = analysis_result["resources"]

                top_opportunities = (
                    analysis_result["top_opportunities"]
                )

                status_counts = (
                    analysis_result["status_counts"]
                )

                total_current_cost = (
                    analysis_result["total_cost"]
                )

                total_potential_saving = (
                    analysis_result["potential_saving"]
                )

                optimized_cost = (
                    analysis_result["optimized_cost"]
                )

                saving_percentage = (
                    analysis_result["saving_percentage"]
                )

                # -----------------------------
                # Save analysis for exports
                # -----------------------------

                request.session["analysis_resources"] = resources

                request.session["analysis_summary"] = {
                    "provider": selected_provider_name,
                    "total_cost": float(total_current_cost),
                    "potential_saving": float(
                        total_potential_saving
                    ),
                    "optimized_cost": float(optimized_cost),
                    "saving_percentage": float(
                        saving_percentage
                    ),
                    "status_counts": status_counts,
                }

                request.session["top_opportunities"] = (
                    top_opportunities
                )

        except Exception as error:

            error_message = (
                "Unable to analyze uploaded file: "
                + str(error)
            )

    # -----------------------------
    # Send data to HTML
    # -----------------------------

    context = {
        "resources": resources,
        "top_opportunities": top_opportunities,
        "status_counts": status_counts,

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


# =========================================================
# CSV EXPORT
# =========================================================

def export_csv(request):

    resources = request.session.get(
        "analysis_resources",
        []
    )

    response = HttpResponse(
        content_type="text/csv"
    )

    response["Content-Disposition"] = (
        'attachment; filename="cloudwise_report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Resource",
        "Provider",
        "Resource Type",
        "Avg CPU (%)",
        "Peak CPU (%)",
        "RAM Usage (%)",
        "Runtime Hours",
        "Status",
        "Priority",
        "Priority Score",
        "Monthly Cost",
        "Potential Saving",
        "Recommendation",
    ])

    for resource in resources:

        writer.writerow([
            resource["id"],
            resource["provider"],
            resource["type"],
            resource["cpu"],
            resource["peak_cpu"],
            resource["ram"],
            resource["runtime_hours"],
            resource["status"],
            resource["priority"],
            resource["priority_score"],
            resource["cost"],
            resource["saving"],
            resource["recommendation"],
        ])

    return response


# =========================================================
# PDF EXPORT
# =========================================================

def export_pdf(request):

    resources = request.session.get(
        "analysis_resources",
        []
    )

    summary = request.session.get(
        "analysis_summary",
        {}
    )

    top_opportunities = request.session.get(
        "top_opportunities",
        []
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; filename="cloudwise_report.pdf"'
    )

    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
    )

    styles = getSampleStyleSheet()

    story = []

    # -----------------------------
    # Report Title
    # -----------------------------

    story.append(
        Paragraph(
            "CloudWise Analysis Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # -----------------------------
    # Provider
    # -----------------------------

    provider = summary.get(
        "provider",
        "Not Available"
    )

    story.append(
        Paragraph(
            f"<b>Selected Provider:</b> {provider}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # -----------------------------
    # Cost Summary
    # -----------------------------

    summary_data = [
        [
            "Total Monthly Cost",
            "Potential Saving",
            "Optimized Cost",
            "Saving Percentage",
        ],
        [
            f"Rs. {summary.get('total_cost', 0)}",
            f"Rs. {summary.get('potential_saving', 0)}",
            f"Rs. {summary.get('optimized_cost', 0)}",
            f"{summary.get('saving_percentage', 0)}%",
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            60 * mm,
            60 * mm,
            60 * mm,
            60 * mm,
        ]
    )

    summary_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#2c3e50")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
        ])
    )

    story.append(summary_table)

    story.append(
        Spacer(1, 18)
    )

    # -----------------------------
    # Resource Status Summary
    # -----------------------------

    status_counts = summary.get(
        "status_counts",
        {}
    )

    story.append(
        Paragraph(
            "Resource Status Summary",
            styles["Heading2"]
        )
    )

    status_data = [
        [
            "Potentially Idle",
            "Underutilized",
            "Normal",
            "Overutilized",
        ],
        [
            status_counts.get("idle", 0),
            status_counts.get("underutilized", 0),
            status_counts.get("normal", 0),
            status_counts.get("overutilized", 0),
        ],
    ]

    status_table = Table(
        status_data,
        colWidths=[
            60 * mm,
            60 * mm,
            60 * mm,
            60 * mm,
        ]
    )

    status_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
        ])
    )

    story.append(status_table)

    story.append(
        Spacer(1, 18)
    )

    # -----------------------------
    # Top Optimization Opportunities
    # -----------------------------

    story.append(
        Paragraph(
            "Top Optimization Opportunities",
            styles["Heading2"]
        )
    )

    if top_opportunities:

        top_data = [
            [
                "Resource",
                "Status",
                "Priority",
                "Score",
                "Potential Saving",
            ]
        ]

        for resource in top_opportunities:

            top_data.append([
                resource["id"],
                resource["status"],
                resource["priority"],
                f'{resource["priority_score"]}/100',
                f'Rs. {resource["saving"]}',
            ])

        top_table = Table(
            top_data,
            repeatRows=1
        )

        top_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#2c3e50")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
            ])
        )

        story.append(top_table)

    else:

        story.append(
            Paragraph(
                "No optimization opportunities available.",
                styles["Normal"]
            )
        )

    story.append(
        Spacer(1, 18)
    )

    # -----------------------------
    # Detailed Resource Analysis
    # -----------------------------

    story.append(
        Paragraph(
            "Detailed Resource Analysis",
            styles["Heading2"]
        )
    )

    resource_data = [
        [
            "Resource",
            "Provider",
            "Avg CPU",
            "Peak CPU",
            "RAM",
            "Runtime",
            "Status",
            "Priority",
            "Score",
            "Cost",
            "Saving",
        ]
    ]

    for resource in resources:

        resource_data.append([
            resource["id"],
            resource["provider"],
            f'{resource["cpu"]}%',
            f'{resource["peak_cpu"]}%',
            f'{resource["ram"]}%',
            f'{resource["runtime_hours"]} hrs',
            resource["status"],
            resource["priority"],
            f'{resource["priority_score"]}/100',
            f'Rs. {resource["cost"]}',
            f'Rs. {resource["saving"]}',
        ])

    resource_table = Table(
        resource_data,
        repeatRows=1
    )

    resource_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#2c3e50")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
        ])
    )

    story.append(resource_table)

    doc.build(story)

    return response

def download_sample(request, provider):
    sample_files = {
        "manual": "manual_sample.csv",
        "azure": "azure_sample.csv",
        "aws": "aws_sample.csv",
        "gcp": "gcp_sample.csv",
    }

    filename = sample_files.get(provider.lower())

    if not filename:
        raise Http404("Sample file not found.")

    file_path = settings.SAMPLE_DATA_ROOT / filename

    if not file_path.exists():
        raise Http404("Sample file not found.")

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=filename
    )