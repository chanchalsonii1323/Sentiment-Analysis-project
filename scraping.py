import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Website URL
url = "https://books.toscrape.com/"

# Page 1 open karo
response = requests.get(url)

# HTML read karo
soup = BeautifulSoup(response.text, "html.parser")

# Page 2 ka link nikalo
next_page = soup.find("li", class_="next").a["href"]

# Page 2 ka complete URL banao
next_url = urljoin(url, next_page)

print("NEXT URL:", next_url)

# Page 2 open karo
next_response = requests.get(next_url)
next_soup = BeautifulSoup(next_response.text, "html.parser")

# Page 1 books
books = soup.find_all("article", class_="product_pod")

# Page 2 books
next_books = next_soup.find_all("article", class_="product_pod")

# Data list
data = []

# Rating mapping
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

# Page 1 ka data
for book in books:
    name = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    rating = book.find("p", class_="star-rating")["class"][1]

    rating = rating_map[rating]

    data.append([name, price, rating])

# Page 2 ka data
for book in next_books:
    name = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    rating = book.find("p", class_="star-rating")["class"][1]

    rating = rating_map[rating]

    data.append([name, price, rating])

# Total books
print("Total books:", len(data))

# Average rating
total_rating = sum(row[2] for row in data)
average_rating = total_rating / len(data)

print("Average Rating:", average_rating)

# Most expensive book
expensive_book = max(
    data,
    key=lambda x: float(x[1].replace("£", "").replace("Â", "").strip())
)

print("Most Expensive Book:", expensive_book)

# print most expensive book
highest_rated = max(data, key=lambda x: x[2])

print("Highest Rated Book:", highest_rated)
print("Book Name:", highest_rated)

# CSV file banana
with open("books.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["Book Name", "Price", "Rating"])
    writer.writerows(data)

print("Data saved to books.csv")

import pandas as pd

df = pd.read_csv("books.csv", encoding="latin1")

# Column names ke extra spaces remove
df.columns = df.columns.str.strip()

df["Price"] = df["Price"] .astype(str).str.extract(r"(\d+\.?\d*)", expand=False).astype(float)
print("\nCleaned Price:")

print(df["Price"].head())

print("\nAverage Price", df["Price"].mean())

print("\nMinimum Price:",df["Price"].min())

cheapest_index = df["Price"].idxmax()

print("Cheapest Book:", df.loc[cheapest_index, "Book Name"])

print("nHighest Rating:", df["Rating"]. max())
highest_rating = df["Rating"].max()
print("\nHighest Rated Books:")
print(df[df["Rating"] == highest_rating][["Book Name", "Rating"]])

print("\nRating Distribution:")
print("\nDuplicate Rows:")
print("\nAverage Price by Rating:")
print(df.groupby("Rating")["Price"].mean())
print(df.duplicated().sum())
print(df["Rating"]. value_counts(). sort_index())


print("\nDataset Information:")
print(df.info())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull(). sum())

print("Columns:", df.columns.tolist())

print("\nFirst 5 Books:")
print(df.head())

print("\nTotal books:", len(df))

print("\nAverage Rating:", df["Rating"].mean())

# Price clean
price = pd.to_numeric(
    df["Price"].astype(str).str.extract(r"(\d+\.?\d*)")[0],
    errors="coerce"
)

print("\nMaximum Price:", price.max())

# Most expensive book
index = price.idxmax()

print("\nMost Expensive Book:")
print(df.iloc[index, 0])
print("Price:", price.loc[index])

# Highest rated book
rating_index = df["Rating"].idxmax()

print("\nHighest Rated Book:")
print(df.iloc[rating_index, 0])
print("Rating:", df.loc[rating_index, "Rating"])


import matplotlib.pyplot as plt

rating_counts = df["Rating"].value_counts().sort_index()
rating_counts.plot(kind="bar")

plt.title("Books by Rating")
plt.xlabel("Rating")
plt.ylabel("Number of books")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("rating_chart.png")
plt.show()


print("\nMost Common Rating :")
print(df["Rating"].mode()[0])

print("\nBooks Count by Rating :")
print(df["Rating"].value_counts().sort_index())

plt.figure(figsize=(8,5))

plt.scatter(df["Price"], df["Rating"])
plt.title("Book Price vs Rating")
plt.xlabel("Price (E)")
plt.ylabel("Rating")

plt.show()

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nStatistical Summary:")
print(df.describe())

