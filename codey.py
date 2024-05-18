#Importing necessary packages
import streamlit as st
import io
from contextlib import redirect_stdout
from streamlit_ace import st_ace
import replicate
from llm_functions import *
import os
from streamlit_float import *
import re

#Setting the Replicate token
os.environ['REPLICATE_API_TOKEN'] = st.secrets['REPLICATE_KEY']

#Setting page configurations
st.set_page_config(layout="wide")
float_init(theme=True, include_unstable_primary=False)

@st.experimental_dialog("Welcome to Codey")
def tutorial():
    '''
    Function for providing user a guided tutorial on how to use the app

    '''
    st.write("Introducing Codey, your all-in-one personal Python assistant and integrated development environment (IDE)")
    st.video("src/intro.mov",autoplay=True,loop=True)
    st.write("Codey is designed to streamline your coding experience, offering intelligent assistance, real-time code suggestions, and debugging help, all within a robust and user-friendly IDE. Whether you're a seasoned developer or just starting out, Codey enhances productivity, allowing you to focus on writing great code with fewer interruptions.")
    st.subheader("""To get started , ask your python queries in this text area , and click the "Generate Solution" button.""")
    st.image("src/landing.png")
    st.write("""Codey will automatically , generate the code and will place in the IDE as given below. You can also try out the code by clicking the Apply button.
             Note that not all packages might be installed , but we do have most of the DE/DS pacakages built in. If you face any issues in the code , you can ask it to the Codey assistant on the right hand side.""")
    st.image("src/gui.png")
    read_button = st.button("Got it!")
    if read_button:
        st.session_state.tutorial = True
        st.rerun()
    else:
        st.session_state.tutorial = False


if "tutorial" not in st.session_state:
    tutorial()

st.header("Codey - Coding Assistant",divider="blue")

#Checking if the user has read the tutorial , if not providing a warning
if not st.session_state.tutorial:
    st.warning("Please read the tutorial")
    if st.button("Teach me"):
        tutorial()

#Codey UI 1 - Space for writing the user query , contains a text area followed by a button
st.write("Welcome to Codey , your very own python coding assistant  , powered by Snowflake Artic. ")
code_req =  st.text_area(label="Write a brief description of the code requirement")
if st.button(label="Generate Solution"):
    st.session_state.button = True

#Codey UI 2 - Once the user enters the query and clicks the button , code ia autodenerated using Artic and is filled in the ace code editor
if "button" in st.session_state:
    if st.session_state.button:
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
                #Code for simulating a terminal , using the exec function to run the code and io functions to get the exec out.
                #Prompt engineering has been done to avoid using system libraries
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
            #Code Sub UI - A live chat interface to identify bugs in the code , powered by Artic
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
                            placheolder.markdown(response.strip("```{}"))
