page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://www.shutterstock.com/image-photo/black-background-wallpaper-plain-color-photo-1567161532");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }

h1, h2, h3, h4, h5 {
    color: #ffffff !important;
    text-shadow: 1px 1px 2px #000;
    font-family: 'Poppins', sans-serif;
}

p, label, span, .stTextInput, .stTextArea {
    color: #e6e6e6 !important;
    font-size: 16px;
}

.stTextInput > div > div > input,
.stTextArea textarea {
    background-color: rgba(255,255,255,0.1) !important;
    color: white !important;
    border-radius: 8px;
}

.stButton > button {
    background-color: #6e6e6e !important;
    color: white;
    padding: 10px 22px;
    border-radius: 10px;
    border: 1px solid white;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #9a9a9a !important;
    border: 1px solid #fff;
}

div.stTabs [role="tablist"] p {
    font-size: 20px;
    font-weight: 600;
    color: white !important;
}

div.stTabs [role="tab"][aria-selected="true"] {
    background-color: rgba(255,255,255,0.15);
    border-radius: 10px;
}

div.stTabs [role="tab"] {
    background-color: rgba(255,255,255,0.05);
    margin-right: 8px;
    padding: 8px 16px;
    border-radius: 10px;
}
</style>
"""
