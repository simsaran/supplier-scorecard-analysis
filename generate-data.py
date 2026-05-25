import csv
import random
from datetime import date, timedelta
import math
import json

random.seed(33)

# Fictional Canadian food manufacturer -- NorthPack Foods
# 12 months of supplier delivery data across 10 suppliers
# Ingredients and packaging materials

SUPPLIERS = {
    "SUP-001": {"name": "Prairie Grain Co.",        "category": "Raw Ingredients",  "volume_pct": 18, "risk_profile": "low"},
    "SUP-002": {"name": "Maple Packaging Ltd.",      "category": "Packaging",        "volume_pct": 14, "risk_profile": "high"},
    "SUP-003": {"name": "Great Lakes Dairy Supply",  "category": "Raw Ingredients",  "volume_pct": 12, "risk_profile": "medium"},
    "SUP-004": {"name": "Ontario Fresh Produce",     "category": "Raw Ingredients",  "volume_pct": 10, "risk_profile": "high"},
    "SUP-005": {"name": "Westcoast Oils Inc.",       "category": "Raw Ingredients",  "volume_pct": 9,  "risk_profile": "low"},
    "SUP-006": {"name": "ClearSeal Packaging",       "category": "Packaging",        "volume_pct": 8,  "risk_profile": "medium"},
    "SUP-007": {"name": "Rocky Mountain Spices",     "category": "Additives",        "volume_pct": 7,  "risk_profile": "low"},
    "SUP-008": {"name": "Atlantic Seafood Supply",   "category": "Raw Ingredients",  "volume_pct": 7,  "risk_profile": "high"},
    "SUP-009": {"name": "Northern Flavours Ltd.",    "category": "Additives",        "volume_pct": 9,  "risk_profile": "medium"},
    "SUP-010": {"name": "EcoBox Solutions",          "category": "Packaging",        "volume_pct": 6,  "risk_profile": "medium"},
}

RISK_PROFILES = {
    "low":    {"otd_mean": 0.93, "otd_std": 0.04, "defect_mean": 0.008, "defect_std": 0.003, "doc_mean": 0.96, "doc_std": 0.03, "lead_time_mean": 7,  "lead_time_std": 1.0},
    "medium": {"otd_mean": 0.84, "otd_std": 0.07, "defect_mean": 0.022, "defect_std": 0.008, "doc_mean": 0.89, "doc_std": 0.06, "lead_time_mean": 10, "lead_time_std": 2.5},
    "high":   {"otd_mean": 0.68, "otd_std": 0.10, "defect_mean": 0.048, "defect_std": 0.015, "doc_mean": 0.75, "doc_std": 0.10, "lead_time_mean": 14, "lead_time_std": 4.0},
}

start_date = date(2024, 1, 1)
all_deliveries = []
delivery_id = 1

for sup_id, sup in SUPPLIERS.items():
    profile = RISK_PROFILES[sup["risk_profile"]]
    monthly_deliveries = random.randint(6, 12)

    for month_offset in range(12):
        month_date = date(2024, 1 + month_offset, 1) if month_offset < 12 else date(2025, month_offset - 11, 1)
        month_str = month_date.strftime("%Y-%m")

        for _ in range(random.randint(4, monthly_deliveries)):
            day = random.randint(1, 28)
            delivery_date = date(2024, month_date.month, day)

            scheduled_date = delivery_date - timedelta(days=random.randint(0, 5))
            lead_time = max(1, round(random.gauss(profile["lead_time_mean"], profile["lead_time_std"])))
            on_time = random.random() < max(0.3, random.gauss(profile["otd_mean"], profile["otd_std"]))
            days_late = 0 if on_time else random.randint(1, 12)
            defect_rate = max(0, random.gauss(profile["defect_mean"], profile["defect_std"]))
            doc_compliant = random.random() < max(0.5, random.gauss(profile["doc_mean"], profile["doc_std"]))
            order_qty = random.randint(500, 8000)
            defective_units = int(order_qty * defect_rate)

            all_deliveries.append({
                "Delivery ID": f"DEL{str(delivery_id).zfill(5)}",
                "Supplier ID": sup_id,
                "Supplier Name": sup["name"],
                "Category": sup["category"],
                "Month": month_str,
                "Delivery Date": delivery_date.strftime("%Y-%m-%d"),
                "Scheduled Date": scheduled_date.strftime("%Y-%m-%d"),
                "Lead Time Days": lead_time,
                "On Time": "Yes" if on_time else "No",
                "Days Late": days_late,
                "Order Quantity": order_qty,
                "Defective Units": defective_units,
                "Defect Rate %": round(defect_rate * 100, 2),
                "Documentation Compliant": "Yes" if doc_compliant else "No",
                "Volume % of Total Spend": sup["volume_pct"],
            })
            delivery_id += 1