print("\nBooks Under £20:")
print((df["Price"] < 20).sum())

print("\nTop 5 Most Expensive Books:")
print(df.nlargest(5, "Price")[["Book Name", "Price"]])

print("\n--- EDA Findings ---")

print("Total Books:", len(df))
print("Average Price:", round(df["Price"].mean(), 2))
print("Average Rating:", round(df["Rating"].mean(), 2))
print("Most Common Rating:", df["Rating"].mode()[0])
print("Cheapest Price:", df["Price"].min())
print("Most Expensive Price:", df["Price"].max())

print("\n--- EDA CONCLUSION ---")

print("1. Total books analyzed:", len(df))

print("2. Average book price:", round(df["Price"].mean(), 2))

print("3. Cheapest book price:", round(df["Price"].min(), 2))

print("4. Most expensive book price:", round(df["Price"].max(), 2))

print("5. Average book rating:", round(df["Rating"].mean(), 2))

print("6. Highest rating:", df["Rating"].max())

print("7. Missing values in dataset:")
print(df.isnull().sum())

print("\nEDA analysis completed successfully!")

#step 3
plt.figure(figsize=(8, 5))

plt.scatter(df["Price"], df["Rating"], alpha=0.7)

plt.title("Book Price vs Rating")
plt.xlabel("Book Price (£)")
plt.ylabel("Book Rating")
plt.grid(True, linestyle= "--", alpha = 0.4)

plt.tight_layout()
plt.savefig("price_vs_rating.png")
plt.show()

print("Graph saved successfully!")

#step 4 data stroy

print("\n-- DATA STORY ---")
print("Total books analyzed:", len(df))
print("Average book price:", round (df["Price"].mean(),2))
print("Average book rating:", round(df["Rating"].mean(), 2))

print("\nInsights:")
print("1. The bar chart shows how many books have each rating.")
print("2. The histogram shows the distribution of book prices.")
print("3. The scatter plot compares book prices with ratings.")
print("4. These charts help us understand the book dataset.")

# Step 5: Save visualization summary

import os

os.makedirs("visualization_output", exist_ok=True)

plt.figure(figsize=(8, 5))
df["Rating"].value_counts().sort_index().plot(kind="bar")

plt.title("Number of Books by Rating")
plt.xlabel("Rating")
plt.ylabel("Number of Books")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("visualization_output/rating_chart.png")
plt.close()

plt.figure(figsize=(8, 5))
plt.hist(df["Price"].dropna(), bins=8, edgecolor="black")

plt.title("Distribution of Book Prices")
plt.xlabel("Book Price (£)")
plt.ylabel("Number of Books")
plt.tight_layout()

plt.savefig("visualization_output/price_histogram.png")
plt.close()

plt.figure(figsize=(8, 5))
plt.scatter(df["Price"], df["Rating"], alpha=0.7)

plt.title("Book Price vs Rating")
plt.xlabel("Book Price (£)")
plt.ylabel("Rating")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("visualization_output/price_vs_rating.png")
plt.close()

print("All graphs saved in visualization_output folder!")

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

reviews = [
    "This book is amazing and wonderful",
    "This book is terrible and boring",
    "This book is okay"
]

print("\n--- SENTIMENT ANALYSIS ---")

for review in reviews:
    score = analyzer.polarity_scores(review)["compound"]

    if score >= 0.05:
        sentiment = "Positive"
    elif score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    print("Review:", review)
    print("Sentiment:", sentiment)
    print()

    import matplotlib.pyplot as plt
from collections import Counter

sentiments = []

for review in reviews:
    score = analyzer.polarity_scores(review)["compound"]

    if score >= 0.05:
        sentiments.append("Positive")
    elif score <= -0.05:
        sentiments.append("Negative")
    else:
        sentiments.append("Neutral")

sentiment_counts = Counter(sentiments)

plt.bar(sentiment_counts.keys(), sentiment_counts.values())
plt.title("Sentiment Analysis Results")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")

plt.savefig("sentiment_analysis.png")
plt.show()

import csv

