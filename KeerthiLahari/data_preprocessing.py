import os
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

OUTPUT_DIR = "Final_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9.\s]", " ", text)  
    tokens = text.split()
    tokens = [t for t in tokens if t not in stop_words]
    print(tokens[:20])
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    print(tokens[:10])
    return " ".join(tokens)


def preprocess_text(text, file_type, df=None, csv_text_columns=None):
    try:
        # -------- TXT or PDF -------- #
        if file_type in ["txt", "pdf"]:
            cleaned = clean_text(text)

            save_path = os.path.join(OUTPUT_DIR, "processed_text.txt")
            with open(save_path, "w") as f:
                f.write(cleaned)

            return cleaned, None

        # -------- CSV -------- #
        if file_type == "csv":
            if csv_text_columns is None:
                csv_text_columns = \
                    df.select_dtypes(include=["object"]).columns.tolist()

            for col in csv_text_columns:
                df[col] = df[col].astype(str).apply(clean_text)

            save_path = os.path.join(OUTPUT_DIR, "processed_csv.csv")
            df.to_csv(save_path, index=False)

            return df, None

        return None, "Unsupported file type."

    except Exception as e:
        return None, f"Preprocessing error: {str(e)}"
