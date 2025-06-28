# 🚓 SecureCheck-A-Python-SQL-Dashboard-for-Police-Traffic-Stops

**SecureCheck** is a data-driven analytics dashboard that visualizes and analyzes police traffic stop records using Python, SQL, Pandas, and Streamlit. The goal is to provide clear insights into driver demographics, violation trends, arrests, and search patterns.
---

## 📊 Key Features

- ✅ **Comprehensive Data Cleaning**  
  - Removed duplicates and null values  
  - Standardized string formats (title case, trimmed spaces)  
  - Converted date/time columns to proper formats  
- ✅ **PostgreSQL Integration**  
  - Structured schema with appropriate data types  
  - Uploaded clean data to a PostgreSQL cloud database using SQLAlchemy  
- ✅ **Interactive Streamlit Dashboard**  
  - View full cleaned dataset  
  - Key metrics: total stops, arrests, warnings, drug-related stops  
  - Visual insights using Altair:  
    - Traffic Stops by Violation  
    - Driver Gender Distribution  
  - Advanced SQL Insights (Medium & Complex level queries)  
  - Predictive Summary Form based on user inputs

---

## 🛠️ Tech Stack Used

- **Python** – Scripting and data processing  
- **Pandas** – Data cleaning and transformation  
- **SQLAlchemy** – Database communication  
- **PostgreSQL** – Data storage and querying  
- **Streamlit** – Building interactive dashboard  


---

## 📂 Project Structure

```
├── SecureCheck.ipynb          # Data cleaning and database upload logic  
├── SecureCheck.py             # Streamlit dashboard code  
├── cleaned_traffic_stop.csv   # Final cleaned dataset  
└── README.md                  # Project documentation (this file)
```

---

## 📈 Dashboard Insights

- Top violations and their search/arrest rates  
- Gender and race-based search trends  
- Drug-related stop trends by country  
- Stop durations categorized by violation type  
- Predictive summary based on user input (age, time, gender, etc.)

---

## ⚙️ How to Use

1. Clone this repository and open it in your preferred IDE (e.g., VS Code).
2. Ensure Python and required libraries are installed.
3. Run the `SecureCheck.py` file using Streamlit:
   ```bash
   streamlit run SecureCheck.py
   ```

---

## 📌 Project Goal

This dashboard was built as a learning and evaluation project to demonstrate the ability to:

- Handle real-world police stop data  
- Clean and normalize data efficiently  
- Store structured data in a relational database  
- Create an insightful and interactive analytics dashboard  
- Deliver real-time insights for decision-making

---

## 📎 Note

- Sensitive credentials are excluded from this project.  
- You may update the PostgreSQL connection with your own secure credentials if testing locally.

---

✅ Ready to explore 🚦 SecureCheck Dashboard and uncover insights from traffic stops!

