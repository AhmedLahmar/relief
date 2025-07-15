import json
import os
from typing import List

import hashlib
import shutil
import networkx as nx
import nltk
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from annotated_text import annotated_text, parameters
from streamlit_extras import add_vertical_space as avs
from streamlit_extras.badges import badge

from scripts.similarity.get_score import *
from scripts.utils import get_filenames_from_dir
from scripts.utils.logger import init_logging_config

# Set page configuration
st.set_page_config(
    page_title="File Matcher",
    page_icon="Assets/img/favicon.ico",
    initial_sidebar_state="auto",
)

init_logging_config()
cwd = find_path("Resume-Matcher")
config_path = os.path.join(cwd, "scripts", "similarity")

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

parameters.SHOW_LABEL_SEPARATOR = False
parameters.BORDER_RADIUS = 3
parameters.PADDING = "0.5 0.25rem"

def create_annotated_text(
    input_string: str, word_list: List[str], annotation: str, color_code: str
):
    # Tokenize the input string
    tokens = nltk.word_tokenize(input_string)

    # Convert the list to a set for quick lookups
    word_set = set(word_list)

    # Initialize an empty list to hold the annotated text
    annotated_text = []

    for token in tokens:
        # Check if the token is in the set
        if token in word_set:
            # If it is, append a tuple with the token, annotation, and color code
            annotated_text.append((token, annotation, color_code))
        else:
            # If it's not, just append the token as a string
            annotated_text.append(token)

    return annotated_text


def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def tokenize_string(input_string):
    tokens = nltk.word_tokenize(input_string)
    return tokens

def calculate_md5_bytes(file_bytes):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file_bytes.read(4096), b""):
        hash_md5.update(chunk)
    file_bytes.seek(0)  # reset pointer
    return hash_md5.hexdigest()

def is_duplicate_bytes(file_bytes, repo_folder):
    file_hash = calculate_md5_bytes(file_bytes)
    for existing_file in os.listdir(repo_folder):
        existing_file_path = os.path.join(repo_folder, existing_file)
        if os.path.isfile(existing_file_path):
            with open(existing_file_path, "rb") as f:
                existing_file_hash = calculate_md5_bytes(f)
            if file_hash == existing_file_hash:
                return True
    return False

def insert_file_and_check_duplicate(uploaded_file):
    if uploaded_file is None:
        st.warning("Please upload a file to insert.")
        return

    repo_folder = "files_repo"
    os.makedirs(repo_folder, exist_ok=True)

    if is_duplicate_bytes(uploaded_file, repo_folder):
        st.error("❌ Duplicate file detected. The file was not added.")
    else:
        filename = uploaded_file.name
        destination_path = os.path.join(repo_folder, filename)
        with open(destination_path, "wb") as out_file:
            out_file.write(uploaded_file.read())
        st.success(f"✅ File '{filename}' inserted successfully into '{repo_folder}'.")

# --------------- File Insertion with st.file_uploader ---------------
st.markdown("## 📄 Insert File to Repository")

uploaded_file = st.file_uploader("Upload a file to insert", type=["pdf", "docx", "txt", "json"])
if st.button("Insert File"):
    insert_file_and_check_duplicate(uploaded_file)

avs.add_vertical_space(2)
#resume_names = get_filenames_from_dir("Data/Processed/Resumes")


# st.markdown(
#     f"##### There are {len(resume_names)} files present. Please select one from the menu below:"
# )
# output = st.selectbox(f"", resume_names)


avs.add_vertical_space(3)

# st.write("You have selected ", output, " printing the resume")
# selected_file = read_json("Data/Processed/Resumes/" + output)

# avs.add_vertical_space(2)
# st.markdown("#### Parsed File Data")
# # st.caption("Utilize this to understand how to make your resume ATS friendly.")
# avs.add_vertical_space(3)
# # st.json(selected_file)
# st.write(selected_file["clean_data"])

# avs.add_vertical_space(3)


# annotated_text(
#     create_annotated_text(
#         selected_file["clean_data"],
#         selected_file["extracted_keywords"],
#         "KW",
#         "#0B666A",
#     )
# )



avs.add_vertical_space(5)


st.markdown("[:arrow_up: Back to Top](#resume-matcher)")
