#Importing necessary packages
import replicate
import streamlit as st

#Prompt for the identifying issues with the code.
code_prompt = """
You are a python coding assistant. answer the user's question accordingly. Help the user in witing clean and efficent code. Follow the rules below.
1. Do not let the user use any system libraries.
2. Identify the code issue with the code supplied below , along with the error if there is a error.
3. Consider the user question also. The user question is also given below.
While returning the answer , follow the rukes below :
1. Give only precise answers , answer to the user query , do not hallucinate.
2. if there is no error , then focus on the question and the code.
3. Provide a code snippet , followed by a simple explanation. Always adhere to this format.
User Inputs
Code : {code}
Error : {error}
Question : {question}
"""

#Prompt for generating code from user query
code_gen_prompt = """
You are a python coding assistant. The user will provide a code description. Return only the nedded code for the user description. Do not use system libraries.
Add suggestions , explanations as well. Put the code between the ```python syntax.
User query = {query}
"""

@st.cache_data
def get_gen_code(query):
    '''
    Function for generating code snippet along with the explanation for the code generated.
    '''
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