all_deliveries.sort(key=lambda x: x["Delivery Date"])

with open('/home/claude/supplier-scorecard/delivery-data.csv','w',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=all_deliveries[0].keys())
    writer.writeheader()
    writer.writerows(all_deliveries)

print(f"Delivery dataset: {len(all_deliveries)} records across {len(SUPPLIERS)} suppliers")

from collections import defaultdict
sup_agg = defaultdict(lambda:{"deliveries":0,"on_time":0,"total_late_days":0,"defect_sum":0,"order_qty":0,"defective":0,"doc_ok":0})
for d in all_deliveries:
    s = d["Supplier ID"]
    sup_agg[s]["deliveries"] += 1
    if d["On Time"] == "Yes": sup_agg[s]["on_time"] += 1
    sup_agg[s]["total_late_days"] += d["Days Late"]
    sup_agg[s]["defect_sum"] += d["Defect Rate %"]
    sup_agg[s]["order_qty"] += d["Order Quantity"]
    sup_agg[s]["defective"] += d["Defective Units"]
    if d["Documentation Compliant"] == "Yes": sup_agg[s]["doc_ok"] += 1

WEIGHTS = {"otd": 0.35, "defect": 0.30, "doc": 0.20, "lead": 0.15}

scorecard_rows = []
for sup_id, d in sup_agg.items():
    sup = SUPPLIERS[sup_id]
    n = d["deliveries"]
    otd_rate = round(d["on_time"] / n * 100, 1)
    avg_defect = round(d["defect_sum"] / n, 2)
    doc_rate = round(d["doc_ok"] / n * 100, 1)
    avg_lead = round(sum(float(x["Lead Time Days"]) for x in all_deliveries if x["Supplier ID"]==sup_id) / n, 1)

    otd_score = min(100, otd_rate)
    defect_score = max(0, 100 - avg_defect * 20)
    doc_score = doc_rate
    lead_score = max(0, 100 - max(0, avg_lead - 5) * 4)

    weighted_score = round(
        otd_score * WEIGHTS["otd"] +
        defect_score * WEIGHTS["defect"] +
        doc_score * WEIGHTS["doc"] +
        lead_score * WEIGHTS["lead"],
        1
    )

    if weighted_score >= 80:
        status = "Approved"
        status_color = "green"
    elif weighted_score >= 60:
        status = "Watch List"
        status_color = "amber"
    else:
        status = "At Risk"
        status_color = "red"

    scorecard_rows.append({
        "Supplier ID": sup_id,
        "Supplier Name": sup["name"],
        "Category": sup["category"],
        "Volume % of Spend": sup["volume_pct"],
        "Total Deliveries": n,
        "On-Time Delivery Rate %": otd_rate,
        "Avg Defect Rate %": avg_defect,
        "Documentation Compliance %": doc_rate,
        "Avg Lead Time Days": avg_lead,
        "OTD Score (35%)": round(otd_score, 1),
        "Defect Score (30%)": round(defect_score, 1),
        "Doc Score (20%)": round(doc_score, 1),
        "Lead Time Score (15%)": round(lead_score, 1),
        "Weighted Score": weighted_score,
        "Status": status,
        "Total Defective Units": d["defective"],
        "Total Order Quantity": d["order_qty"],
    })

scorecard_rows.sort(key=lambda x: x["Weighted Score"])

with open('/home/claude/supplier-scorecard/supplier-scorecard.csv','w',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=scorecard_rows[0].keys())
    writer.writeheader()
    writer.writerows(scorecard_rows)

print("\nSupplier scorecard:")
for r in scorecard_rows:
    print(f"  {r['Supplier Name']}: score {r['Weighted Score']} | OTD {r['On-Time Delivery Rate %']}% | Defect {r['Avg Defect Rate %']}% | Status: {r['Status']}")

