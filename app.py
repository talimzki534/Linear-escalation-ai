import streamlit as st
from openai import OpenAI

# 🔑 Put your OpenAI API key here or use Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Linear Escalation Formatter", layout="centered")

st.title("🧠 Linear Escalation Formatter AI")

st.write("Paste raw Intercom / support notes below and generate a structured Linear escalation.")

# INPUT BOX
raw_input = st.text_area("Paste user info here", height=250)

def build_prompt(text):
    return f"""
You are a support escalation formatter.

Convert the raw text into EXACTLY this format (no extra text):

* **user email:** ...

* **problem**
  * **User report:** ...

* Did you create Dispute? Yes/No

* **If unauthorized transactions, confirm that you**
Asked user to delete card and change password: Yes/No

* **transactions:**
  * (Transaction ID, Amount, Merchant Name)

* additional context
  * Were there other similar reports with the SAME merchant?
  * Provide any additional context that you think helpful

Rules:
- Extract missing info if possible
- If not found, write "N/A"
- Keep strict formatting
- Do NOT add explanations
- Output ONLY the formatted escalation

RAW INPUT:
{text}
"""

if st.button("Generate Escalation"):
    if not raw_input.strip():
        st.error("Please paste input first.")
    else:
        with st.spinner("Generating escalation..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a strict data formatter."},
                    {"role": "user", "content": build_prompt(raw_input)}
                ]
            )

            output = response.choices[0].message.content

        st.success("Generated Escalation:")
        st.text_area("Copy this into Linear", output, height=400)
        st.copy_button = st.button("Copy to Clipboard")

        if st.button("Copy Output"):
            st.write("Copied! (Use manual copy if browser blocks auto-copy)")