import os
import re
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

# ---------- SAFE DOWNLOADS ----------
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")


# Output folder
OUTPUT_DIR = "Final_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# NLP components
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


#Count words
def count_words(text: str) -> int:
    """Counts words in a string based on whitespace splitting."""
    if not isinstance(text, str):
        return 0
    return len(text.split())


# ----------------------------------------------------
# AGGRESSIVE CLEANING (For TXT / PDF)
# ----------------------------------------------------
def clean_text(text: str) -> str:
    """
    Aggressively cleans text for NLP: Lowercasing, removing punctuation/numbers, 
    removing stopwords, and lemmatizing.
    """
    if not isinstance(text, str):
        text = str(text)

    # 1. Lowercasing
    text = text.lower()
    
    # 2. Remove punctuation (Keep numbers for now, they will be stripped later if they are not words)
    # We now remove only non-alphanumeric characters, but KEEP spaces and numbers.
    text = re.sub(r'[^\w\s]', ' ', text) 
    
    # 3. Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # 4. Tokenize and remove stopwords, and filter out remaining standalone numbers
    tokens = text.split()
    tokens = [t for t in tokens if t not in stop_words and not t.isdigit()]
    
    # 5. Lemmatize
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    return " ".join(tokens)


# ----------------------------------------------------
# STRUCTURED CLEANING & IMPUTATION (For CSV)
# ----------------------------------------------------
def clean_csv_structured(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles missing data (NaN) in a structured DataFrame:
    - Fills missing values in numerical columns with the mean of that column.
    - Fills missing values in text columns with a placeholder string ('missing').
    - Protects structural columns (date, ticker) from aggressive cleaning.
    """
    
    # Create a copy to avoid modifying the original DataFrame in place
    processed_df = df.copy()
    
    # Define columns to protect from any text cleaning
    cols_to_exclude = ['date', 'time', 'ticker', 'id', 'name']
    
    # --- STEP 1: IMPUTATION (Robust Logic for Mixed Data) ---
    for col in processed_df.columns:
        
        # A. Attempt Numeric Imputation
        # Try to convert to numeric, coercing errors means non-numeric (like 'AAPL') become NaN
        series_numeric = pd.to_numeric(processed_df[col], errors='coerce')
        
        # Check if the column is primarily numeric (more than 50% non-NaN numeric values)
        is_primarily_numeric = series_numeric.notna().sum() > (len(series_numeric) * 0.5)

        if is_primarily_numeric:
            # --- NUMERIC IMPUTATION (Mean Imputation) ---
            
            # Calculate mean ONLY from the successful numeric conversions
            mean_value = series_numeric.mean() 
            
            if not np.isnan(mean_value):
                # 1. Impute the NaN values in the numeric series with the mean.
                series_imputed = series_numeric.fillna(mean_value)
                
                # 2. Crucial Step for Protection: 
                # Combine the imputed numeric data (series_imputed) with the original data (df[col]).
                # combine_first ensures:
                # - If series_imputed is NOT NaN (real number or imputed mean), it wins.
                # - If series_imputed IS NaN (because the original value was non-numeric, like 'AAPL'), 
                #   the original value from df[col] is retained.
                processed_df[col] = series_imputed.combine_first(df[col])
                
                # Ensure the column type can handle the mixture of numbers and preserved strings
                if df[col].dtype == 'object':
                    processed_df[col] = processed_df[col].astype(object)
                
            # If the mean calculation resulted in NaN, we skip numeric fill.

        # C. Final Text/Placeholder Imputation
        # This handles columns that are purely text, and any remaining NaNs (after numeric imputation).
        if processed_df[col].dtype == 'object' or processed_df[col].isna().any():
            
            # For columns not in the exclusion list, fill NaNs with 'missing'
            if col.lower() not in cols_to_exclude:
                processed_df[col] = processed_df[col].fillna('missing')
                
            # For excluded columns (Ticker, Date), fill with an empty string
            else:
                processed_df[col] = processed_df[col].fillna('')


    # --- STEP 2: AGGRESSIVE CLEANING FOR UNSTRUCTURED TEXT ---
    text_cols_to_clean = [col for col in processed_df.select_dtypes(include=["object"]).columns.tolist() 
                          if col.lower() not in cols_to_exclude]

    if text_cols_to_clean:
        for col in text_cols_to_clean:
            # Apply the aggressive cleaning ONLY to the identified text columns
            processed_df[col] = processed_df[col].apply(clean_text)

    return processed_df

# ----------------------------------------------------
# PREPROCESS MAIN (Controls the flow)
# ----------------------------------------------------
def preprocess_text(text=None, file_type=None, df=None):
    """
    Processes TXT/PDF using aggressive cleaning, or CSV using structured cleaning.
    Saves results in Final_data/
    """
    OUTPUT_DIR = "Final_data"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    try:
        # ---------- TXT / PDF (Aggressive Cleaning) ----------
        if file_type in ["txt", "pdf"]:
            if not text:
                return None, "Text content is missing for TXT/PDF processing."
            
            # Use the aggressive cleaner
            cleaned = clean_text(text)
            
            # Save the cleaned text
            save_path = os.path.join(OUTPUT_DIR, "processed_text.txt")
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(cleaned)
                
            return cleaned, None

        # ---------- CSV (Structured Cleaning and Imputation) ----------
        elif file_type == "csv":
            if df is None:
                return None, "CSV DataFrame missing."
            
            # Use the structured cleaner and imputation function
            processed_df = clean_csv_structured(df)
            
            # Save the processed DataFrame
            save_path = os.path.join(OUTPUT_DIR, "processed_csv.csv")
            processed_df.to_csv(save_path, index=False)

            return processed_df, None

        else:
            return None, "Unsupported file type specified."

    except Exception as e:
        return None, f"Preprocessing error: {str(e)}"
