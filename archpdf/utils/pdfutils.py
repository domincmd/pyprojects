from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def merge_pdfs(input_paths, output_path):
    merger = PdfWriter()

    try:
        for path in input_paths:
            merger.append(path)

        merger.write(output_path)
    finally:
        merger.close()


def add_page_numbers(input_path, output_path, position="bottom-right"):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        packet = io.BytesIO()

        # Match page size
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        c = canvas.Canvas(packet, pagesize=(width, height))

        text = f"{i + 1}"

        # Positioning
        margin = 20
        if position == "bottom-right":
            x = width - margin
            y = margin
            align = "right"
        elif position == "bottom-center":
            x = width / 2
            y = margin
            align = "center"
        elif position == "bottom-left":
            x = margin
            y = margin
            align = "left"
        else:
            raise ValueError("Invalid position")

        # Draw text
        if align == "right":
            c.drawRightString(x, y, text)
        elif align == "center":
            c.drawCentredString(x, y, text)
        else:
            c.drawString(x, y, text)

        c.save()

        packet.seek(0)
        overlay_pdf = PdfReader(packet)
        overlay_page = overlay_pdf.pages[0]

        page.merge_page(overlay_page)
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)