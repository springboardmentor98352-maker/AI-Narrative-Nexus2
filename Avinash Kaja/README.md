# 📘 NarrativeNexus Pro — Intelligent Multi-Document Analyzer

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![NLP](https://img.shields.io/badge/NLP-Spacy%20%7C%20NLTK-green)](https://spacy.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**NarrativeNexus Pro** is an advanced, Streamlit-based application designed to process, analyze, compare, and visualize insights from multiple documents simultaneously. It combines state-of-the-art NLP techniques, topic modeling, summarization, and semantic search into a clean, modern interface featuring a "Glassmorphism" design with neon aesthetics.

---

## 🔥 Key Features

### 📄 1. Multi-Format Document Upload
* **Flexible Inputs:** Upload multiple files (PDF, TXT, DOCX) simultaneously or paste raw text.
* **Smart Separation:** Uses custom delimiters (`---`) for handling multi-document raw text inputs.

### 🌍 2. Automatic Language Detection & Translation
* **Detection:** Instantly identifies the language of every uploaded document.
* **Translation:** Automatically translates non-English content into English for consistent analysis.

### 🧠 3. Advanced Text Processing
* **Cleaning Pipeline:** Removes stopwords, punctuation, and special characters.
* **Normalization:** Performs lemmatization and tokenization to prepare data for ML models.

### 📝 4. Intelligent Summarization
* **Transformer Models:** Utilizes advanced transformer-based models to generate concise, coherent abstracts.
* **Quick Insights:** Get the gist of long documents in seconds.

### 🔍 5. Topic Modeling (LDA)
* **Theme Extraction:** Identifies hidden thematic structures within the text corpus.
* **Keywords:** Highlights the most dominant keywords for every identified topic.

### 📊 6. Sentiment Analysis
* **Emotional AI:** Classifies text as **Positive**, **Negative**, or **Neutral**.
* **Scoring:** Provides Polarity and Subjectivity scores for granular emotional insight.

### 🔎 7. Semantic Search (AI Search Engine)
* **Contextual Querying:** Ask natural language questions about your documents.
* **Vector Embeddings:** Retrieves the most relevant passages from all files using sentence embeddings.

### 📉 8. Cosine Similarity Matrix
* **Document Comparison:** Calculates a similarity score (0 to 1) between every pair of documents.
* **Heatmap:** Visualizes how closely related different documents are to each other.

### ☁️ 9. Visual Insights
* **Word Clouds:** Generates aesthetic word clouds to visualize frequent terms.
* **Data Vizzes:** Interactive charts for sentiment distribution and topic frequency.

### 📑 10. Auto-Generated PDF Reports
* **Exportable Insights:** Compiles all analysis, summaries, and charts into a downloadable professional PDF report.

### 🕒 11. Analysis History (Local Memory)
* **Session Management:** Saves every processed batch locally.
* **Review:** Reload previous analyses and reports without re-processing.

### 🎨 12. Modern UI/UX
* **Neon & Glass:** A custom-styled interface with dark mode, neon accents, and glassmorphism effects for a futuristic feel.

---

## 🚀 Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Frontend** | Streamlit, HTML5, CSS3 (Custom Neon/Glass UI) |
| **NLP & ML** | NLTK, Spacy, TextBlob, Gensim (LDA), Transformers (HuggingFace), Scikit-learn |
| **Vectorization** | TF-IDF, Cosine Similarity, Sentence Embeddings |
| **Utilities** | PyPDF2, LangDetect, GoogleTrans, FPDF (Report Generation) |

---

## 📂 Project Structure

```text
NarrativeNexus/
│
├── app.py                 # Main Streamlit application entry point
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
│
├── assets/
│   └── custom.css         # Custom styling for Neon/Glass UI
│
├── utils/
│   ├── file_utils.py      # File handling and loading
│   ├── preprocessing.py   # Text cleaning and normalization
│   ├── summarizer.py      # AI summarization logic
│   ├── topic_modeling.py  # LDA topic extraction
│   ├── sentiment.py       # Sentiment analysis engine
│   ├── visualization.py   # Charts and WordCloud generation
│   ├── cosine_sim.py      # Similarity matrix calculation
│   ├── semantic_search.py # Vector search implementation
│   ├── language.py        # Language detection
│   ├── translate.py       # Translation services
│   └── report.py          # PDF report generation
│
└── uploaded_files/        # Directory for temporary file storage
```
## 🛠 Installation & Setup

Follow these steps to set up the project locally.

### 1️⃣ Clone the Repository
```bash
git clone [https://github.com/springboardmentor98352-maker/AI-Narrative-Nexus2.git](https://github.com/springboardmentor98352-maker/AI-Narrative-Nexus2.git)
cd AI-Narrative-Nexus2
```
### 2️⃣ Create Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
* **Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
* **Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
## 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
**Note: If you encounter errors related to spaCy, run the following command to download the English model:**
```bash
python -m spacy download en_core_web_sm
```
## 4️⃣ Run the App
```bash
streamlit run app.py
```
## 🎯 How It Works
* **Upload:** Drag and drop your files or paste text into the sidebar.
* **Process:** The pipeline automatically cleans, translates, and analyzes the text.
* **Explore:** Navigate through tabs to see Summaries, Sentiment, Topics, and Similarity matrices.
* **Search:** Use the "Semantic Search" bar to find specific information across all files.
* **Export:** Click "Download Report" to get a PDF summary of the analysis.


