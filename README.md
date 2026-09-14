# CloudWise — Multi-Cloud Cost & Resource Optimization Platform

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

CloudWise is a Django-based cloud cost analysis and resource optimization platform.

It accepts cloud resource data, converts provider-specific datasets into one common format, analyzes utilization and monthly cost, and generates clear optimization recommendations through a web dashboard.

The current version is a file-based multi-cloud prototype supporting Offline/Manual, Azure-style, AWS-style, and GCP-style datasets.

## Live Demo

**[Open CloudWise Live](https://cloudwise-afx3.onrender.com)**

---

## Key Features

### Multi-Cloud Data Support

- Offline / Manual resource data
- Microsoft Azure-style datasets
- Amazon Web Services (AWS)-style datasets
- Google Cloud Platform (GCP)-style datasets
- Common normalization layer for consistent analysis

### File Upload

- CSV
- JSON
- Parquet
- Maximum upload size: 10 MB
- Validation for empty files, invalid numeric values, duplicate resource IDs, utilization ranges, and negative values

### Resource Analysis

CloudWise classifies resources into four categories:

- Potentially Idle
- Underutilized
- Normal
- Overutilized

The engine uses average CPU, peak CPU, average RAM, runtime hours, and monthly cost to generate results.

### Optimization Recommendations

- Detect resources that may be stopped or scheduled for shutdown
- Identify resources that may be suitable for rightsizing
- Identify resources that may require scaling or upsizing
- Estimate potential monthly savings
- Calculate estimated optimized monthly cost

### Priority Scoring

Each resource receives a CloudWise priority score from 0 to 100.

The score helps rank optimization opportunities using resource status, monthly cost, and estimated saving.

### Dashboard Analytics

- Total monthly cost
- Potential monthly saving
- Estimated optimized cost
- Saving percentage
- Resource status summary
- Resource status distribution chart
- Cost vs potential saving chart
- Top 3 optimization opportunities
- Detailed resource analysis table

### Reporting

- Export complete analysis as CSV
- Export formatted analysis report as PDF
- Download provider-specific sample datasets directly from the application

---

## Technology Stack

- **Programming Language:** Python 3.13
- **Backend Framework:** Django 6.1
- **Data Processing:** Pandas, NumPy
- **File Processing:** CSV, JSON, Parquet, PyArrow
- **Frontend:** HTML5, CSS3, Django Templates, Vanilla JavaScript
- **Charts:** Chart.js
- **PDF Reports:** ReportLab
- **Local Database:** SQLite
- **Environment Variables:** python-dotenv
- **Version Control:** Git and GitHub

---

## Project Structure

```text
CloudWise/
│
├── analysis/                 # Optimization and cost-analysis logic
├── cloudwise_web/            # Django project settings and root URLs
├── dashboard/                # Dashboard views, template and tests
├── data/                     # Development and demo datasets
├── integrations/             # Future live cloud integration layer
├── normalizers/              # Provider-specific data normalization
├── results/                  # Generated analysis output used during development
├── sample_data/              # Downloadable sample datasets
├── .gitignore
├── LICENSE
├── manage.py
├── requirements.txt
└── README.md
```

The project separates normalization, optimization logic, web presentation, and future provider integration so each responsibility remains easy to understand and maintain.

---

## CloudWise Workflow

```text
Cloud Resource Dataset
        │
        ▼
Upload CSV / JSON / Parquet
        │
        ▼
Select Data Source
        │
        ▼
Provider-Specific Normalizer
        │
        ▼
CloudWise Common Schema
        │
        ▼
Input Validation
        │
        ▼
Optimization Engine
        │
        ├── Resource Classification
        ├── Priority Scoring
        ├── Saving Estimation
        └── Recommendations
        │
        ▼
Dashboard Analytics
        │
        ├── Charts
        ├── Top Opportunities
        ├── Detailed Analysis
        └── CSV / PDF Reports
```

---

## Common Data Schema

All provider-specific datasets are normalized into this structure before analysis:

| Field | Description |
|---|---|
| Provider | Cloud provider or data source |
| Resource_ID | Unique resource identifier |
| Resource_Type | Resource type |
| vCPU | Number of virtual CPUs |
| RAM_GB | Allocated memory in GB |
| Avg_CPU | Average CPU utilization (%) |
| Peak_CPU | Peak CPU utilization (%) |
| Avg_RAM | Average RAM utilization (%) |
| Runtime_Hours | Resource runtime in hours |
| Monthly_Cost | Monthly resource cost |
| Currency | Cost currency |

---

## Optimization Rules

### Potentially Idle

```text
Average CPU < 5%
Average RAM < 10%
Peak CPU < 20%
```

CloudWise recommends reviewing the resource for shutdown, decommissioning, or scheduled shutdown depending on runtime.

Estimated saving: up to the current monthly resource cost.

### Underutilized

```text
Average CPU < 20%
Average RAM < 30%
Peak CPU < 60%
```

CloudWise recommends reviewing the resource for rightsizing.

Prototype estimated saving: 40% of monthly cost.

### Overutilized

```text
Average CPU >= 70%
OR Average RAM >= 80%
OR Peak CPU >= 90%
```

CloudWise recommends reviewing workload performance and considering scaling or upsizing.

### Normal

Resources that do not match the above conditions are classified as Normal.

---

## Running the Application Locally

### Clone the Repository

```bash
git clone https://github.com/manav-jagtap/CloudWise.git
cd CloudWise
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Virtual Environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create the Environment File

Create a `.env` file in the project root:

```text
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
```

You can generate a Django secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Apply Database Migrations

```bash
python manage.py migrate
```

### Run the Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## Quick Demo

1. Start the Django development server.
2. Open the CloudWise dashboard.
3. Select a cloud data source.
4. Download a sample dataset from the dashboard or choose an existing compatible file.
5. Upload the file and run the analysis.
6. Review cost summary, status cards, charts, recommendations, and top opportunities.
7. Export the result as CSV or PDF.

---

## Running Tests

```bash
python manage.py test
```

The project includes automated tests for the optimization engine, including idle, underutilized, normal, overutilized, summary calculation, and opportunity ranking behavior.

---

## Data Validation

CloudWise checks uploaded data before analysis.

Validation includes:

- Maximum file size of 10 MB
- Supported file format
- Empty dataset detection
- Valid data-source selection
- Required columns
- Numeric field validation
- CPU and RAM utilization range from 0 to 100
- Non-negative vCPU, RAM, runtime, and monthly cost values
- Duplicate Resource_ID detection

---

## Security

- Django secret key is loaded from environment variables
- `.env` is excluded from Git
- Local SQLite database is excluded from Git
- Django CSRF middleware is enabled
- Django security middleware is enabled
- Sensitive values are not intended to be stored directly in source code

---

## Current Integration Scope

Azure, AWS, and GCP support currently works through provider-style uploaded datasets and provider-specific normalization.

CloudWise does **not** currently fetch live billing and monitoring data directly from cloud-provider APIs.

The Azure integration module is reserved for future live integration and requires an active Azure subscription before it can be implemented and tested properly.

---

## Prototype Assumptions

CloudWise is an academic and portfolio prototype.

- Optimization thresholds are CloudWise prototype rules, not official Azure, AWS, or GCP recommendations.
- Potential savings are estimates and should be validated before making real infrastructure changes.
- Provider-style sample files represent the fields required by CloudWise and are not complete exports of every cloud-provider billing or monitoring service.

---

## Future Enhancements

- Live Azure Cost Management and Azure Monitor integration
- Live AWS Cost Explorer and CloudWatch integration
- Live GCP Billing and Cloud Monitoring integration
- Authentication and user accounts
- Saved analysis history
- Database-backed reports
- Custom optimization thresholds
- Additional resource types
- Historical utilization analysis
- Scheduled analysis
- Advanced FinOps recommendations
- Cloud deployment of the complete application

---

## Project Status

CloudWise currently includes multi-cloud file normalization, upload validation, resource classification, priority scoring, saving estimation, dashboard analytics, downloadable sample datasets, CSV export, PDF export, and automated optimization-engine tests.

The current version is ready for local academic demonstration and portfolio presentation as a file-based prototype.

---

## Author

**Manav Jagtap**  
B.Sc. Computer Science

If you find the project useful, consider giving it a star on GitHub.
