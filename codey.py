import streamlit as st
import io
from contextlib import redirect_stdout
from streamlit_ace import st_ace
import replicate
from llm_functions import *
import os
from streamlit_float import *
import re

st.set_page_config(layout="wide")
float_init(theme=True, include_unstable_primary=False)

os.environ['REPLICATE_API_TOKEN'] = st.secrets['REPLICATE_KEY']

st.header("Codey - Coding Assistant",divider="blue")
st.write("Welcome to Codey , your very own python coding assistant  , powered by Snowflake Artic. ")
code_req =  st.text_area(label="Write a brief description of the code requirement")
if code_req:
    code_gen = get_gen_code(code_req)
    python_matches = re.findall(r"```python\n(.*?)\n```", code_gen, re.DOTALL)
    if len(python_matches)>0:
        python_code = "\\n".join(python_matches)
    else:
        python_code = ""
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            with st.container():
                content = st_ace(value=python_code,language="python")
            with st.container(border=True):
                st.write("Terminal")
                stdout = io.StringIO()
                try:
                    with redirect_stdout(stdout):
                        exec(content)

                    out = stdout.getvalue()
                    error = 'No error'
                except Exception as e:
                    out=e
                    error = e
                st.markdown(out)

        with c2:
            with st.container(border=True):
                placheolder = st.empty()
                with st.chat_message('assistant'):
                    placheolder.markdown(code_gen)
                with st.container():
                    button_b_pos = "0rem"
                    button_css = float_css_helper(width="2.2rem", bottom=button_b_pos, transition=0)
                    float_parent(css=button_css)
                    prompt = st.chat_input("Any queries , let's chat !")
                if prompt:
                    placheolder.empty()
                    final_prompt = code_prompt.format(question=prompt,code=content,error=error)
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
                        placheolder.markdown(response)
