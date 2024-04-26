import streamlit as st
plh = st.container()
script = """<div id = 'chat_outer'></div>"""
st.markdown(script, unsafe_allow_html=True)

with plh:
    script = """<div id = 'chat_inner'></div>"""
    st.markdown(script, unsafe_allow_html=True)
    st.text("Random inner text")

st.text("Random outer text")

## applying style
chat_plh_style = """<style>
div[data-testid='stVerticalBlock']:has(div#chat_inner):not(:has(div#chat_outer)) {background-color: #E4F2EC};
</style>
"""

st.markdown(chat_plh_style, unsafe_allow_html=True)