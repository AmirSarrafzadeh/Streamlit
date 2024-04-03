import io
import sys
import streamlit as st

# Create a sidebar and a tab
st.sidebar.header("🚀 Python Course 😉")
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #4682B4; 
}
</style>
""", unsafe_allow_html=True)

zoomcamp_expander = st.sidebar.expander("Variables definitions")

with zoomcamp_expander:
    zoomcamp_tab = st.empty()
    st.subheader("Variables in Python")
    st.write("**Strings:**")
    st.code('name = "Alice"')
    st.write("**Numbers:**")
    st.write("- **Integers:**  Whole numbers")
    st.write("- **Floats:**  Numbers with decimals")
    st.code('age = 25  # Integer\ntemperature = 98.6  # Float')
    st.write("**Booleans:** True or False.")
    st.code('is_enrolled = True\nis_active = False')
    st.write("**Lists:**")
    st.code('course_modules = ["Benz", "BMW", "Audi"]')
    st.write("**Dictionaries:**")
    st.code('student = {"name": "Bob", "city": "New York"}')

st.markdown("<h1 style='text-align: center;'>Python Course</h1>", unsafe_allow_html=True)

st.markdown("""
<style>
.center-link {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 1vh;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
            <div class="center-link">
              <a href="https://www.python.org/">Python 🐍</a>
            </div>
            """, unsafe_allow_html=True)

st.subheader("Python Code Simulator")
code_input = st.text_area("Write your Python code here:", height=200)

if st.button("Run Code"):
    try:
        stdout_buffer = io.StringIO()
        sys.stdout = stdout_buffer

        exec(code_input)
        output_value = stdout_buffer.getvalue()

        sys.stdout = sys.__stdout__

        st.write("Output:")
        for line in output_value.split("\n"):
            st.write(line)

    except Exception as e:
        st.error(f"An error occurred: {e}")
