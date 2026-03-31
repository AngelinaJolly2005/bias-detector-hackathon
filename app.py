import os
from dotenv import load_dotenv

# This line finds the .env file and loads the key into your system
load_dotenv()

# This line grabs the key so Gemini can use it
api_key = os.getenv("GOOGLE_API_KEY")
import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
from bias_detector import calculate_bank_fairness

# Load API Key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="SafeLoan AI", page_icon="🏦")
st.title("🏦 SafeLoan: Smart AI Fairness Auditor")

uploaded_file = st.file_uploader("Upload Bank Loan Data (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview", df.head())

    target = st.selectbox("Select Decision Column (e.g., Approved)", df.columns)
    protected = st.selectbox("Select Sensitive Group (e.g., Gender)", df.columns)

    if st.button("Run Full Audit"):
        results = calculate_bank_fairness(df, target, protected)
        
        # Display Metrics
        st.metric("Fairness Score", f"{results['impact_ratio']:.2f}")
        st.bar_chart(results['group_rates'])

        # --- ASK GEMINI FOR ADVICE ---
        st.subheader("🤖 AI Auditor Recommendations")
        with st.spinner("Gemini is analyzing the legal risks..."):
            prompt = f"""
            As a Banking Compliance Officer, analyze these results:
            - The fairness ratio for {protected} is {results['impact_ratio']:.2f}.
            - A score below 0.80 indicates illegal bias.
            Provide a 3-sentence summary of the risk and one specific fix.
            """
            response = model.generate_content(prompt)
            st.info(response.text)

