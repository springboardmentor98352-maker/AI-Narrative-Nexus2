import streamlit as st
import os
from data_extractor import extract_text_from_file
from data_preprocessing import preprocess_text
import pandas as pd

INPUT_FOLDER = "Input_data"
FINAL_FOLDER = "Final_data"

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(FINAL_FOLDER, exist_ok=True)

def render_text_input():
    st.subheader("Upload a file OR paste text")

    # ------------------ Load last processed text ------------------ #
    last_text_file = os.path.join(INPUT_FOLDER, "last_text.txt")
    last_text = ""
    if os.path.exists(last_text_file):
        with open(last_text_file, "r", encoding="utf-8") as f:
            last_text = f.read()

    # ------------------ Text Area ------------------ #
    pasted_text = st.text_area(
        "Or paste text here...",
        height=200,
        value=last_text
    )

    # ------------------ File Uploader ------------------ #
    uploaded_file = st.file_uploader(
        "Upload TXT / CSV / PDF (optional)",
        type=["txt", "csv", "pdf"]
    )

    # ------------------ Process Button ------------------ #
    if st.button("Process Text"):
        raw_text, file_type, df_data, error = extract_text_from_file(
            uploaded_file=uploaded_file,
            pasted_text=pasted_text
        )

        if error:
            st.error(error)
            return

        st.success(f"Extracted ({file_type.upper()}) successfully!")

        # ------------------ Save last input text ------------------ #
        if file_type in ["txt", "pdf"]:
            # Save the extracted text in Input_data for persistence
            with open(os.path.join(INPUT_FOLDER, "last_text.txt"), "w", encoding="utf-8") as f:
                f.write(raw_text)

            # Preprocess and save to Final_data
            processed, err = preprocess_text(raw_text, file_type)
            if err:
                st.error(err)
                return

            with open(os.path.join(FINAL_FOLDER, "processed_text.txt"), "w", encoding="utf-8") as f:
                f.write(processed)

            st.write(processed[:2000])

        elif file_type == "csv":
            # Save CSV file in Input_data
            csv_path = os.path.join(INPUT_FOLDER, "last_csv.csv")
            df_data.to_csv(csv_path, index=False)

            # Preprocess CSV and save to Final_data
            processed_df, err = preprocess_text(text=None, file_type="csv", df=df_data)
            if err:
                st.error(err)
                return

            processed_df.to_csv(os.path.join(FINAL_FOLDER, "processed_csv.csv"), index=False)
            st.dataframe(processed_df.head())

        st.info("Move to the 'Text Analysis' tab for insights.")
