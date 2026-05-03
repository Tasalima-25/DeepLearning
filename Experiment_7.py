# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# import streamlit as st
# import os

# load_dotenv()
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-lite",
#     google_api_key=os.getenv("Gemini_API_KEY"),
#     temperature=0.7
# )

# st.title(" AI Interview Simulator")

# if "question" not in st.session_state:
#     st.session_state.question = ""

# role = st.selectbox("Select Role:", ["Frontend", "Backend", "AI/ML", "Full Stack"])

# if st.button("Generate Question "):
#     prompt = f"Generate ONLY one short one-line technical interview question for {role} role. Do not explain. Do not add anything else."
#     response = llm.invoke(prompt)
#     st.session_state.question = response.content

# if st.session_state.question:
#     st.write("### Question:")
#     st.write(st.session_state.question)

# user_answer = st.text_area("Your Answer:")

# if st.button("Evaluate Answer ") and user_answer:
#     eval_prompt = f"""
# You are a helpful interviewer.
# Evaluate the answer briefly and clearly.
# Question: {st.session_state.question}
# Answer: {user_answer}
# Rules:
# - Keep everything short and to the point
# - Feedback: max 2 lines
# - Correct answer: max 3 lines
# - Friendly tone (not strict)

# Format:
# Feedback:
# Score:
# Correct Answer:
# Tip:
# """

#     result = llm.invoke(eval_prompt)
#     st.markdown("### Evaluation:")
#     st.markdown(result.content)


from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os

load_dotenv()

if not os.getenv("Gemini_API_KEY"):
    st.error(" API key not found. Add it in .env file")
    st.stop()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("Gemini_API_KEY"),
    temperature=0.7
)

st.title(" AI Interview Simulator")

if "question" not in st.session_state:
    st.session_state.question = ""

role = st.selectbox("Select Role:", ["Frontend", "Backend", "AI/ML", "Full Stack"])

def generate_question(role):
    prompt = f"""
Generate ONLY one short one-line technical interview question for {role} role.
Do not explain. Do not add anything else.
"""
    return llm.invoke(prompt).content

def evaluate_answer(question, answer):
    eval_prompt = f"""
You are a helpful interviewer.

Evaluate the answer in a balanced way.

Question: {question}
Answer: {answer}

Return STRICTLY in this format (use new lines exactly):

Feedback:
<your feedback>

Score:
<X>/10

Correct Answer:
<correct answer>

Tip:
<one line tip>

Do NOT write everything in one line.
"""
    return llm.invoke(eval_prompt).content

if st.button("Generate Question "):
    with st.spinner("Generating question..."):
        try:
            st.session_state.question = generate_question(role)
        except:
            st.error("Error generating question")

if st.session_state.question:
    st.markdown(f"###  Question:\n{st.session_state.question}")

user_answer = st.text_area(" Your Answer:")

if st.button("Evaluate Answer "):
    if not st.session_state.question:
        st.warning("Please generate a question first!")
    elif not user_answer:
        st.warning(" Please enter your answer!")
    else:
        with st.spinner("Evaluating answer..."):
            try:
                result = evaluate_answer(st.session_state.question, user_answer)
                st.markdown("### Evaluation:")
                st.markdown(result)
            except:
                st.error("Error evaluating answer")


if st.button("Reset "):
    st.session_state.question = ""
    st.success("Reset successful!")
