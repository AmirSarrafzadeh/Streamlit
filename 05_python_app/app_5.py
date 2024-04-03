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

zoomcamp_expander = st.sidebar.expander("Variables Documentation")
selected_tab = st.sidebar.radio("Select a Tab:", ["Python Documentation", "Tasks"])


if selected_tab == "Python Documentation":
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

elif selected_tab == "Tasks":
    task_expander = st.sidebar.expander("Tasks")
    with task_expander:
        task_1 = st.button("Task 01")
        task_2 = st.button("Task 02")
        task_3 = st.button("Task 03")

    st.markdown("<h1 style='text-align: center;'>Tasks</h1>", unsafe_allow_html=True)

    # Logic to handle what happens when clicking on each task button
    if task_1:
        st.markdown("You clicked Task 01. (Page content for Task 01 would go here)")
    elif task_2:
        st.markdown("You clicked Task 02. (Page content for Task 02 would go here)")
    elif task_3:
        st.markdown("You clicked Task 03. (Page content for Task 03 would go here)")

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

