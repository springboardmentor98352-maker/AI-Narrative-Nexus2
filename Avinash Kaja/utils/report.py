from fpdf import FPDF
import re


def safe_text(text):
    """
    Removes characters that FPDF cannot render (non-latin, special unicode)
    and ensures the text contains only safe printable characters.
    """
    if not text:
        return ""

    # Remove emojis and unsupported symbols
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Replace multiple spaces
    return re.sub(r"\s+", " ", text).strip()


def wrap_long_text(text, max_len=80):
    """
    Break long lines so FPDF never throws width errors.
    """
    words = text.split()
    lines = []
    current = ""

    for w in words:
        if len(current) + len(w) + 1 > max_len:
            lines.append(current)
            current = w
        else:
            current += " " + w if current else w

    if current:
        lines.append(current)

    return "\n".join(lines)


def generate_pdf(summary, topics, sentiments):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", style="B", size=16)
    pdf.multi_cell(0, 10, safe_text("NarrativeNexus NLP Report"))
    pdf.ln(3)

    # Summary Section
    pdf.set_font("Arial", style="B", size=14)
    pdf.multi_cell(0, 10, "Summary")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, wrap_long_text(safe_text(summary)))
    pdf.ln(5)

    # Topics Section
    pdf.set_font("Arial", style="B", size=14)
    pdf.multi_cell(0, 10, "Topics")
    pdf.set_font("Arial", size=12)

    for i, t in enumerate(topics):
        topic_text = f"Topic {i + 1}: {', '.join(t)}"
        topic_text = safe_text(topic_text)
        topic_text = wrap_long_text(topic_text, max_len=60)

        pdf.multi_cell(0, 8, topic_text)
        pdf.ln(1)

    pdf.ln(5)

    # Sentiment Section
    pdf.set_font("Arial", style="B", size=14)
    pdf.multi_cell(0, 10, "Sentiment Analysis")
    pdf.set_font("Arial", size=12)

    for i, s in enumerate(sentiments):
        sent_line = f"Document {i + 1}: {s['label']} (Score: {s['score']:.3f})"
        pdf.multi_cell(0, 8, safe_text(sent_line))

    return pdf.output(dest="S").encode("latin-1")
