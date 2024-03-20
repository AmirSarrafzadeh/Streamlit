import streamlit as st

# Function to perform addition
def add(x, y):
    return x + y

# Function to perform subtraction
def subtract(x, y):
    return x - y

# Function to perform multiplication
def multiply(x, y):
    return x * y

# Function to perform division
def divide(x, y):
    if y == 0:
        return "Cannot divide by Zero"
    else:
        return x / y

# Streamlit UI
def main():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images2.alphacoders.com/535/thumb-1920-535390.png"); 
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    with col2:
        st.title(":orange[Calculator]")

    num1 = st.number_input("Enter first number")

    operation = st.selectbox(
        "Select operation",
        ("Addition", "Subtraction", "Multiplication", "Division")
    )
    num2 = st.number_input("Enter second number")

    if operation == "Addition":
        result = add(num1, num2)
    elif operation == "Subtraction":
        result = subtract(num1, num2)
    elif operation == "Multiplication":
        result = multiply(num1, num2)
    elif operation == "Division":
        result = divide(num1, num2)

    if st.button("Calculate"):
        result_style = """
                <style>
                div.result {
                    font-size: 45px;
                    color: lime;
                    text-align: center;
                    position: absolute;
                    bottom: -140px;      
                    left: 50%;
                    transform: translateX(-50%); 
                }
                </style>
                """

        st.markdown(result_style, unsafe_allow_html=True)
        st.markdown(f"<div class='result'>{result}</div>", unsafe_allow_html=True)

    caption_style = """
        <style>
        div.caption {
            text-align: center;
            position: absolute;
            bottom: -200px;      
            left: 50%;
            transform: translateX(-50%); 
        }
        </style>
        """

    st.markdown(caption_style, unsafe_allow_html=True)
    st.markdown(f"<div class='caption'>Made with ❤️ by Amir</div>", unsafe_allow_html=True)
if __name__ == "__main__":
    main()
