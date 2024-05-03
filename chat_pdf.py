
import streamlit as st
import pdfminer
from pdfminer.high_level import extract_text
import openai

# Set up the OpenAI API client
openai.api_key = "API_KEY"

# Create a Streamlit app
st.title("Quiz App")

# Allow the user to upload a PDF file
with st.sidebar.header('1. Upload your PDF file'):
    uploaded_file = st.sidebar.file_uploader("Upload your file", type=['pdf'])

pdf_text = ""
if uploaded_file is not None:
    pdf_text = extract_text(uploaded_file)

# Select interaction type
interaction_type = st.selectbox("Select interaction type", ["Ask a Question", "Generate MCQ"])

if interaction_type == "Ask a Question":
    prompt = st.text_input("Ask a question about the PDF")
    if st.button("Get Answer") and prompt:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Answer the following question based on the PDF content: {prompt}"}]
        )
        answer = response.choices[0].message["content"]
        st.write(answer)

elif interaction_type == "Generate MCQ":
    # Check if there is already a question generated and stored in session state
    if 'question' in st.session_state and 'options' in st.session_state:
        # Display the existing question and options
        st.write(f"Question: {st.session_state['question']}")
        user_answer = st.radio("Choose the correct answer:", st.session_state['options'], key="user_answer")
    
    # Button to generate a new question
    if st.button("Generate MCQ") and pdf_text:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Generate a question and four options based on the following knowledge: {pdf_text}"}]
        )
        response_text = response.choices[0].message["content"]
        question, *options = response_text.split("\n")
        st.session_state['options'] = options
        st.session_state['question'] = question
        st.session_state['correct_answer'] = options[0]  # Assuming the first option is correct

        # Redisplay the new question and options
        st.write(f"Question: {question}")
        user_answer = st.radio("Choose the correct answer:", options, key="user_answer")

    # Button to submit an answer
    if st.button("Submit Answer") and 'user_answer' in st.session_state:
        user_answer = st.session_state.user_answer
        correct_answer = st.session_state['correct_answer']
        if user_answer == correct_answer:
            st.success("Correct!")
        else:
            st.error(f"Incorrect. The correct answer is: {correct_answer}")