with open("sentiment_results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["Review", "Sentiment"])

    for review, sentiment in zip(reviews, sentiments):
        writer.writerow([review, sentiment])

print("Sentiment results saved successfully!")

print("\n--- SENTIMENT SUMMARY ---")

for sentiment, count in sentiment_counts.items():
    print(f"{sentiment}: {count}")

print("Total sentences analyzed:", len(reviews))

import pandas as pd

review_data = {
    "Review": [
        "This book is excellent and very useful",
        "The story is boring and disappointing",
        "The book is okay, nothing special",
        "Amazing quality and wonderful content",
        "Very poor book, I did not like it",
        "The book is average"
    ]
}

review_df = pd.DataFrame(review_data)

review_df["Sentiment"] = review_df["Review"].apply(
    lambda review: (
        "Positive" if analyzer.polarity_scores(review)["compound"] >= 0.05
        else "Negative" if analyzer.polarity_scores(review)["compound"] <= -0.05
        else "Neutral"
    )
)

review_df.to_csv("book_review_sentiments.csv", index=False)

print("\nReview dataset created!")
print(review_df)

import matplotlib.pyplot as plt

sentiment_counts = review_df["Sentiment"].value_counts()

plt.bar(sentiment_counts.index, sentiment_counts.values)

plt.title("Book Review Sentiment Analysis")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")

plt.savefig("book_review_sentiment_chart.png")
plt.show()

print("Sentiment graph saved successfully!")

print("\n--- SENTIMENT ANALYSIS CONCLUSION ---")

positive = (review_df["Sentiment"] == "Positive").sum()
negative = (review_df["Sentiment"] == "Negative").sum()
neutral = (review_df["Sentiment"] == "Neutral").sum()
total = len(review_df)

print("Total Reviews:", total)
print("Positive Reviews:", positive)
print("Negative Reviews:", negative)
print("Neutral Reviews:", neutral)

if positive > negative and positive > neutral:
    print("Conclusion: Overall sentiment is Positive.")
elif negative > positive and negative > neutral:
    print("Conclusion: Overall sentiment is Negative.")
elif positive == negative == neutral:
    print("Conclusion: All sentiments are equally distributed.")
else:
    print("Conclusion: No single sentiment is dominant.")

    print("\n===== SENTIMENT ANALYSIS REPORT =====")

print("Project: Book Review Sentiment Analysis")
print("Method: VADER Sentiment Analysis")
print("Dataset: 6 Sample Book Reviews")

print("\nResults:")
print(review_df["Sentiment"].value_counts())

print("\nConclusion:")
print(
    "Sentiment analysis classifies reviews as Positive, "
    "Negative, or Neutral using text sentiment scores."
)

print("\nFiles Generated:")
print("- book_review_sentiments.csv")
print("- book_review_sentiment_chart.png")

print("\nProject completed successfully!")

import pandas as pd

df_reviews = pd.read_csv("book_review_sentiments.csv")

print("\n--- LOADED REVIEW DATA ---")
print(df_reviews.head())

print("\n--- SENTIMENT COUNTS ---")
print(df_reviews["Sentiment"].value_counts())

print("\n--- DATASET INFORMATION ---")
print("Total reviews:", len(df_reviews))
print("Missing values:")
print(df_reviews.isnull().sum())

print("\n--- EMOTION DETECTION ---")

emotion_examples = {
    "Joy": "I am very happy and excited about this book",
    "Anger": "I am angry and frustrated with this book",
    "Sadness": "This book made me sad and unhappy",
    "Fear": "This story is scary and frightening"
}

for emotion, text in emotion_examples.items():
    print("Text:", text)
    print("Detected emotion:", emotion)
    print()

print("\n--- EMOTION AND SENTIMENT CHECK ---")

emotion_texts = [
    "I am so happy with this wonderful book!",
    "I am angry and disappointed with this book.",
    "This story makes me feel sad.",
    "This book is okay, nothing special."
]

for text in emotion_texts:
    score = analyzer.polarity_scores(text)["compound"]

    if score >= 0.05:
        sentiment = "Positive"
    elif score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    print("Text:", text)
    print("Sentiment:", sentiment)
    print("Compound score:", score)
    print()

    from transformers import pipeline

print("\n--- EMOTION DETECTION MODEL ---")

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=1
)

texts = [
    "I am very happy with this book!",
    "I am angry and disappointed.",
    "This story makes me feel sad.",
    "I am afraid of what happens next."
]

for text in texts:
    result = emotion_classifier(text)[0][0]

    print("Text:", text)
    print("Emotion:", result["label"])
    print("Confidence:", round(result["score"] * 100, 2), "%")
    print()

import pandas as pd

emotion_results = []

