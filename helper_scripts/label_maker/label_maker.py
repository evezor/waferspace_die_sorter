import json
from pathlib import Path
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors

# -----------------------------
# Configuration
# -----------------------------
RUN_ID = "1"
FOUNDRY = "GF"

LABEL_WIDTH_MM = 100
LABEL_HEIGHT_MM = 62
SAFE_MARGIN_MM = 5

INPUT_JSON = "../pick_mapper/waferspace_run1_test.json"
OUTPUT_PDF = "waferspace_labels.pdf"

# -----------------------------
# PDF Setup
# -----------------------------
PAGE_SIZE = landscape((LABEL_WIDTH_MM * mm, LABEL_HEIGHT_MM * mm))

doc = SimpleDocTemplate(
    OUTPUT_PDF,
    pagesize=PAGE_SIZE,
    leftMargin=SAFE_MARGIN_MM * mm,
    rightMargin=SAFE_MARGIN_MM * mm,
    topMargin=SAFE_MARGIN_MM * mm,
    bottomMargin=SAFE_MARGIN_MM * mm,
)

styles = getSampleStyleSheet()
style_title = styles["Heading1"]
style_body = styles["Normal"]

elements = []

# -----------------------------
# Load JSON
# -----------------------------
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

# -----------------------------
# Generate Labels
# -----------------------------
for project, entries in data.items():
    quantity = len(entries)

    payload = {
        "project": project,
        "run_id": RUN_ID,
        "foundry": FOUNDRY,
        "quantity": quantity,
    }

    # Text content
    text_block = [
        Paragraph(f"<b>Project:</b> {project}", style_title),
        Spacer(1, 4 * mm),
        Paragraph(f"<b>Run ID:</b> {RUN_ID}", style_body),
        Paragraph(f"<b>Foundry:</b> {FOUNDRY}", style_body),
        Paragraph(f"<b>Quantity:</b> {quantity}", style_body),
    ]

    # QR Code
    qr_code = qr.QrCodeWidget(json.dumps(payload))
    bounds = qr_code.getBounds()
    qr_width = bounds[2] - bounds[0]
    qr_height = bounds[3] - bounds[1]

    qr_size_mm = 30 * mm

    drawing = Drawing(qr_size_mm, qr_size_mm, transform=[
        qr_size_mm / qr_width, 0, 0,
        qr_size_mm / qr_height, 0, 0
    ])

    drawing.add(qr_code)
    
    # Layout table: text left, QR right
    table = Table(
        [[text_block, drawing]],
        colWidths=[
            (LABEL_WIDTH_MM - SAFE_MARGIN_MM * 2 - 35) * mm,
            35 * mm,
        ],
    )

    table.setStyle(
        [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("BOX", (0, 0), (-1, -1), 0, colors.white),
        ]
    )

    elements.append(table)
    elements.append(PageBreak())

# -----------------------------
# Build PDF
# -----------------------------
doc.build(elements)

print(f"Generated {len(data)} labels in {OUTPUT_PDF}")


