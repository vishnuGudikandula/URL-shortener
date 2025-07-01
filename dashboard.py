
import streamlit as st
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
collection = client["logstream"]["metrics"]

st.title("Log Analytics Dashboard")

data = list(collection.find().sort("processed_at", -1).limit(5))
for doc in data:
    st.subheader(doc["filename"])
    st.write(f"Errors: {doc['errors']}")
    st.bar_chart(doc["hourly_traffic"])
    st.json(doc["ip_hits"])