for text in texts:
    result = emotion_classifier(text)[0]

    emotion_results = []

for text in texts:
    result = emotion_classifier(text)[0][0]

    emotion_results.append({
        "Text": text,
        "Emotion": result["label"],
        "Confidence": round(result["score"] * 100, 2)
    })

emotion_df = pd.DataFrame(emotion_results)

emotion_df.to_csv("emotion_detection_results.csv", index=False)

print("\nEmotion results saved successfully!")
print(emotion_df)

import matplotlib.pyplot as plt

emotion_counts = emotion_df["Emotion"].value_counts()

plt.bar(emotion_counts.index, emotion_counts.values)

plt.title("Emotion Detection Results")
plt.xlabel("Emotion")
plt.ylabel("Number of Texts")

plt.savefig("emotion_detection_chart.png")
plt.show()

print("Emotion chart saved successfully!")

import pandas as pd

reviews_df = pd.read_csv("customer reviews.csv")

print("\n--- CUSTOMER REVIEWS DATA ---")
print(reviews_df.head())

print("\nColumn Names:")
print(reviews_df.columns.tolist())

print("\nTotal Rows:", len(reviews_df))

reviews_df = pd.read_csv("customer reviews.csv")

print("\n--- CUSTOMER REVIEWS DATA ---")
print(reviews_df.head())

print("\nColumn Names:")
print(reviews_df.columns.tolist())

print("\nTotal Rows:", len(reviews_df))

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# Review text ko clean karna
reviews_df["review description"] = (
    reviews_df["review description"].fillna("").astype(str)
)

# Sentiment classify karna
def analyze_sentiment(review):
    score = analyzer.polarity_scores(review)["compound"]

    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

reviews_df["Sentiment"] = reviews_df["review description"].apply(
    analyze_sentiment
)

# Results check karna
print("\n--- SENTIMENT ANALYSIS RESULTS ---")
print(reviews_df[["review description", "Sentiment"]].head(10))

print("\nSentiment Counts:")
print(reviews_df["Sentiment"].value_counts())

# CSV save karna
reviews_df.to_csv("customer_review_sentiments.csv", index=False)

print("\nSentiment results saved successfully!")

import matplotlib.pyplot as plt

sentiment_counts = reviews_df["Sentiment"].value_counts()

plt.figure(figsize=(8, 5))
plt.bar(sentiment_counts.index, sentiment_counts.values)

plt.title("Customer Reviews Sentiment Analysis")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")

for i, count in enumerate(sentiment_counts.values):
    plt.text(i, count, str(count), ha="center", va="bottom")

plt.tight_layout()
plt.savefig("customer_sentiment_chart.png")
plt.show()

print("Sentiment chart saved successfully!")

# Sentiment Analysis Summary Report

total_reviews = len(reviews_df)
sentiment_counts = reviews_df["Sentiment"].value_counts()

print("\n--- SENTIMENT ANALYSIS REPORT ---")
print("Total Reviews:", total_reviews)

for sentiment, count in sentiment_counts.items():
    percentage = (count / total_reviews) * 100 if total_reviews > 0 else 0
    print(f"{sentiment}: {count} reviews ({percentage:.2f}%)")

# Save report to a text file
with open("sentiment_report.txt", "w", encoding="utf-8") as file:
    file.write("CUSTOMER REVIEW SENTIMENT REPORT\n")
    file.write(f"Total Reviews: {total_reviews}\n\n")

    for sentiment, count in sentiment_counts.items():
        percentage = (count / total_reviews) * 100 if total_reviews > 0 else 0
        file.write(
            f"{sentiment}: {count} reviews ({percentage:.2f}%)\n"
        )

print("\nReport saved as sentiment_report.txt")

print("\n--- BUSINESS INSIGHTS ---")

print("1. Most reviews are positive, showing favorable customer opinion.")
print("2. Negative reviews should be checked to identify product issues.")
print("3. Neutral reviews may help identify areas for improvement.")
print("4. Businesses can use customer feedback to improve book quality and service.")
print("5. More reviews can help identify trends over time.")


print("\n--- TASK 4: SENTIMENT PATTERNS ---")

# Sentiment by customer rating
if "rating" in reviews_df.columns:
    reviews_df["rating"] = pd.to_numeric(
        reviews_df["rating"], errors="coerce"
    )

    print("\nSentiment by Rating:")
    print(pd.crosstab(
        reviews_df["rating"],
        reviews_df["Sentiment"]
    ))
