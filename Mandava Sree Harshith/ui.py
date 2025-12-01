page_bg = """
<style>

[data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
}

/* Header */
[data-testid="stHeader"] {
    background-color: #ffffff !important;
    border-bottom: 1px solid #e0e0e0;
}

/* Main Page Title */
h1, h2 {
    text-align: center !important;
    color: #111111 !important;
    font-family: 'Poppins', sans-serif;
    font-weight: 700 !important;
}

/* Labels, descriptions, small text */
label, p, span {
    color: #4d4d4d !important;
    font-size: 16px !important;
    font-family: 'Poppins', sans-serif;
}

/* Section headers (Before/After Preprocessing etc.) */
.block-container h3 {
    color: #2c2c2c !important;
    font-weight: 700 !important;
}

/* Text input boxes */
.stTextArea textarea,
.stTextInput > div > div > input {
    background-color: #ffffff !important;
    color: #2b2b2b !important;
    border-radius: 8px;
    border: 1px solid #505050 !important;
}

/* Buttons */
.stButton > button {
    background-color: #c8d2e0 !important;
    color: white !important;
    padding: 10px 24px;
    border-radius: 10px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background-color: #c0c5cc !important;
}

/* Tabs */
div.stTabs [role="tablist"] p {
    font-size: 18px;
    font-weight: 600;
    color: #333 !important;
}

/* Center tab navigation */
.stTabs [data-baseweb="tab-list"] {
    justify-content: center;
}

div.stTabs [role="tab"][aria-selected="true"] {
    background-color: #e6f0ff !important;
    border-radius: 10px;
}

div.stTabs [role="tab"] {
    background-color: #f3f3f3 !important;
    padding: 8px 16px;
    border-radius: 10px;
}

/* FILE UPLOADER BOX */
[data-testid="stFileUploader"] section {
    background-color: #f3f3f3 !important;
    color: #000 !important;
    border: 1px solid #ccc !important;
    border-radius: 10px;
    padding: 12px;
}

/* Browse button */
[data-testid="stFileUploader"] button {
    background-color: #d9d9d9 !important;
    color: #000000 !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
}

[data-testid="stFileUploader"] button:hover {
    background-color: #c4c4c4 !important;
}

/* FILE NAME TEXT */
[data-testid="stFileUploader"] div[role="textbox"] span {
    color: #26282b !important;
    font-weight: 600 !important;
}

/* FILE SIZE TEXT */
[data-testid="stFileUploader"] small {
    color: #444444 !important;
    font-weight: 600 !important;
}

/* ---------------------------------------------- */
/* FIX BLACK CODE BOX → MAKE IT LIGHT LIKE CARDS */
/* ---------------------------------------------- */

.stCodeBlock, pre, code {
    background-color: #f3f3f3 !important;
    color: #111 !important;
    border-radius: 10px !important;
    padding: 12px !important;
    border: 1px solid #dcdcdc !important;
    font-size: 16px !important;
}

/* Output inside markdown */
[data-testid="stMarkdownContainer"] pre {
    background-color: #f3f3f3 !important;
    color: #111 !important;
    border-radius: 10px !important;
    border: 1px solid #dcdcdc !important;
}

</style>
"""
