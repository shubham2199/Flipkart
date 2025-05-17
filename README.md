## Flipkart Chat BOAT

# 📊 Chatbot with DataStax Astra Integration (Data Cleaning ➜ Vectorization ➜ Chatbot)

This project demonstrates a full pipeline to build an intelligent chatbot using your custom data. The data flows through cleaning, vectorization, storage in [DataStax Astra DB](https://www.datastax.com/astra), and is served via a Flask-based chatbot API.

---

## 🔧 Project Workflow

1. **Data Cleaning**
2. **Vectorization (Convert Data to Vector Form)**
3. **Upload Vector Data to Astra DB**
4. **Fetch & Search Vector Data from Astra DB**
5. **Query Parsing & History Storage**
6. **Create a Flask Chatbot**
7. **Respond to User Queries using Vector Search**

---

## 1️⃣ Data Cleaning

Clean raw data (CSV, JSON, text, etc.) by:
- Removing nulls, duplicates
- Lowercasing text
- Removing stopwords, punctuations
- Tokenization


## 2️⃣ Convert Data to Vectors (Embeddings)

Once the data is cleaned, convert each text entry into a high-dimensional vector representation using a pre-trained model. 
These embeddings will be used for semantic search in Astra DB.


## 3️⃣ Upload Vector Data to DataStax Astra DB

After generating vector embeddings, the next step is to upload them to DataStax Astra DB using the cassio library, which makes it easy to work with vector-enabled Cassandra databases.


## 4️⃣ Vector Search in DataStax Astra DB

Once your embeddings are stored, you can perform semantic search using a query vector.