else:
    print("Rating column not found.")
    print("Available columns:", reviews_df.columns.tolist())

import matplotlib.pyplot as plt

if "rating" in reviews_df.columns:
    sentiment_rating = pd.crosstab(
        reviews_df["rating"],
        reviews_df["Sentiment"]
    )

    sentiment_rating.plot(
        kind="bar",
        figsize=(9, 5)
    )

    plt.title("Customer Sentiment by Rating")
    plt.xlabel("Customer Rating")
    plt.ylabel("Number of Reviews")
    plt.xticks(rotation=0)
    plt.legend(title="Sentiment")
    plt.tight_layout()

    plt.savefig("sentiment_by_rating.png")
    plt.show()

    print("Graph saved as sentiment_by_rating.png")
else:
    print("Rating column not found. Check column names.")

    print("\n--- TASK 4: PUBLIC OPINION INSIGHTS ---")

if "rating" in reviews_df.columns:
    print("\nAverage rating by sentiment:")

    print(
        reviews_df.groupby("Sentiment")["rating"]
        .mean()
        .round(2)
    )

    print("\nMost common sentiment:")
    print(reviews_df["Sentiment"].value_counts().idxmax())

    print("\nInterpretation:")
    print(
        "This analysis compares customer sentiment "
        "with their ratings to identify opinion patterns."
    )
else:
    print("Rating column not found.")
    print("Available columns:", reviews_df.columns.tolist())

# Task 4: Save Public Opinion Findings

with open("task4_findings.txt", "w", encoding="utf-8") as file:
    file.write("PUBLIC OPINION AND SENTIMENT TRENDS\n")
    file.write("=" * 40 + "\n\n")

    file.write(f"Total reviews analyzed: {len(reviews_df)}\n\n")

    file.write("Sentiment Distribution:\n")
    file.write(
        reviews_df["Sentiment"].value_counts().to_string()
        + "\n\n"
    )

    if "rating" in reviews_df.columns:
        file.write("Average Rating by Sentiment:\n")
        file.write(
            reviews_df.groupby("Sentiment")["rating"]
            .mean()
            .round(2)
            .to_string()
            + "\n\n"
        )

    file.write("Conclusion:\n")
    file.write(
        "Customer reviews were analyzed to understand public opinion. "
        "Sentiment categories and rating patterns can help identify "
        "customer satisfaction and areas for improvement.\n"
    )

print("Task 4 findings saved in task4_findings.txt")

print("\n--- CUSTOMER REVIEW COLUMNS ---")
print(reviews_df.columns.tolist())

# Task 4: Monthly Sentiment Trends

reviews_df["date"] = pd.to_datetime(
    reviews_df["date"],
    errors="coerce"
)

reviews_df["Month"] = reviews_df["date"].dt.to_period("M")

monthly_trends = pd.crosstab(
    reviews_df["Month"],
    reviews_df["Sentiment"]
)

print("\n--- MONTHLY SENTIMENT TRENDS ---")
print(monthly_trends)

if not monthly_trends.empty:
    monthly_trends.plot(
        kind="line",
        marker="o",
        figsize=(10, 5)
    )

    plt.title("Monthly Customer Sentiment Trends")
    plt.xlabel("Month")
    plt.ylabel("Number of Reviews")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("monthly_sentiment_trends.png")
    plt.show()

    print("Monthly trend graph saved successfully!")
else:
    print("Valid dates nahi mili. Date format check karna hoga.")

    # Task 4: Monthly Trend Summary

print("\n--- TASK 4 FINAL SUMMARY ---")

print("Total reviews:", len(reviews_df))
print("\nOverall sentiment distribution:")
print(reviews_df["Sentiment"].value_counts())

print("\nMonthly trend data:")
print(monthly_trends)

print("\nConclusion:")
print(
    "Customer reviews were analyzed to understand public opinion. "
    "Sentiment categories and monthly patterns help summarize "
    "customer opinions over time."
)

# TASK 5: BUSINESS INSIGHTS

print("\n--- TASK 5: BUSINESS INSIGHTS ---")

# Count each sentiment
sentiment_counts = reviews_df["Sentiment"].value_counts()

total_reviews = len(reviews_df)

print("\n1. Total Customer Reviews:", total_reviews)

print("\n2. Sentiment Distribution:")
print(sentiment_counts)

