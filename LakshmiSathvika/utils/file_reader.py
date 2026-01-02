import docx
import pandas as pd
import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import PyPDF2

class SimpleHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
    
    def handle_data(self, data):
        self.text.append(data)
    
    def get_text(self):
        return ' '.join(self.text)

def read_file(uploaded_file):
    """Read any uploaded file and return text content"""
    file_name = uploaded_file.name.lower()
    
    try:
        if file_name.endswith('.docx'):
            return read_docx(uploaded_file)
        elif file_name.endswith('.csv'):
            return read_csv(uploaded_file)
        elif file_name.endswith('.json'):
            return read_json(uploaded_file)
        elif file_name.endswith('.xml'):
            return read_xml(uploaded_file)
        elif file_name.endswith(('.html', '.htm')):
            return read_html(uploaded_file)
        elif file_name.endswith('.pdf'):
            return read_pdf(uploaded_file)
        else:
            return read_text(uploaded_file)
    except Exception as e:
        raise Exception(f"Error processing {file_name}: {str(e)}")

def read_docx(file):
    doc = docx.Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

def read_csv(file):
    df = pd.read_csv(file)
    return df.to_string()

def read_json(file):
    data = json.load(file)
    return json.dumps(data, indent=2)

def read_xml(file):
    root = ET.fromstring(file.read())
    return ET.tostring(root, encoding='unicode')

def read_html(file):
    parser = SimpleHTMLParser()
    parser.feed(file.read().decode('utf-8'))
    return parser.get_text()

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def read_text(file):
    return file.read().decode('utf-8')