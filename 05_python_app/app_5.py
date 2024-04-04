import io
import sys
import streamlit as st

st.sidebar.header("🚀 Python Course Materials 😉")

# Define sidebar state
selected_option = st.sidebar.radio("Select Sidebar", ["Variables", "Statements", "Loops", "Functions", "Tasks"])

if selected_option == "Variables":
    selected_variable_option = st.sidebar.radio("Variables", ["Strings", "Numbers", "Boolean", "Lists", "Tuples", "Dictionaries", "Sets"])

    # Display content based on selected option
    if selected_variable_option == "Strings":
        st.title("Strings Documentation")
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

    elif selected_variable_option == "Numbers":
        st.write("You selected Option 2")

    elif selected_variable_option == "Boolean":
        st.write("You selected Option 3")

elif selected_option == "Tasks":
    selected_task_option = st.sidebar.radio("Tasks", ["Task 1", "Task 2", "Task 3"])

    # Display content based on selected task
    if selected_task_option == "Task 1":
        st.title("Write a Python program to check if a number is prime or not.")
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
        st.subheader("Python Code Simulator")
        code_input = st.text_area("Write your Python code here:", height=200)

        st.markdown("""
            <div class="center-link">
              <a href="https://docs.python.org/3/library/string.html/">Strings documentation in Python 🐍</a>
            </div>
            """, unsafe_allow_html=True)

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

caption_style = """
<style>
div.caption {
    text-align: center;
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
}
</style>
"""

st.markdown(caption_style, unsafe_allow_html=True)
st.markdown(f"<div class='caption'>Made with ❤️ by Amir</div>", unsafe_allow_html=True)
