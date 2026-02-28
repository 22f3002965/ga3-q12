from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import re
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str):

    # 1️⃣ Ticket Status
    match = re.search(r"ticket (\d+)", q, re.IGNORECASE)
    if "ticket" in q.lower() and match:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": int(match.group(1))
            })
        }

    # 2️⃣ Schedule Meeting
    match = re.search(r"(\d{4}-\d{2}-\d{2}).*?(\d{2}:\d{2}).*?Room ([A-Za-z0-9 ]+)", q)
    if "schedule" in q.lower() and match:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": match.group(1),
                "time": match.group(2),
                "meeting_room": f"Room {match.group(3)}"
            })
        }

    # 3️⃣ Expense Balance
    match = re.search(r"employee (\d+)", q, re.IGNORECASE)
    if "expense" in q.lower() and match:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": int(match.group(1))
            })
        }

    # 4️⃣ Performance Bonus
    match = re.search(r"employee (\d+).*?(\d{4})", q, re.IGNORECASE)
    if "bonus" in q.lower() and match:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(match.group(1)),
                "current_year": int(match.group(2))
            })
        }

    # 5️⃣ Office Issue
    match = re.search(r"issue (\d+).*?department\.?", q, re.IGNORECASE)
    dept_match = re.search(r"for the ([A-Za-z ]+) department", q, re.IGNORECASE)
    if "issue" in q.lower() and match and dept_match:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(match.group(1)),
                "department": dept_match.group(1)
            })
        }

    return JSONResponse(status_code=400, content={"error": "Query not recognized"})
