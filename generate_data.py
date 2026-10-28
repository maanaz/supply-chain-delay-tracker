# generate_data.py - creates all mock data + policy documents.
import json, os

os.makedirs("data", exist_ok=True)
os.makedirs("docs", exist_ok=True)

# ---------- 1. Shipments (what get_shipment_status reads) ----------
# stock_cover_days = days of inventory left at the factory (safety stock view)
shipments = [
    {"shipment_id": "S-201", "supplier": "Acme Components", "part": "Bearings", "route": "SHA-MAA",
     "status": "In transit", "original_eta": "2026-10-30", "current_eta": "2026-10-30",
     "order_value_usd": 22000, "stock_cover_days": 14, "contract_id": "C-ACME-2025"},
    {"shipment_id": "S-202", "supplier": "Nova Electronics", "part": "Controllers", "route": "SZX-BOM",
     "status": "In transit", "original_eta": "2026-11-04", "current_eta": "2026-11-05",
     "order_value_usd": 61000, "stock_cover_days": 9, "contract_id": "C-NOVA-2025"},
    {"shipment_id": "S-203", "supplier": "Acme Components", "part": "Gaskets", "route": "SIN-COK",
     "status": "At port", "original_eta": "2026-10-28", "current_eta": "2026-10-28",
     "order_value_usd": 9500, "stock_cover_days": 20, "contract_id": "C-ACME-2025"},
    {"shipment_id": "S-204", "supplier": "Acme Components", "part": "Steel shafts", "route": "SHA-MAA",
     "status": "In transit", "original_eta": "2026-11-02", "current_eta": "2026-11-06",
     "order_value_usd": 48000, "stock_cover_days": 6, "contract_id": "C-ACME-2025"},
    {"shipment_id": "S-205", "supplier": "Nova Electronics", "part": "Sensors", "route": "ROT-BOM",
     "status": "Delayed", "original_eta": "2026-11-01", "current_eta": "2026-11-09",
     "order_value_usd": 73000, "stock_cover_days": 4, "contract_id": "C-NOVA-2025"},
    {"shipment_id": "S-206", "supplier": "Acme Components", "part": "Fasteners", "route": "SIN-COK",
     "status": "In transit", "original_eta": "2026-11-08", "current_eta": "2026-11-08",
     "order_value_usd": 7000, "stock_cover_days": 25, "contract_id": "C-ACME-2025"},
    {"shipment_id": "S-207", "supplier": "Nova Electronics", "part": "Batteries", "route": "SZX-BOM",
     "status": "Customs hold", "original_eta": "2026-11-03", "current_eta": "2026-11-07",
     "order_value_usd": 55000, "stock_cover_days": 5, "contract_id": "C-NOVA-2025"},
    {"shipment_id": "S-208", "supplier": "Acme Components", "part": "Valves", "route": "ROT-BOM",
     "status": "In transit", "original_eta": "2026-11-12", "current_eta": "2026-11-12",
     "order_value_usd": 31000, "stock_cover_days": 18, "contract_id": "C-ACME-2025"},
]
json.dump(shipments, open("data/shipments.json", "w"), indent=2)
print(f"Wrote data/shipments.json ({len(shipments)} shipments)")

# ---------- 2. Route conditions (what get_route_delays reads) ----------
routes = {
    "SHA-MAA": {"name": "Shanghai to Chennai", "port_congestion_days": 5,
                "weather_alert": "Typhoon warning in South China Sea", "severity": "high"},
    "SZX-BOM": {"name": "Shenzhen to Mumbai", "port_congestion_days": 2,
                "weather_alert": "None", "severity": "low"},
    "SIN-COK": {"name": "Singapore to Kochi", "port_congestion_days": 1,
                "weather_alert": "Monsoon swell, minor", "severity": "low"},
    "ROT-BOM": {"name": "Rotterdam to Mumbai", "port_congestion_days": 6,
                "weather_alert": "Red Sea rerouting adds transit time", "severity": "high"},
}
json.dump(routes, open("data/route_delays.json", "w"), indent=2)
print(f"Wrote data/route_delays.json ({len(routes)} routes)")

# ---------- 3. Alerts log (create_alert_or_reorder appends here) ----------
json.dump([], open("data/alerts.json", "w"))
print("Wrote data/alerts.json")

# ---------- 4. Policy documents (RAG corpus) ----------
# Sections are separated by blank lines so chunking is easy later.
docs = {}

docs["contract_acme_components.txt"] = """\
CONTRACT C-ACME-2025: Supply Agreement with Acme Components

Clause 4.1 Lead Time
Acme Components commits to a standard lead time of 21 days from order confirmation to delivery at the buyer's factory.

Clause 7.2 Late Delivery Penalty
If delivery is later than 3 grace days past the agreed delivery date, the supplier pays 2 percent of the order value for each additional day late. The total penalty is capped at 20 percent of the order value.

Clause 7.4 Expedited Shipping
If a delay exceeds 5 days, the supplier bears the cost of air freight for up to 30 percent of the order quantity, at the buyer's request.

Clause 9.1 Force Majeure
Delays caused by officially declared weather events exempt the supplier from the Clause 7.2 penalty only if the supplier notifies the buyer in writing within 48 hours of the event.
"""

docs["contract_nova_electronics.txt"] = """\
CONTRACT C-NOVA-2025: Supply Agreement with Nova Electronics

Clause 6.1 Late Delivery Penalty
If delivery is later than 2 grace days past the agreed date, the supplier pays 1.5 percent of the order value per day late, capped at 15 percent of the order value.

Clause 6.3 Cancellation Right
If delay exceeds 14 days, the buyer may cancel the order without penalty and receive a full refund of any advance payment.

Clause 8.2 Alternate Sourcing
If delay exceeds 10 days, the buyer may source the same parts from an alternate supplier without breaching exclusivity.
"""

docs["shipping_sop.txt"] = """\
SHIPPING SOP: Logistics Operating Procedures

SOP-LOG-04 Delay Escalation
Level 1 (1 to 2 days late): log the delay in the tracker. Level 2 (3 to 5 days late): notify the production planner and check stock cover. Level 3 (more than 5 days late, or stock cover is shorter than the expected delay): escalate to the logistics manager the same day.

SOP-LOG-07 Demurrage Control
Each container has 4 free days at the destination port. After that, demurrage is charged at 150 USD per container per day. Container pickup must be booked within 24 hours of vessel arrival.

SOP-LOG-09 Supplier Contact
For any Level 2 or Level 3 delay, request a written status update from the supplier within 24 hours.
"""

docs["delay_playbook.txt"] = """\
DELAY HANDLING PLAYBOOK

PB-01 Risk Bands
If predicted delay risk is below 30 percent, keep monitoring. If risk is 30 to 70 percent, alert the planner and ask the supplier for an update. If risk is above 70 percent, create an alert and evaluate expedited shipping.

PB-02 Stock Cover Rule
If stock cover days is less than the expected delay days plus 2 days of buffer, trigger a reorder from the backup supplier or approve air freight for part of the order.

PB-03 Communication
Always record the reason for any alert or reorder. Inform the supplier in writing and cite the relevant contract clause.
"""

for name, text in docs.items():
    with open(f"docs/{name}", "w", encoding="utf-8") as f:
        f.write(text)
print(f"Wrote {len(docs)} docs in docs/")