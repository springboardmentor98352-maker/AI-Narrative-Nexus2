import streamlit as st
from streamlit_option_menu import option_menu
from data_extractor import extract_text_from_file
from data_preprocessing import preprocess_text


# ---------- GLOBAL CSS FIXES ------------
st.markdown("""
<style>
/* Remove Streamlit's default top padding */
.block-container {
    padding-top: 1rem !important;
}

/* Center alignment for all required text */
.center-text {
    text-align: center;
}

/* Optional: increase spacing between sections */
.spacing {
    margin-top: -20px;
}
</style>
""", unsafe_allow_html=True)

# -----------settings----------------
title = "Narrative Nexus"
caption = "Dynamic Text Analysis Platform"
subheader = " summarise . Analyze . Get Insights "
icon = "🧠"
layout = "centered"

# -------------Heading part-------------------------
st.set_page_config(page_title=title, page_icon=icon, layout=layout)
st.markdown(f"<h1 class='center-text'>{title} {icon}</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 class='center-text spacing'>{caption}</h3>", unsafe_allow_html=True)
st.markdown(f"<p class='center-text spacing'>{subheader}</p>", unsafe_allow_html=True)

# ----------- Navigation Menu --------------
selected = option_menu(
            menu_title=None,
            options=["About", "Text Input", "Text Analysis"],
            icons=["house", "upload", "bar-chart"],
            default_index=0,
            orientation="horizontal",
)
# -------------About Section-----------------
if selected == "About":
    st.subheader("About Narrative Nexus")
    entered_text = """
    <div style="text-align: Justify;font:arial; font-size:20px;">
    Narrative Nexus is a dynamic text analysis platform designed to help users quickly summarize content,
    measure word and character counts, evaluate sentiment, and generate meaningful insights from any text.
    The application supports text uploads and manual input, processes data efficiently, and delivers clearly
    structured results that can be downloaded for further use. With features ranging from automated summarization
    to sentiment distribution visualization, Narrative Nexus provides a simple yet powerful tool for students,
    researchers, professionals, and anyone looking to understand and refine their written content with ease.
    </div>
    """
    st.markdown(entered_text, unsafe_allow_html=True)

# -------------Text Input Section----------------
elif selected == "Text Input":

    st.subheader("Upload a file OR paste text")

    uploaded_file = st.file_uploader("Upload TXT / CSV / PDF", type=["txt", "csv", "pdf"])
    pasted_text = st.text_area("Or paste text here...", height=200)

    if st.button("Process Text"):
        raw_text, file_type, df_data, error = extract_text_from_file(
            uploaded_file=uploaded_file,
            pasted_text=pasted_text
        )

        if error:
            st.error(error)

        else:
            st.success(f"Extracted ({file_type.upper()}) successfully!")

            # ---- FILE-TYPE BASED PREPROCESSING ---- #
            if file_type in ["txt", "pdf"]:
                processed, err = preprocess_text(raw_text, file_type)
                if err:
                    st.error(err)
                else:
                    st.success("Preprocessing complete!")
                    st.write(processed[:2000])

            elif file_type == "csv":
                processed_df, err = preprocess_text(
                    text=None,
                    file_type="csv",
                    df=df_data
                )
                if err:
                    st.error(err)
                else:
                    st.success("CSV preprocessing complete!")
                    st.dataframe(processed_df.head())

            st.info("➡ Move to the 'Text Analysis' tab for insights.")

# ---------------- TEXT ANALYSIS ------------------
elif selected == "Text Analysis":
    st.subheader("Results will appear here after processing.")
    st.info("Since session_state is removed, copy-paste your processed text here to analyze it.")