at_risk = [r for r in scorecard_rows if r["Status"]=="At Risk"]
watch = [r for r in scorecard_rows if r["Status"]=="Watch List"]
approved = [r for r in scorecard_rows if r["Status"]=="Approved"]

root_cause_rows = []
for r in at_risk + watch[:2]:
    sup_deliveries = [d for d in all_deliveries if d["Supplier ID"]==r["Supplier ID"]]
    late = [d for d in sup_deliveries if d["On Time"]=="No"]
    late_pct = round(len(late)/len(sup_deliveries)*100,1)

    if r["Status"] == "At Risk":
        primary_cause = "Systemic delivery failure — late deliveries concentrated across all months with no improvement trend"
        secondary_cause = "Documentation non-compliance — missing or incomplete COAs and delivery notes on majority of shipments"
        five_why_root = "Supplier does not have a formal internal scheduling system. Deliveries are managed manually by one person with no backup coverage."
        recommended_action = "Issue formal corrective action request. Schedule supplier audit within 30 days. Identify alternative supplier as contingency."
        urgency = "Immediate"
    else:
        primary_cause = "Elevated defect rate — above acceptable threshold in most recent 3 months"
        secondary_cause = "Lead time variance — unpredictable delivery windows creating planning uncertainty"
        five_why_root = "Production scheduling changes at supplier facility not communicated to NorthPack. No change notification protocol in supplier agreement."
        recommended_action = "Issue performance improvement notice. Require monthly reporting for 90 days. Update supplier agreement to include change notification clause."
        urgency = "Within 30 days"

    root_cause_rows.append({
        "Supplier ID": r["Supplier ID"],
        "Supplier Name": r["Supplier Name"],
        "Status": r["Status"],
        "Weighted Score": r["Weighted Score"],
        "Volume % of Spend": r["Volume % of Spend"],
        "Primary Root Cause": primary_cause,
        "Secondary Root Cause": secondary_cause,
        "5 Whys Root Cause": five_why_root,
        "Recommended Action": recommended_action,
        "Urgency": urgency,
    })

with open('/home/claude/supplier-scorecard/root-cause-analysis.csv','w',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=root_cause_rows[0].keys())
    writer.writeheader()
    writer.writerows(root_cause_rows)

total_vol_at_risk = sum(r["Volume % of Spend"] for r in at_risk)
total_vol_watch = sum(r["Volume % of Spend"] for r in watch)

summary = [
    ["Metric","Value","Notes"],
    ["Total suppliers assessed","10","Across raw ingredients, packaging, and additives"],
    ["Analysis period","12 months","January to December 2024"],
    ["Total deliveries tracked",str(len(all_deliveries)),"Across all 10 suppliers"],
    ["Suppliers — Approved",str(len(approved)),"Weighted score 80 or above"],
    ["Suppliers — Watch List",str(len(watch)),"Weighted score 60 to 79"],
    ["Suppliers — At Risk",str(len(at_risk)),"Weighted score below 60"],
    ["% of spend in At Risk suppliers",f"{total_vol_at_risk}%","High concentration risk"],
    ["% of spend in Watch List suppliers",f"{total_vol_watch}%","Monitoring required"],
    ["Worst performing supplier",scorecard_rows[0]["Supplier Name"],f"Score {scorecard_rows[0]['Weighted Score']} — {scorecard_rows[0]['Status']}"],
    ["Second worst supplier",scorecard_rows[1]["Supplier Name"],f"Score {scorecard_rows[1]['Weighted Score']} — {scorecard_rows[1]['Status']}"],
    ["Scoring weights","OTD 35%, Defect 30%, Documentation 20%, Lead Time 15%","Weighted by operational impact"],
]

with open('/home/claude/supplier-scorecard/analysis-summary.csv','w',newline='') as f:
    writer = csv.writer(f)
    writer.writerows(summary)

print(f"\nAt risk suppliers: {len(at_risk)} ({total_vol_at_risk}% of spend)")
print(f"Watch list suppliers: {len(watch)} ({total_vol_watch}% of spend)")
print(f"Approved suppliers: {len(approved)}")
print("\nAll files written.")
