# CloudWise — Multi-Cloud Cost & Resource Optimization

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

CloudWise is a Django and Pandas portfolio prototype that converts Azure-, AWS-, GCP-, and manually structured resource data into a common schema, analyzes utilization and cost, and produces actionable optimization recommendations.

[Open Live Demo](https://cloudwise-afx3.onrender.com) • [View Source](https://github.com/manav-jagtap/CloudWise)

## Engineering Highlights

- Provider-specific normalization into one consistent analysis model
- CSV, JSON, and Parquet uploads up to 10 MB
- Validation for missing fields, invalid values, duplicate IDs, and utilization ranges
- Idle, underutilized, normal, and overutilized classifications
- Priority scoring from 0 to 100
- Estimated monthly savings and optimized cost
- Dashboard charts, top opportunities, and detailed resource results
- CSV and PDF report exports
- Automated optimization-engine tests

## How It Works

1. Upload a provider-style or manual resource dataset.
2. Select the source format.
3. Normalize the input into the CloudWise common schema.
4. Validate resource and utilization data.
5. Classify resources and calculate priority scores.
6. Generate recommendations and estimated savings.
7. Review or export the analysis.

## Optimization Rules

| Classification | Prototype rule | Suggested review |
|---|---|---|
| Potentially Idle | Avg CPU < 5%, Avg RAM < 10%, Peak CPU < 20% | Shutdown, decommission, or schedule |
| Underutilized | Avg CPU < 20%, Avg RAM < 30%, Peak CPU < 60% | Rightsize the resource |
| Overutilized | Avg CPU ≥ 70%, Avg RAM ≥ 80%, or Peak CPU ≥ 90% | Scale or upsize |
| Normal | No other rule matches | Continue monitoring |

The thresholds are CloudWise prototype rules and are not official recommendations from Azure, AWS, or GCP.

## Common Data Schema

| Field | Purpose |
|---|---|
| Provider | Cloud provider or manual source |
| Resource_ID | Unique resource identifier |
| Resource_Type | Resource category |
| vCPU / RAM_GB | Allocated capacity |
| Avg_CPU / Peak_CPU | CPU utilization |
| Avg_RAM | Memory utilization |
| Runtime_Hours | Monthly runtime |
| Monthly_Cost / Currency | Cost information |

## Technology Stack

- Python 3.13 and Django 6.1
- Pandas, NumPy, PyArrow
- HTML, CSS, Django Templates, JavaScript
- Chart.js and ReportLab
- SQLite for local development
- Gunicorn and Render for deployment

## Project Structure

```text
CloudWise/
├── analysis/          # Classification and recommendation logic
├── cloudwise_web/     # Django settings and root URLs
├── dashboard/         # Views, templates, and tests
├── integrations/      # Future live-provider integration layer
├── normalizers/       # Provider-specific normalization
├── sample_data/       # Downloadable demo datasets
├── manage.py
├── requirements.txt
└── README.md
```

## Run Locally

```bash
git clone https://github.com/manav-jagtap/CloudWise.git
cd CloudWise
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file:

```text
DJANGO_SECRET_KEY=replace-with-a-local-secret
DEBUG=True
```

Then run:

```bash
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Tests

```bash
python manage.py test
```

Tests cover resource classification, summary calculations, estimated savings, and opportunity ranking.

## Security and Scope

- Secrets are loaded from environment variables.
- `.env` and the local SQLite database are excluded from Git.
- Django CSRF and security middleware are enabled.
- Current Azure, AWS, and GCP support uses uploaded provider-style datasets.
- CloudWise does not currently fetch live billing or monitoring data from provider APIs.
- Savings are estimates and must be validated before real infrastructure changes.

## Planned Enhancements

- Live Azure Cost Management and Azure Monitor integration
- AWS Cost Explorer and CloudWatch integration
- GCP Billing and Cloud Monitoring integration
- Saved analysis history and custom thresholds
- Scheduled analysis and advanced FinOps recommendations

## Author

**Manav Jagtap** — B.Sc. Computer Science student