# Calculate sentiment percentages
print("\n3. Sentiment Percentages:")
for sentiment, count in sentiment_counts.items():
    percentage = (count / total_reviews) * 100 if total_reviews else 0
    print(f"{sentiment}: {percentage:.2f}%")

# Identify the most common sentiment
if not sentiment_counts.empty:
    most_common = sentiment_counts.idxmax()
    print("\n4. Most Common Sentiment:", most_common)

# Business recommendations based on the results
print("\n5. Business Recommendations:")

if "Negative" in sentiment_counts.index:
    print("- Review negative feedback to find customer problems.")

if "Positive" in sentiment_counts.index:
    print("- Study positive reviews to understand what customers like.")

if "Neutral" in sentiment_counts.index:
    print("- Check neutral reviews for possible improvements.")

print("\nTask 5 basic analysis completed!")

# TASK 5: SAVE BUSINESS INSIGHTS REPORT

sentiment_counts = reviews_df["Sentiment"].value_counts()
total_reviews = len(reviews_df)

with open("business_insights_report.txt", "w", encoding="utf-8") as file:
    file.write("BUSINESS INSIGHTS REPORT\n")
    file.write("=" * 35 + "\n\n")

    file.write(f"Total reviews analyzed: {total_reviews}\n\n")
    file.write("Sentiment Distribution:\n")

    for sentiment, count in sentiment_counts.items():
        percentage = (count / total_reviews) * 100 if total_reviews else 0
        file.write(
            f"{sentiment}: {count} reviews ({percentage:.2f}%)\n"
        )

    file.write("\nBusiness Recommendations:\n")
    file.write(
        "1. Review negative feedback to identify customer problems.\n"
    )
    file.write(
        "2. Study positive reviews to understand customer preferences.\n"
    )
    file.write(
        "3. Examine neutral reviews to find improvement opportunities.\n"
    )
    file.write(
        "4. Monitor sentiment regularly to track customer opinions.\n"
    )

print("Business insights saved to business_insights_report.txt")

# TASK 5: COMMON WORDS IN NEGATIVE REVIEWS

from collections import Counter
import re

negative_reviews = reviews_df.loc[
    reviews_df["Sentiment"] == "Negative",
    "review description"
].dropna()

all_words = []

for review in negative_reviews:
    words = re.findall(r"\b[a-zA-Z]{3,}\b", str(review).lower())
    all_words.extend(words)

# Remove common words that do not tell us much
stop_words = {
    "the", "and", "for", "was", "this", "that", "with",
    "but", "not", "are", "you", "have", "had", "has",
    "very", "from", "they", "their", "too", "its", "been",
    "were", "would", "could", "about", "there", "what",
    "when", "your", "all", "one", "book"
    "his", "her", "she", "him", "who", "how",
"out", "all", "one", "life", "read", "like",
"people", "get", "just", "really", "also"
}

filtered_words = [
    word for word in all_words if word not in stop_words
]

common_words = Counter(filtered_words).most_common(10)

print("\n--- COMMON WORDS IN NEGATIVE REVIEWS ---")
print("Negative reviews analyzed:", len(negative_reviews))

for word, count in common_words:
    print(f"{word}: {count}")

# TASK 5: NEGATIVE REVIEW WORD FREQUENCY CHART

if common_words:
    words = [item[0] for item in common_words]
    counts = [item[1] for item in common_words]

    plt.figure(figsize=(10, 5))
    plt.bar(words, counts)

    plt.title("Most Common Words in Negative Reviews")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("negative_review_common_words.png")
    plt.show()

    print("Chart saved as negative_review_common_words.png")
else:
    print("No words found in negative reviews.")

# TASK 5: SAVE NEGATIVE REVIEW FINDINGS

with open(
    "negative_review_findings.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write("NEGATIVE CUSTOMER REVIEW ANALYSIS\n")
    file.write("=" * 40 + "\n\n")

    file.write(
        f"Negative reviews analyzed: {len(negative_reviews)}\n\n"
    )

    file.write("Most common words:\n")

    if common_words:
        for word, count in common_words:
            file.write(f"{word}: {count}\n")
    else:
        file.write("No common words were found.\n")

    file.write("\nInterpretation:\n")
    file.write(
        "Frequent words can suggest topics in negative reviews. "
        "The original reviews should be read to confirm the actual "
        "customer problems before making business decisions.\n"
    )

print("Negative review findings saved successfully!")