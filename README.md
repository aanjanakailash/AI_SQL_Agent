# AI_SQL_Agent
AI_SQL_Agent
# 🤖 SQL Agent

An AI-powered SQL Agent that allows users to upload CSV files, automatically clean and store data in MySQL, generate SQL queries from natural language questions, and display query results through an interactive Streamlit interface.

---

## 📌 Project Overview

SQL Agent bridges the gap between non-technical users and databases.

Instead of writing SQL queries manually, users can simply ask questions in plain English such as:

* "Show top 5 customers by sales"
* "Count total cities"
* "Find highest revenue products"
* "Show average sales by region"

The AI model converts the question into SQL, executes the query on MySQL, and returns the result instantly.

---

## 🚀 Features

### 📂 CSV Upload

* Upload any CSV dataset
* Automatic table creation in MySQL

### 🧹 Data Cleaning

* Removes duplicate records
* Removes empty rows
* Standardizes column names
* Handles missing values

### 🤖 AI-Powered SQL Generation

* Natural Language → SQL
* Dynamic table and column detection
* Context-aware query generation

### 🗄️ MySQL Integration

* Stores uploaded data in MySQL
* Executes generated SQL queries

### 📊 Interactive Results

* Displays generated SQL query
* Shows query output in tabular format
* Dataset preview and statistics

### 🌐 Streamlit Dashboard

* User-friendly interface
* Real-time query execution
* Easy dataset management

---

## 🏗️ Architecture

User Question
↓
AI Model (OpenRouter)
↓
SQL Query Generation
↓
MySQL Database
↓
Query Execution
↓
Results Displayed in Streamlit

---

## 🛠️ Tech Stack

| Technology     | Purpose             |
| -------------- | ------------------- |
| Python         | Backend Development |
| Streamlit      | Frontend Dashboard  |
| MySQL          | Database            |
| Pandas         | Data Processing     |
| SQLAlchemy     | Database Engine     |
| OpenRouter API | AI Integration      |
| Requests       | API Communication   |

---

## 📁 Project Structure

```text
SQL-Agent/
│
├── app.py
├── ai_helper.py
├── db.py
├── requirements.txt
├── README.md
│
├── assets/
│
├── screenshots/
│
└── sample_data/
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/sql-agent.git
cd sql-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure MySQL

Create database:

```sql
CREATE DATABASE sql_agent;
```

Update MySQL credentials in:

```python
db.py
```

### 4. Configure OpenRouter API

Add your API key inside:

```python
ai_helper.py
```

### 5. Run Application

```bash
streamlit run app.py
```

---

## 📸 Screenshots

### Home Page

Add screenshot here.

### CSV Upload

Add screenshot here.

### Query Generation

Add screenshot here.

### Query Results

Add screenshot here.

---

## 🎯 Example Questions

* Count total customers
* Show top 5 customers by sales
* Find total revenue
* Show highest selling products
* Count total cities
* Show average sales by region
* Find products with maximum profit

---

## 🔮 Future Enhancements

* Query History
* User Authentication
* Download Results as CSV
* Interactive Charts
* Dashboard Analytics
* Multi-file Support
* Voice-to-SQL
* ChatGPT-style Conversation Interface

---

## 👨‍💻 Author

Kailash J. Choudhary

### Skills Used

* SQL
* MySQL
* Python
* Pandas
* Streamlit
* Data Analysis
* Artificial Intelligence

---

## ⭐ Project Outcome

This project demonstrates how Artificial Intelligence can simplify database interaction by allowing users to query data using natural language instead of writing SQL manually.

It combines AI, Data Analytics, Database Management, and Web Application Development into a single intelligent solution.

