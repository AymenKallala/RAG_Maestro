import streamlit as st
from streamlit_chat import message
from PIL import Image
from utils.load_config import LoadConfig
from utils.app_utils import load_data, RAG, delete_data
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import CitationQueryEngine
from pyprojroot import here
import subprocess
import os


APPCFG = LoadConfig()

# ===================================
# Setting page title and header
# ===================================
im = Image.open("images/mithril_security_company_logo.jpeg")

st.set_page_config(page_title="FinancialGPT", page_icon=im, layout="wide")
st.markdown("<h1 style='text-align: center;'>FinancialGPT</h1>", unsafe_allow_html=True)
st.divider()
st.markdown(
    "<a style='display: block; text-align: center;' href='https://aymenkallala.github.io/' target='_blank'> Aymen Kallala</a>",
    unsafe_allow_html=True,
)
st.divider()

# ===================================
# Initialise session state variables
# ===================================
if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

# ==================================
# Sidebar:
# ==================================
counter_placeholder = st.sidebar.empty()
with st.sidebar:
    openai_token=st.text_input(label='OPENAI API KEY',value = None,type = 'password')
    if openai_token:
            os.environ['OPENAI_API_KEY'] = openai_token
    st.markdown(
        "<h3 style='text-align: center;'>Ask a financial question that can be found in the latest news.</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<center><i>Example: What is the equities market outlook for 2024?</i></center>",
        unsafe_allow_html=True,
    )
    # st.sidebar.title("An agent that read and summarizethe the news for you")
    st.sidebar.image("images/mithril_security_company_logo.jpeg", use_column_width=True)
    news_source = st.sidebar.radio("Pick a source:", ("Finance specific (Investopedia.com)", "Global News (CNBC.com)"))
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
# ==================================
# Reset everything (Clear button)
if clear_button:
    st.session_state["generated"] = []
    st.session_state["past"] = []
    delete_data()
if news_source == "Finance specific (Investopedia.com)":
    source = "investopedia"
if news_source == "Global News (CNBC.com)":
    source = "cnbc"

response_container = st.container()  # container for message display

if query := st.chat_input("What do you want to know? I will check the news for you."):
    st.session_state["past"].append(query)
    if openai_token == None:
         message("No API token provided! Please enter a valid key in the left top button.", is_user=False)
    if source == None:
         message("Please pick a source of information to browse in.", is_user=False)


    else:
        try:
            process = subprocess.Popen(
                f"python src/utils/scraper.py --query '{query}' --sources {source} --numresults {APPCFG.articles_to_search}",
                shell=True,
            )
            out, err = process.communicate()
            errcode = process.returncode

            with st.spinner("Searching the web..."):
                data = load_data()
                index = RAG(APPCFG, _docs=data)
                query_engine = index.as_query_engine(
                    response_mode="tree_summarize",
                    verbose=True,
                    similarity_top_k=APPCFG.similarity_top_k,
                )
            with st.spinner("Thinking..."):
                response = query_engine.query(query + APPCFG.llm_format_output)

            st.session_state["generated"].append(response.response)
            del index
            del query_engine

            with response_container:
                for i in range(len(st.session_state["generated"])):
                    message(st.session_state["past"][i], is_user=True)

                    message(st.session_state["generated"][i], is_user=False)

        except Exception as e:
            print(e)
            st.session_state["generated"].append(
                "An error occured with the web search, please modify your query."
            )
