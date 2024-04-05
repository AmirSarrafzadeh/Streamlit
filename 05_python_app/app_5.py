import io
import sys
import streamlit as st

st.sidebar.header("🚀 Python Course Materials 😉")

# Define sidebar state
selected_option = st.sidebar.radio("Select Sidebar", ["Variables", "Statements", "Loops", "Functions", "Tasks"])

if selected_option == "Variables":
    selected_variable_option = st.sidebar.radio("Variables", ["Strings", "Numbers", "Boolean", "Lists", "Tuples", "Dictionaries", "Sets"])

    if selected_variable_option == "Strings":
        st.title("Strings Documentation")

        st.write("""
        **Strings in Python**

        * Strings represent sequences of characters enclosed in quotes (single, double, or triple).
        * You can create, manipulate, and format strings in many ways. 

        **Examples:**
        ```python
        name = "Alice"
        print(name)
        message = 'Hello, world!'
        print(message)
        long_text = "This is a multi-line string."
        print(long_text)
        ```
        
        **Output:**
        ```
        Alice
        Hello, world!
        This is a multi-line string.
        ```
        
        **String Operations:**
        * Concatenation: `str1 + str2`
        * Repetition: `str * n`
        * Slicing: `str[start:end]`
        * Length: `len(str)`
        * Formatting: `f"Hello, {name}!"`
        
        **String Methods:**
        * `upper()`, `lower()`, `capitalize()`
        * `strip()`, `lstrip()`, `rstrip()`
        * `replace()`, `split()`, `join()`
        * `find()`, `count()`, `startswith()`, `endswith()`
        
        **Escape Sequences:**
        * `\\` - Backslash
        * `\'` - Single quote
        * `\"` - Double quote
        * `\n` - Newline
        * `\t` - Tab
        * `\b` - Backspace
        * `\r` - Carriage return
        
        **String Formatting:**
        * `%` operator
        * `str.format()`
        * f-strings (Python 3.6+)
        
        **String Indexing:**
        * Strings are indexed from 0 to n-1
        * Negative indexing: -n to -1
        * Slicing: str[start:end:step]
        
        **String Methods:**
        * `upper()`, `lower()`, `capitalize()`
        * `strip()`, `lstrip()`, `rstrip()`
        * `replace()`, `split()`, `join()`
        * `find()`, `count()`, `startswith()`, `endswith()`
        
        **String Formatting:**
        * `%` operator
        * `str.format()`
        * f-strings (Python 3.6+)
        
        """)

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
              <a href="https://docs.python.org/3/library/string.html/">Strings documentation in Python 🐍</a>
            </div>
            """, unsafe_allow_html=True)

    elif selected_variable_option == "Numbers":
        st.title("Numbers Documentation")

        st.write("""
        **Numbers in Python**

        Python supports two main types of numbers:

        * **Integers (int):** Whole numbers without decimals (e.g., 10, -5, 0)
        * **Floating-point numbers (float):** Numbers with decimals (e.g., 3.14, -10.5)

        **Examples:**
        ```python
        age = 25          # Integer
        temperature = 98.6  # Float
        pi = 3.14159      # Float
        ```
        """)

    elif selected_variable_option == "Boolean":
        st.title("Booleans Documentation")

        st.write("""
        **Booleans in Python**

        Booleans represent logical values: True or False. They are often used in conditional statements and comparisons.

        **Examples:**
        ```python
        is_adult = age >= 18
        is_empty = len(my_list) == 0
        ```
        """)

    elif selected_variable_option == "Lists":
        st.title("Lists Documentation")

        st.write("""
        **Lists in Python**

        Lists are ordered collections of items. They can contain elements of different data types. Lists are mutable, meaning you can change them after creation.

        **Examples:**
        ```python
        numbers = [1, 2, 3, 4]
        names = ["Alice", "Bob", "Charlie"]
        mixed_list = [10, "hello", True]
        ```
        """)

    elif selected_variable_option == "Tuples":
        st.title("Tuples Documentation")

        st.write("""
        **Tuples in Python**

        Tuples are similar to lists, but they are immutable, meaning you cannot change their elements after creation. They are defined using parentheses.

        **Examples:**
        ```python
        coordinates = (10, 20)
        colors = ("red", "green", "blue")
        ```
        """)

# ... (Dictionaries and Sets - Add documentation)

elif selected_option == "Tasks":
    selected_task_option = st.sidebar.radio("Tasks", ["Task 1", "Task 2", "Task 3"])

    if selected_task_option == "Task 1":
        st.title("Calculate the Fibonacci Sequence")
        st.write("""
                **Task Description:** The Fibonacci sequence is a series where each number is the sum of the two preceding ones (starting from 0 and 1).

                **Instructions:** Write a Python program to calculate and display the first 10 numbers of the Fibonacci sequence.
                """)

    elif selected_task_option == "Task 2":
        st.title("Calculate the Fibonacci Sequence")
        st.write("""
        **Task Description:** The Fibonacci sequence is a series where each number is the sum of the two preceding ones (starting from 0 and 1).

        **Instructions:** Write a Python program to calculate and display the first 10 numbers of the Fibonacci sequence.
        """)

    elif selected_task_option == "Task 3":
        st.title("Find the Factorial of a Number")
        st.write("""
        **Task Description:** The factorial of a number is the product of all positive integers less than or equal to it. 

        **Instructions:** Write a Python program to calculate the factorial of a number entered by the user.
        """)
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
