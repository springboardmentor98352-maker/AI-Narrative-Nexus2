
````markdown
# Dynamic AI Text Summarisation

A Streamlit-based application for extracting, cleaning, analyzing, and summarizing text data from multiple sources like TXT, PDF, and CSV. The project provides **abstractive summaries**, **text metrics**, and **downloadable reports**, making it ideal for research, content analysis, and data-driven insights.

---

## 🌟 Features

- **Multi-format Input:** Upload TXT, PDF, or CSV files or paste text directly.
- **Text Cleaning & Preprocessing:** Cleans text, removes unwanted characters, stopwords, and prepares it for summarization.
- **Abstractive Summarization:** Uses LDA or NMF topic modeling for meaningful summarization.
- **CSV Summarization:** Generates descriptive statistics using pandas for tabular data.
- **Metrics Dashboard:**
  - Word count
  - Sentence count
  - Top tokens (frequent words)
  - Sentiment analysis & distribution
- **Downloadable Report:** Generate a summary report including metrics and summary.
- **Interactive UI:** Built with Streamlit for an easy-to-use interface.

---

## 🛠 Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd Dynamic\ AI\ text\ Summarisation
````

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
```

3. Install dependencies:

```bash
pip install -r KeerthiLahari/requirements.txt
```

---

## 🚀 Usage

1. Run the Streamlit app:

```bash
streamlit run KeerthiLahari/app.py
```

2. **Upload or paste text:**

   * Supports TXT, PDF, CSV.
   * CSV files are summarized using descriptive statistics.
3. **Generate Summary:** Click the “Summarise” button to view:

   * Abstractive summary (for text)
   * Pandas describe summary (for CSV)
4. **View Metrics:** Word count, sentence count, top tokens, sentiment analysis.
5. **Download Report:** Click the download button in the analysis tab to save the summary and metrics.

---

## 🗂 Project Structure

```
Dynamic AI text Summarisation/
├── Final_data/
│   └── (processed text and CSV files stored here)
├── Input_data/
│   └── (uploaded files stored here)
├── KeerthiLahari/
│   ├── Final_summary/          # Stores generated reports for download
│   ├── Styles/
│   │   └── main.css            # CSS for styling Streamlit app
│   ├── UI/
│   │   ├── about.py
│   │   ├── analysis.py
│   │   ├── layout.py
│   │   └── text_input.py
│   ├── app.py                  # Main Streamlit app
│   ├── data_extractor.py       # Functions to extract text from TXT, PDF, CSV
│   ├── data_preprocessing.py   # Text/CSV preprocessing
│   ├── metrics.py              # Functions to compute word count, sentiment, etc.
│   ├── summarise.py            # Abstractive summary and CSV summarisation
│   └── requirements.txt        # Python dependencies
└── virtual/                    # Virtual environment

```

---

## ⚡ Technologies Used

* **Python 3.9+**
* **Streamlit** – Interactive web app
* **NLTK** – Natural language processing
* **Scikit-learn** – LDA & NMF topic modeling
* **Pandas & NumPy** – Data processing and CSV summarization
* **Plotly** – Charts for sentiment distribution

---

## 📌 Notes

* Preprocessed files are stored in `KeerthiLahari/Final_data/`.
* Abstractive summarization works best on textual data.
* CSV summarization provides descriptive statistics and ignores text cleaning.

---

## 👤 Author

**Edara Keerthi Lahari**
B.Tech CSE | Dynamic AI Text Summarisation Project

---

## 📄 License

This project is licensed under the MIT License.

```

---
```
