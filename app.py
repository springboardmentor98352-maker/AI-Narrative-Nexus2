import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ui import page_bg
from read_file import read_file
from preprocessing import count_words, preprocess_text, clean_cell


st.set_page_config(page_title="Dynamic Text Analysis Platform", layout="wide")
st.markdown(page_bg, unsafe_allow_html=True)

st.title("Dynamic Text Analysis Platform")


tab1, tab2, tab3 = st.tabs(["Text Tokenization", "Cosine Similarity", "Preprocessing"])


with tab1:
    st.header("Text Tokenization")
    user_text = st.text_area("Enter text to tokenize", height=100)    #user input

    
    upload_file = st.file_uploader("Upload txt, pdf, csv",                
                                   type=["txt", "pdf", "csv"], 
                                   key="tok_file")                          #upload file

 
    file_text, file_df = read_file(upload_file)                        #read file

    if file_df is not None:
        st.subheader("CSV Preview")
        st.dataframe(file_df)

                                                                      #conversion
        csv_text = " ".join(
            file_df.astype(str)
            .fillna("")
            .apply(lambda row: " ".join(row), axis=1)
            .tolist()
        )
        file_text = csv_text   

   
    elif file_text:
        st.subheader("File Preview")
        st.write(file_text[:500] + "..." if len(file_text) > 500 else file_text)

    
    import re

    def simple_tokenize(text):
        return re.findall(r"\b\w+\b", text.lower())

    
    if st.button("Tokenize"):
        if not user_text and not file_text:
            st.error("Enter text or upload a file.")
        else:
            combined = (user_text or "") + " " + (file_text or "")
            tokens = simple_tokenize(combined)

            st.write("### Tokens")
            st.write(tokens)
            st.success(f"Total Tokens: **{len(tokens)}**")

    
    if st.button("Total Words"):
        combined = (user_text or "") + " " + (file_text or "")
        wc = count_words(combined)
        st.success(f"Total Words: **{wc}**")




with tab2:
    st.header("Word Similarity (Cosine TF-IDF)")

    # --------------------------------------
    # BACKEND WORD LIST
    # --------------------------------------
    backend_words = [
        "apple", "banana", "orange", "grapes", "mango", "pineapple",
        "dog", "cat", "lion", "tiger", "elephant", "horse",
        "happy", "sad", "angry", "excited", "confused",
        "computer", "mobile", "internet", "software", "hardware", "cpu", "python",
        "love", "hate", "book", "car", "house", "chair", "school",
        "teacher", "student", "water", "food", "work", "job", "city",
        "run", "jump", "eat", "sleep", "walk", "write", "read",
        "sales", "customer", "profit", "loss", "market", "analysis",
        "doctor", "medicine", "health", "family", "music", "movie"
    ]

    import re
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    # --------------------------------------
    # TOKENIZER (NO NLTK)
    # --------------------------------------
    def tokenize(text):
        return re.findall(r"[a-zA-Z]+", text.lower())

    # --------------------------------------
    # SIMILARITY FUNCTION
    # --------------------------------------
    def get_similarity(text):
        cleaned_input_words = tokenize(text)

        if not cleaned_input_words:
            return None

        cleaned_backend = [w.lower() for w in backend_words]

        vectorizer = TfidfVectorizer()

        all_words = cleaned_input_words + cleaned_backend
        vectors = vectorizer.fit_transform(all_words)

        input_vec = vectors[:len(cleaned_input_words)]
        backend_vec = vectors[len(cleaned_input_words):]

        sim_matrix = cosine_similarity(input_vec, backend_vec)
        avg_similarity = sim_matrix.mean(axis=0)

        # top 5 matches
        top_idx = avg_similarity.argsort()[::-1][:5]

        results = [(backend_words[i], avg_similarity[i]) for i in top_idx]
        return results

    # --------------------------------------
    # UI
    # --------------------------------------
    user_text = st.text_area("Enter paragraph / sentence text:", height=120)

    if st.button("Find Similar Words"):
        if not user_text.strip():
            st.warning("Please enter some text!")
        else:
            results = get_similarity(user_text)

            if not results:
                st.error("No valid words found in input.")
            else:
                st.subheader("🔍 Top Similar Word Matches")

                for word, score in results:
                    st.write(f"**{word}** — {score:.4f}")



with tab3:
    st.header("Pre-processing")

    # Upload file
    preview_file = st.file_uploader("Upload txt, pdf, csv", type=["txt", "pdf", "csv"], key="prev_file")

    if preview_file is not None:

        # -------- Determine File Type -------- #
        if preview_file.type == "text/plain":
            file_type = "txt"
            text_raw = preview_file.read().decode("utf-8")
            df_raw = None

        elif preview_file.type == "application/pdf":
            file_type = "pdf"
            from pypdf import PdfReader
            reader = PdfReader(preview_file)
            text_raw = ""
            for page in reader.pages:
                text_raw += page.extract_text() or ""
            df_raw = None

        elif preview_file.type == "text/csv":
            file_type = "csv"
            df_raw = pd.read_csv(preview_file)
            text_raw = None

        else:
            st.error("Unsupported file type.")
            st.stop()

        st.subheader("Before Preprocessing")

        # Show preview based on type
        if file_type in ["txt", "pdf"]:
            st.write(text_raw[:1500] + "..." if len(text_raw) > 1500 else text_raw)

        elif file_type == "csv":
            st.dataframe(df_raw)


        # -------- RUN PREPROCESSING -------- #
        st.write("---")

        st.subheader("After Preprocessing")

        cleaned_output, error = None, None

        if file_type in ["txt", "pdf"]:
            cleaned_output, error = preprocess_text(text=text_raw, file_type=file_type)

            if error:
                st.error(error)
            else:
                st.write(cleaned_output[:2000] + "...")
                st.success("Text preprocessing completed and saved in Final_data/processed_text.txt")


        elif file_type == "csv":
            cleaned_output, error = preprocess_text(df=df_raw, file_type="csv")

            if error:
                st.error(error)
            else:
                st.dataframe(cleaned_output)
                st.success("CSV preprocessing completed and saved in Final_data/processed_csv.csv")
