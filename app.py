import pdfplumber
import streamlit as st
import pandas as pd

@st.cache_data
def load_pdf_data():
    rows = []
    with pdfplumber.open('MCA_2025_RankList.pdf') as pdf:
        for page in pdf.pages:
            text = page.extract_table()
            if text:
                for row in text:
                    if row[0] and str(row[0]).isdigit():
                        rows.append(row)
    return rows
data_rows = load_pdf_data()
st.set_page_config(
    page_title="MCA Rank Finder 2025",
    page_icon="icon.png", 
    layout="centered"
)
st.title("MCA Rank Finder 2025")
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
        st.markdown(f'### Hi, {matches[0][3].title()}!')
        st.caption(f"Roll Number: {matches[0][2]} | Application Number: {matches[0][1]} | Date of Birth: {matches[0][7]}")
        col1, col2 = st.columns([1,1])
        col1.metric("Rank", f"{matches[0][0]}")
        col2.metric("Score ", f"{matches[0][8]}/120")
        st.divider()
        st.markdown("#### Subject Breakdown")
        col1, col2 = st.columns([1,1])
        col1.metric(f"Computer Science", f"{matches[0][-4]}/50")
        col2.metric(f"Mathematics and Statistics", f"{matches[0][-3]}/25")
        col3, col4 = st.columns([1,1])
        col3.metric(f"Quantitative Aptitude, Logical Ability", f"{matches[0][-2]}/25")
        eng_gk = int(matches[0][-5]) - int(matches[0][-4]) - int(matches[0][-3]) - int(matches[0][-2])
        col4.metric(f"English & G.K", f"{eng_gk-6}/20*")
        st.caption("*English & G.K marks are estimated by subtracting CS, Math, Aptitude, and a fixed bonus of 6 marks (awarded to all students due to out-of-syllabus questions).")
    else:
        st.info("Multiple entries found. Please find your Roll Number below:")
        df_matches = pd.DataFrame(matches, columns=["Rank", "App No", "Roll No", "Name", "Nativity", "Community", "Whether OEC", "DOB", "Total", "CS", "Math", "Apt", "Final Rank"])
        st.table(df_matches[["Rank", "Roll No", "Name", "Total"]]) 