
````markdown
🧠 Dynamic AI Text Summarisation

A Streamlit-based application for extracting, cleaning, analyzing, and summarizing text data from multiple sources such as TXT, PDF, and CSV files.
The project provides abstractive summaries, text metrics, sentiment analysis, and downloadable reports, making it ideal for research, content analysis, and data-driven insights.
---
````

1. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

2. Install dependencies

```bash
pip install -r KeerthiLahari/requirements.txt
```

3. Run the Streamlit application

```bash
streamlit run KeerthiLahari/app.py
```

---

🗂 Project Structure

```
Dynamic AI text Summarisation/
├── Final_data/
│   └── Processed text and CSV files
├── Input_data/
│   └── Uploaded input files
├── KeerthiLahari/
│   ├── Final_summary/          # Generated reports for download
│   ├── Styles/
│   │   └── main.css            # Streamlit UI styling
│   ├── UI/
│   │   ├── about.py
│   │   ├── analysis.py
│   │   ├── layout.py
│   │   └── text_input.py
│   ├── app.py                  # Main Streamlit entry point
│   ├── data_extractor.py       # TXT, PDF, CSV text extraction
│   ├── data_preprocessing.py   # Text and CSV preprocessing
│   ├── metrics.py              # Word count, sentiment, token metrics
│   ├── summarise.py            # Abstractive & CSV summarisation
│   └── requirements.txt        # Project dependencies
└── virtual/                    # Virtual environment
```

---

⚡ Technologies Used

* Python 3.9+
* Streamlit – Interactive web application
* NLTK – Natural Language Processing & sentiment analysis
* Scikit-learn – LDA & NMF topic modeling
* Pandas & NumPy – Data processing and CSV summarization
* Plotly – Sentiment distribution visualizations

---

👤 Author

Edara Keerthi Lahari

---

📄 License

This project is licensed under the MIT License.

