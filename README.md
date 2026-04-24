import pypandoc

readme_text = """# 🌧️ Rain Jacket Data Cleaning Project

## 📌 Overview

This project focuses on cleaning and standardising a messy Excel dataset containing sales, orders, and customer data for a rain jacket business operating across Australia.

The goal is to transform raw, inconsistent data into a clean and reliable dataset that can be used for analysis and decision-making.

---

## 📁 Project Structure

models/
├── raw/                
├── processed/          
├── src/                
│   └── clean_sales_data.py
├── reports/            

requirements.txt
README.md

---

## ⚙️ Setup Instructions

### 1. Create virtual environment
#Windows
python -m venv .venv_newproject

#mac
python3 -m venv .venv_newproject

### 2. Activate virtual environment
#windows
.venv_newproject\Scripts\Activate.ps1

#mac
source .venv_newproject/bin/activate

### 3. Install dependencies
#windows and mac
pip install -r requirements.txt

---

## ▶️ Run the cleaning pipeline
#windows
python models\src\clean_sales_data.py

#mac
python models/src/clean_sales_data.py

---

## 📥 Input

models/raw/messy_rain_jacket_sales_database.xlsx

---

## 📤 Output

models/processed/clean_sales_data.csv

---

## 🧠 Data Cleaning Logic

- Clean city names using fuzzy matching
- Convert numeric fields
- Handle missing values
- Remove duplicates
- Apply validation rules

---

## 🛠️ Technologies Used

- Python
- Pandas
- OpenPyXL
- RapidFuzz

---

## 🚀 Future Improvements

- Data quality reports
- Weather API integration
- PostgreSQL integration
- Pipeline automation

---

## 🎯 Project Goal

Create a reliable single source of truth for sales data.