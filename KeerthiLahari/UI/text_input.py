import streamlit as st
import os
import pandas as pd

from data_extractor import extract_text_from_file
from data_preprocessing import preprocess_text
from summarise import generate_abstractive_summary

INPUT_FOLDER = "Input_data"
FINAL_FOLDER = "Final_data"
FINAL_SUMMARY_FOLDER = "KeerthiLahari/Final_summary"

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(FINAL_FOLDER, exist_ok=True)
os.makedirs(FINAL_SUMMARY_FOLDER, exist_ok=True)


def render_text_input():

    # Initialize session state
    if "last_file_type" not in st.session_state:
        st.session_state.last_file_type = None

    # ------------------ Paste text ------------------
    pasted_text = st.text_area("Paste text here", height=200)

    uploaded_file = st.file_uploader(
        "Upload TXT / CSV / PDF",
        type=["txt", "csv", "pdf"]
    )

    # ------------------ Auto-process ------------------
    processed_successfully = False
    file_type = None

    if uploaded_file or pasted_text:
        raw_text, file_type_detected, df_data, error = extract_text_from_file(
            uploaded_file=uploaded_file,
            pasted_text=pasted_text
        )

        if error:
            st.error(error)
            return

        if file_type_detected in ["txt", "pdf"]:
            st.session_state.last_file_type = "text"
            processed, err = preprocess_text(raw_text, file_type_detected)
            if err:
                st.error(err)
                return

            with open(os.path.join(FINAL_FOLDER, "processed_text.txt"), "w", encoding="utf-8") as f:
                f.write(processed)

            processed_successfully = True

        elif file_type_detected == "csv":
            st.session_state.last_file_type = "csv"
            processed_df, err = preprocess_text(None, "csv", df_data)
            if err:
                st.error(err)
                return
            processed_df.to_csv(os.path.join(FINAL_FOLDER, "processed_csv.csv"), index=False)
            processed_successfully = True

    # ------------------ Summarise Button ------------------
    if st.button("Summarise"):
        if not processed_successfully:
            st.error("❌ Please upload or paste text to summarise.")
            return
        else:
            file_type = st.session_state.last_file_type

            if file_type == "csv":
                df = pd.read_csv(os.path.join(FINAL_FOLDER, "processed_csv.csv"))
                st.success("Summary generated using Pandas Describe")
                st.dataframe(df.describe())  # ✅ interactive & readable

                # Optional: store CSV summary as text
                csv_summary_text = df.describe().to_string()
                summary_file = os.path.join(FINAL_SUMMARY_FOLDER, "summary.txt")
                with open(summary_file, "w", encoding="utf-8") as f:
                    f.write("=== CSV Summary ===\n")
                    f.write(csv_summary_text)
                    
            else:
                model, summary = generate_abstractive_summary()
                if summary:
                    st.success(f"Summary generated using {model}")
                    st.write(summary)

                    # Store the text summary
                    summary_file = os.path.join(FINAL_SUMMARY_FOLDER, "summary.txt")
                    with open(summary_file, "w", encoding="utf-8") as f:
                        f.write(summary)
    
                else:
                    st.warning("Summary could not be generated.")