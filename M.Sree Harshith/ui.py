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

/* Labels, descriptions, small text - CRITICAL CHANGE TO BLACK FOR VISIBILITY */
label, p, span, div, li {
    color: #000000 !important; /* Ensure all primary text is black */
    font-size: 16px !important;
    font-family: 'Poppins', sans-serif;
}

/* Section headers (Before/After Preprocessing etc.) */
.block-container h3 {
    color: #2c2c2c !important;
    font-weight: 700 !important;
}

/* Text input boxes - ENSURED TEXT INSIDE IS BLACK */
.stTextArea textarea,
.stTextInput > div > div > input {
    background-color: #ffffff !important;
    color: #000000 !important; /* Ensure input text is black */
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

/* Primary Button (Used for Similarity) */
.stButton > button[kind="primary"] {
    background-color: #4CAF50 !important; /* Green for primary */
    color: white !important;
}
.stButton > button[kind="primary"]:hover {
    background-color: #45a049 !important;
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

/* CODE BOX / PREVIEW */
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

/* HTML TABLE OUTPUT - Ensure headers and data are visible */
table, th, td {
    color: #000000 !important;
    border-color: #dcdcdc !important;
}

/* Selectbox container */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;   /* white background */
    border: 1px solid #e5e7eb !important;    /* light grey border */
    border-radius: 8px !important;
}

/* Selected value text */
div[data-baseweb="select"] span {
    color: #111827 !important;               /* dark readable text */
    font-weight: 500;
}

/* Dropdown arrow */
div[data-baseweb="select"] svg {
    fill: #111827 !important;
}

/* Dropdown menu */
ul[data-baseweb="menu"] {
    background-color: #ffffff !important;
    border: 1px solid #e5e7eb !important;
}

/* Dropdown options */
li[data-baseweb="menu-item"] {
    color: #111827 !important;
    background-color: #ffffff !important;
}

/* Hover effect */
li[data-baseweb="menu-item"]:hover {
    background-color: #f3f4f6 !important;
}

/* Primary button & download button */
button[kind="primary"],
.stDownloadButton button {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.2rem !important;
}

/* Hover effect */
button[kind="primary"]:hover,
.stDownloadButton button:hover {
    background-color: #f9fafb !important;
    border-color: #d1d5db !important;
    color: #111827 !important;
}

/* Remove Streamlit shadow */
button[kind="primary"],
.stDownloadButton button {
    box-shadow: none !important;
}

/* Align icon + text nicely */
button svg {
    margin-right: 6px;
}


/* Toast / notification container */
div[data-testid="stToast"] {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08) !important;
}

/* Toast text */
div[data-testid="stToast"] p {
    color: #111827 !important;
    font-weight: 500 !important;
}

/* Toast close (X) button */
div[data-testid="stToast"] svg {
    fill: #6b7280 !important;
}

/* Toast icon */
div[data-testid="stToast"] img,
div[data-testid="stToast"] svg {
    filter: none !important;
}

/* Selectbox main input */
div[data-testid="stSelectbox"] > div {
    background-color: #ffffff !important;
    color: #111827 !important;
    border-radius: 10px !important;
    border: 1px solid #e5e7eb !important;
}

/* Dropdown menu container */
ul[role="listbox"] {
    background-color: #ffffff !important;
    border-radius: 12px !important;
    border: 1px solid #e5e7eb !important;
    box-shadow: 0 10px 28px rgba(0,0,0,0.12) !important;
}

/* Individual dropdown options */
ul[role="listbox"] li {
    background-color: #ffffff !important;
    color: #111827 !important;
    font-size: 15px !important;
}

/* Hover effect */
ul[role="listbox"] li:hover {
    background-color: #f3f4f6 !important;
    color: #fcfcfc !important;
}

/* Selected option */
ul[role="listbox"] li[aria-selected="true"] {
    background-color: #e5e7eb !important;
    color: #fcfcfc !important;
    font-weight: 600 !important;
}

/* Dropdown arrow */
div[data-testid="stSelectbox"] svg {
    fill: #fafbfc !important;
}


</style>
"""
