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
    st.header("Cosine Similarity")

   
    st.subheader("")
    upload1 = st.file_uploader(
        "Upload txt, pdf, csv",
        type=["txt", "pdf", "csv"],
        key="cos_file1",
        help="This uploader spans the full width of the screen"
    )

    
    text1_text, text1_df = read_file(upload1)                        #read file

    if text1_df is not None:
        text1_text = " ".join(
            text1_df.astype(str)
            .fillna("")
            .apply(lambda row: " ".join(row), axis=1)
            .tolist()
        )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Text 1 ")
        text1_input = st.text_area("Enter first text", height=100)
        text1_final = (text1_input or "") + " " + (text1_text or "")

    with col2:
        st.subheader("Text 2")
        text2_input = st.text_area("Enter second text", height=100)


    if st.button("Calculate Cosine Similarity", key="cos_btn"):
        if text1_final.strip() == "" or text2_input.strip() == "":
            st.error("Both text fields must contain content.")
        else:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

                                                                                            #tf=idf
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform([text1_final, text2_input])

           
            score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

            
            st.write("### Cosine Similarity Score:")
            st.success(f"**{score:.4f}**")                                                   #results
            st.info(f"Similarity: {score*100:.2f}%")


with tab3:
    st.header("Pre-processing")

    preview_file = st.file_uploader("Upload txt, pdf, csv", type=["txt", "pdf", "csv"], key="prev_file")
    text_raw, df_raw = read_file(preview_file)

    if df_raw is not None:
        st.subheader("Before Preprocessing (CSV)")
        st.dataframe(df_raw)

        df_clean = df_raw.applymap(clean_cell)

        st.subheader("After Preprocessing (CSV)")
        st.dataframe(df_clean)
        st.success("CSV Preprocessing Completed!")

    elif text_raw:
        st.subheader("Before Preprocessing (Text)")
        st.write(text_raw[:1500] + "...")

        processed = preprocess_text(text_raw)

        st.subheader("After Preprocessing (Text)")
        st.write(processed[:1500] + "...")
        st.success("Text Preprocessing Completed!")
