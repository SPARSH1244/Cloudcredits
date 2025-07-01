import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def export_to_json(data, filename="export.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    return filename

def export_to_pdf(data, filename="export.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica", 12)
    c.drawString(50, y, "CryptX Export Report")
    y -= 30

    for key, value in data.items():
        lines = [f"{key}: {value[i:i+90]}" for i in range(0, len(str(value)), 90)]
        for line in lines:
            if y < 50:
                c.showPage()
                y = height - 50
            c.drawString(50, y, line)
            y -= 20

    c.save()
    return filename
