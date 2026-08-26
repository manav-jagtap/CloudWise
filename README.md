#  CloudWise

### Intelligent Multi-Cloud Cost Analysis & Resource Optimization Platform

CloudWise is a Django-based cloud cost analysis and resource optimization platform designed to help users identify idle, underutilized, normal, and overutilized cloud resources across multiple cloud environments.

The current prototype supports Offline/Manual data as well as Azure, AWS, and GCP-style resource datasets through a common normalization layer.

---

##  Project Overview

Cloud infrastructure can become expensive when resources are:

- Running without meaningful utilization
- Oversized for their actual workload
- Underutilized for long periods
- Overloaded and at risk of performance issues
- Difficult to compare across different cloud providers

CloudWise analyzes cloud resource utilization and cost data and provides explainable optimization recommendations.

The system combines:

- Resource utilization analysis
- Cost analysis
- Priority scoring
- Optimization recommendations
- Potential saving estimation
- Multi-cloud normalization
- Dashboard analytics
- CSV and PDF reporting

---

##  Problem Statement

Organizations using cloud infrastructure often struggle to identify inefficient resource usage across multiple cloud platforms.

Cloud providers provide their own monitoring and recommendation tools, but managing recommendations across Azure, AWS, GCP, and offline/manual datasets can become fragmented.

CloudWise aims to provide a unified analysis layer where cloud resource data can be normalized, analyzed, prioritized, and presented through a single dashboard.

---

##  Objectives

The main objectives of CloudWise are:

- Analyze cloud resource utilization
- Identify potentially idle resources
- Detect underutilized resources
- Detect overutilized resources
- Estimate potential cost savings
- Generate optimization recommendations
- Rank optimization opportunities
- Provide multi-cloud data normalization
- Visualize cloud resource analytics
- Export analysis reports

---

##  Supported Data Sources

CloudWise currently supports:

- Offline / Manual Data
- Microsoft Azure-style datasets
- Amazon Web Services (AWS)-style datasets
- Google Cloud Platform (GCP)-style datasets

> Note: The current Azure, AWS, and GCP integrations are file-based prototype adapters. Live cloud API integration is planned as future work.

---

##  Supported File Formats

CloudWise supports:

- CSV
- JSON
- Parquet

Uploaded data is converted into a common CloudWise schema before analysis.

---

##  CloudWise Common Schema

CloudWise normalizes provider-specific data into the following common structure:

| Field | Description |
|---|---|
| Provider | Cloud provider |
| Resource_ID | Unique resource identifier |
| Resource_Type | Resource type |
| vCPU | Number of virtual CPUs |
| RAM_GB | Allocated memory |
| Avg_CPU | Average CPU utilization |
| Peak_CPU | Peak CPU utilization |
| Avg_RAM | Average memory utilization |
| Runtime_Hours | Resource runtime |
| Monthly_Cost | Estimated monthly cost |
| Currency | Cost currency |

---

##  Optimization Engine

CloudWise uses an explainable rule-based optimization engine.

### Potentially Idle

A resource is considered potentially idle when:

```text
Average CPU < 5%
Average RAM < 10%
Peak CPU < 20%
```

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/manav-jagtap/CloudWise.git
cd CloudWise
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

For Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create the environment file

Create a `.env` file in the project root and add:

```text
DJANGO_SECRET_KEY=your-secret-key
```

### 6. Run the Django development server

```bash
python manage.py runserver
```

Open in the browser:

```text
http://127.0.0.1:8000/
```