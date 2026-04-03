import pdfplumber
import streamlit as st
import pandas as pd

@st.cache_data
def load_pdf_data():
    rows = []
    with pdfplumber.open('MCA_2024_RankList.pdf') as pdf:
        for page in pdf.pages:
            text = page.extract_table()
            if text:
                for row in text:
                    if row[0] and str(row[0]).isdigit():
                        rows.append(row)
    return rows
data_rows = load_pdf_data()
name = "User"
query = st.text_input("Search by Name / Roll Number").upper().strip()
matches = []
name = query
for row in data_rows:
    if name in row[3]:
        matches.append(row)
if query.isdigit():
    roll_number = query
    for row in data_rows:
        if roll_number in row[2]:
            matches.append(row)
if name:
    if not matches:
        st.error("Sorry, your Name / Roll Number is not found in the list.")
    elif len(matches) == 1:
        st.success(f'Hello, {matches[0][3]}!')
        st.info(f"Your Rank is {matches[0][0]}")
        st.info(f"Your Score is {matches[0][5]} Out of 120")
        st.info(f"Your Marks Details Per Subjects:")
        st.info(f"Computer Science(Out of 50): {matches[0][6]}")
        st.info(f"Mathematics and Statistics(Out of 25): {matches[0][7]}")
        st.info(f"Quantitative Aptitude, Logical Ability (Out of 25): {matches[0][8]}")
        st.info(f"English & G.K (Out of 20): {matches[0][9]}")
    else:
        st.info("Multiple entries found. Please find your Roll Number below:")
        df_matches = pd.DataFrame(matches, columns=["Rank", "App No", "Roll No", "Name", "DOB", "Total", "CS", "Math", "Apt", "Eng", "Final Rank"])
        st.table(df_matches[["Rank", "Roll No", "Name", "Total"]])

def handler(req, res):
    return
app = handler