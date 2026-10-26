def analytics_csv_rows(history): return history

def summary_pdf(summary):
    """Create a compact PDF report entirely from session-generated values."""
    from io import BytesIO
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    output=BytesIO(); pdf=canvas.Canvas(output,pagesize=A4); width,height=A4
    pdf.setTitle("PC Performance Lab Session Summary")
    y=height-54; pdf.setFont("Helvetica-Bold",16); pdf.drawString(48,y,"PC PERFORMANCE LAB — Session Summary"); y-=32
    pdf.setFont("Helvetica",10)
    for label,value in summary:
        if y<52: pdf.showPage(); y=height-54; pdf.setFont("Helvetica",10)
        pdf.drawString(52,y,f"{label}: {value}"); y-=18
    pdf.save(); return output.getvalue()
