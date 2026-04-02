import pdfplumber
rows = []
matches = []
with pdfplumber.open('demo.pdf') as pdf:
    for page in pdf.pages:
        text = page.extract_table()
        if text:
            for row in text:
                if row[0] and str(row[0]).isdigit():
                    rows.append(row)
with open('out.csv', 'w') as c:
    for i in rows:
        
        c.write(', '.join(i) + '\n')
name = input('Enter ur name:').upper()
print(f'Hello, {name}!')
with open('out.csv', 'r') as c:
    for line in c:
        if name in line:
            parts = line.strip().split(', ')
            if name in parts[3]:
                matches.append(parts)

    print(f"Total Matches Found: {len(matches)}")
    if not matches:
        print("Sorry, your name is not found in the list.")
    elif len(matches) == 1:
            print(f"Your Rank is {line.split(', ')[0]}")
            print(f"Your Score is {line.split(', ')[5]} Out of 120")
            print(f"Your Marks Details Per Subjects:")
            print(f"Computer Science(Out of 50): {line.split(', ')[6]}")
            print(f"Mathematics and Statistics(Out of 25): {line.split(', ')[7]}")
            print(f"Quantitative Aptitude, Logical Ability (Out of 25): {line.split(', ')[8]}")
            print(f"English & G.K (Out of 20): {line.split(', ')[9]}")
    else:
        print("Multiple entries found for your name. Please check the list for more details.")
