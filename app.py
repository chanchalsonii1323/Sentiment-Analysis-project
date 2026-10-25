import streamlit as st
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(
    page_title="Sentiment Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sentiment Analysis Project")
st.write("Analyze the sentiment of any review.")

analyzer = SentimentIntensityAnalyzer()

review = st.text_area(
    "Enter your review",
    placeholder="Example: This book is amazing!"
)

if st.button("Analyze Sentiment"):
    if review.strip():
        score = analyzer.polarity_scores(review)["compound"]

        if score >= 0.05:
            sentiment = "Positive 😊"
        elif score <= -0.05:
            sentiment = "Negative 😞"
        else:
            sentiment = "Neutral 😐"

        st.subheader("Analysis Result")
        st.success(f"Sentiment: {sentiment}")
        st.metric("Sentiment Score", round(score, 3))
    else:
        st.warning("Please enter a review first.")

st.divider()
st.subheader("Project Files")

try:
    df = pd.read_csv("sentiment_results.csv")
    st.write("Sample sentiment analysis results")
    st.dataframe(df.head(20), use_container_width=True)
except FileNotFoundError:
    st.info("Sample results file is not available.")
