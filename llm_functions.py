import replicate
import os
import streamlit as st

os.environ['REPLICATE_API_TOKEN'] = "r8_YPFVKiy1WorCCageHX3HJD4iljgBNc21Z9N5q"

code_prompt = """
You are a python coding assistant. answer the user's question accordingly. Help the user in witing clean and efficent code. Follow the rules below.
1. Do not let the user use any system libraries.
2. Identify the code issue with the code supplied between <code> syntax and </code> syntax ,  and error given between <error> syntax and </error>.
3. Consider the user question also. The user question would be placed in the question <question> syntax
User Inputs
<code>{code}</code>
<error>{error}</error>
<question>{question}</question>
"""

code_gen_prompt = """
You are a python coding assistant. The user will provide a code description. Return only the nedded code for the user description.
Add suggestions , explanations as comments in the code. You should only return the code.
User query = {query}
"""
@st.cache_data
def get_gen_code(query):
    final_prompt = code_gen_prompt.format(query=query)
    input = {
                "prompt": final_prompt,
                "temperature": 0.2
            }
    response = ""
    for event in replicate.stream(
        "snowflake/snowflake-arctic-instruct",
        input=input
    ):
        response += event.data
    return response  

