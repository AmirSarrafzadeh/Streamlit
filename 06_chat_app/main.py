import streamlit as st
from transformers import pipeline

# Load the pre-trained model for question answering
nlp = pipeline("question-answering")


# Define a function to respond to user input
def respond(input_text, language):
    # Here we handle both normal messages and questions
    if "?" in input_text:
        # If it's a question, use the NLP model to generate an answer
        response = nlp({
            "question": input_text,
            "context": "This is a dummy context for the question-answering model. You can replace it with your own context."
        })
        return response["answer"]
    else:
        # If it's a normal message, echo it back
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
    st.sidebar.markdown("---")  # Add a horizontal line
    st.sidebar.markdown("&nbsp;")  # Add a non-breaking space (equivalent to 30px)

    # Add robot image to the bottom of sidebar
    st.sidebar.image("robot.png", use_column_width=True)


if __name__ == "__main__":
    main()
