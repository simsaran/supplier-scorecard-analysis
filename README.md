# supplier-scorecard-analysis
# The Supplier That Was Always Late
### Supplier Performance Scorecard: NorthPack Foods

I worked in shipping and receiving at Agropur. You learn quickly which suppliers you can count on and which ones you build buffer time around. I wanted to quantify that instinct.

This project builds the formal scorecard that would have made that pattern visible much earlier and given the procurement team something concrete to act on.

---

## What this is

A supplier performance scorecard and root cause analysis for a fictional Canadian food manufacturer called NorthPack Foods. 12 months of delivery data across 10 suppliers. A weighted scoring model across four dimensions. A formal supplier review report with corrective action recommendations for the bottom performers.

---

## What the data showed

Three suppliers are At Risk with weighted scores below 60. Together they account for 31% of total purchase spend — a significant concentration of risk in underperforming suppliers.

| Supplier | Score | OTD % | Defect % | Status |
|---------|-------|--------|----------|--------|
| Atlantic Seafood Supply | 45.0 | 63.9% | 5.07% | At Risk |
| Maple Packaging Ltd. | 45.9 | 61.3% | 5.01% | At Risk |
| Ontario Fresh Produce | 51.1 | 67.4% | 4.60% | At Risk |
| Northern Flavours Ltd. | 75.5 | 86.4% | 2.34% | Watch List |
| Prairie Grain Co. | 90.6 | 94.0% | 0.82% | Approved |

The scoring model weights delivery reliability most heavily because a late delivery in food manufacturing does not just mean a delay. It means a production line stops.

---

## How the scoring works

Four dimensions. Four weights based on operational impact.

On-time delivery at 35% because production schedules depend on it. Defect rate at 30% because food safety and rework cost both flow directly from quality failures. Documentation compliance at 20% because missing certificates of analysis and delivery notes create regulatory and traceability risk. Lead time consistency at 15% because unpredictable lead times make planning impossible even when deliveries eventually arrive.

Each dimension is scored 0 to 100 and the weighted composite determines the classification.

---

## Files in this repo

| File | What it is |
|------|-----------|
| supplier-review.pdf | Full supplier performance review report with scorecard, root cause analysis, and corrective action plan |
| delivery-data.csv | 774 delivery records across 10 suppliers with OTD, defect rate, documentation compliance, and lead time |
| supplier-scorecard.csv | Weighted scorecard with individual dimension scores and overall status for all 10 suppliers |
| root-cause-analysis.csv | 5 Whys root cause analysis and recommended corrective actions for At Risk and Watch List suppliers |
| analysis-summary.csv | Headline metrics in one place |
| generate-data.py | Python script that built the dataset and ran the scoring model |

---

## Skills demonstrated

Supplier scorecarding and performance classification. Weighted scoring model design. Root cause analysis using 5 Whys. Corrective action planning. On-time delivery and defect rate analysis. Food manufacturing supply chain knowledge. Python for data generation and scoring calculation. Procurement operations context.

---

## About this project

Part of a portfolio series built while job searching in Canada after graduating from the University of Waterloo.

Prepared by Simran Saran. Co-op experience at Agropur in shipping and receiving. Targeting supply chain analyst and operations analyst roles at PepsiCo, Maple Leaf, Saputo, and Agropur across Canada.

All data is synthetic. NorthPack Foods is fictional. Supplier performance patterns are modelled on real supply chain management challenges in Canadian food manufacturing.
