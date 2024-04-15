import streamlit as st


# Define a function to respond to user input
def respond(input_text, language):
    # Here you can implement the logic of your chatbot
    # For simplicity, let's just echo the user's input
    return f"You said: {input_text} (in {language})"


# Streamlit UI
def main():
    st.title("Simple Chatbot")

    # Sidebar for additional controls
    st.sidebar.title("Settings")
    language = st.sidebar.selectbox("Select Language:", ["English", "Spanish", "French"], index=0)

    # Text input for user to type messages
    user_input = st.text_input("Enter your message:", "")

    if st.button("Send"):
        # Respond to user's input
        response = respond(user_input, language)
        st.text_area("Bot's response:", value=response, height=100)

    # Add space between sidebar content and image
    st.sidebar.markdown("---")
    st.sidebar.markdown("&nbsp;")

    # Add robot image to the bottom of sidebar
    st.sidebar.image("robot.png", use_column_width=True)


if __name__ == "__main__":
    main()
