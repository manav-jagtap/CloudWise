import pandas as pd
from django.test import SimpleTestCase

from analysis.optimization_engine import analyze_cloud_data, analyze_resource


class OptimizationEngineTests(SimpleTestCase):
    def test_idle_resource(self):
        row = pd.Series({
            "Monthly_Cost": 6000,
            "Avg_CPU": 2,
            "Peak_CPU": 10,
            "Avg_RAM": 5,
            "Runtime_Hours": 600,
        })

        result = analyze_resource(row)

        self.assertEqual(result["status"], "POTENTIALLY IDLE")
        self.assertEqual(result["priority"], "HIGH")
        self.assertEqual(result["priority_score"], 90)
        self.assertEqual(result["estimated_saving"], 6000)

    def test_underutilized_resource(self):
        row = pd.Series({
            "Monthly_Cost": 5000,
            "Avg_CPU": 12,
            "Peak_CPU": 40,
            "Avg_RAM": 20,
            "Runtime_Hours": 300,
        })

        result = analyze_resource(row)

        self.assertEqual(result["status"], "UNDERUTILIZED")
        self.assertEqual(result["priority"], "MEDIUM")
        self.assertEqual(result["estimated_saving"], 2000)
        self.assertEqual(result["priority_score"], 60)

    def test_overutilized_resource(self):
        row = pd.Series({
            "Monthly_Cost": 8000,
            "Avg_CPU": 75,
            "Peak_CPU": 92,
            "Avg_RAM": 60,
            "Runtime_Hours": 500,
        })

        result = analyze_resource(row)

        self.assertEqual(result["status"], "OVERUTILIZED")
        self.assertEqual(result["priority"], "HIGH")
        self.assertEqual(result["priority_score"], 75)
        self.assertEqual(result["estimated_saving"], 0)

    def test_normal_resource(self):
        row = pd.Series({
            "Monthly_Cost": 3000,
            "Avg_CPU": 45,
            "Peak_CPU": 65,
            "Avg_RAM": 55,
            "Runtime_Hours": 400,
        })

        result = analyze_resource(row)

        self.assertEqual(result["status"], "NORMAL")
        self.assertEqual(result["priority"], "LOW")
        self.assertEqual(result["priority_score"], 10)
        self.assertEqual(result["estimated_saving"], 0)

    def test_summary_and_top_opportunities(self):
        data = pd.DataFrame([
            {
                "Provider": "Offline",
                "Resource_ID": "VM-01",
                "Resource_Type": "Virtual Machine",
                "vCPU": 4,
                "RAM_GB": 8,
                "Avg_CPU": 2,
                "Peak_CPU": 10,
                "Avg_RAM": 5,
                "Runtime_Hours": 600,
                "Monthly_Cost": 10000,
                "Currency": "INR",
            },
            {
                "Provider": "Offline",
                "Resource_ID": "VM-02",
                "Resource_Type": "Virtual Machine",
                "vCPU": 4,
                "RAM_GB": 8,
                "Avg_CPU": 15,
                "Peak_CPU": 45,
                "Avg_RAM": 25,
                "Runtime_Hours": 400,
                "Monthly_Cost": 5000,
                "Currency": "INR",
            },
            {
                "Provider": "Offline",
                "Resource_ID": "VM-03",
                "Resource_Type": "Virtual Machine",
                "vCPU": 4,
                "RAM_GB": 8,
                "Avg_CPU": 50,
                "Peak_CPU": 65,
                "Avg_RAM": 50,
                "Runtime_Hours": 400,
                "Monthly_Cost": 3000,
                "Currency": "INR",
            },
        ])

        result = analyze_cloud_data(data)

        self.assertEqual(result["total_cost"], 18000)
        self.assertEqual(result["potential_saving"], 12000)
        self.assertEqual(result["optimized_cost"], 6000)
        self.assertEqual(result["status_counts"]["idle"], 1)
        self.assertEqual(result["status_counts"]["underutilized"], 1)
        self.assertEqual(result["status_counts"]["normal"], 1)
        self.assertEqual(result["top_opportunities"][0]["id"], "VM-01")
