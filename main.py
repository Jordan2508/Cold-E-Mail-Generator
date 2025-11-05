import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def set_background():
    # HTML background injection (works in all Streamlit versions)
    page_bg_img = """
    <style>
    body {
        background-image: url("https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=2000&q=80");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        background-color: orange;
    }

    /* Add a translucent white card effect to the main content */
    [data-testid="stAppViewContainer"] > .main {
        background: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 0 20px rgba(0,0,0,0.2);
    }

    /* Title styling */
    .title {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        color: #1a1a1a;
        text-align: center;
        text-shadow: 1px 1px 3px rgba(255,255,255,0.8);
        margin-bottom: 2rem;
    }

    /* Input field */
    .stTextInput > div > div > input {
        background-color: #ffffffcc;
        color: #000;
        border-radius: 10px;
        font-size: 1rem;
        padding: 0.6rem 1rem;
        border: 1px solid #ddd;
    }

    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #ff4b4b, #ff7b00);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.7rem 1.4rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #ff2e2e, #ff5a00);
    }

    /* Code block styling */
    pre {
        background-color: #1a1a1a !important;
        color: #00ffb3 !important;
        border-radius: 10px;
        font-size: 0.95rem;
        padding: 1rem !important;
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)


def create_streamlit_app(llm, portfolio, clean_text):
    set_background()

    st.markdown("<div class='title'>📧 Cold Mail Generator</div>", unsafe_allow_html=True)

    url_input = st.text_input(
        "Enter a Job URL:",
        value="https://careers.nike.com/machine-learning-engineer/job/R-70336"
    )
    submit_button = st.button("Generate Email")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            for job in jobs:
                skills = job.get("skills", [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language="markdown")

        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)




