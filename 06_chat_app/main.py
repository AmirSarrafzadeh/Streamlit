import streamlit as st

# Define a function to respond to user input
def respond(input_text):
    # Here you can implement the logic of your chatbot
    # For simplicity, let's just echo the user's input
    return f"You said: {input_text}"

# Streamlit UI
def main():
    st.title("Simple Chatbot")

    # Text input for user to type messages
    user_input = st.text_input("Enter your message:", "")

    if st.button("Send"):
        # Respond to user's input
        response = respond(user_input)
        st.text_area("Bot's response:", value=response, height=100)

if __name__ == "__main__":
    main()
