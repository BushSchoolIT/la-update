import pandas as pd

existing_students = pd.read_csv("StudentExport.csv")
bb_students = pd.read_csv("~/la-import/BBExport.csv")

grade_level_map = {
    "Kindergarten": "K",
    "1st Grade": 1,
    "2nd Grade": 2,
    "3rd Grade": 3,
    "4th Grade": 4,
    "5th Grade": 5,
    "6th Grade": 6,
    "7th Grade": 7,
    "8th Grade": 8,
    "9th Grade": 9,
    "10th Grade": 10,
    "11th Grade": 11,
    "12th Grade": 12,
}

bb_students["Grade"] = bb_students["Grade"].map(grade_level_map)
# bb_students["Username"] = [username[:-9] if pd.notna(username) else "" for username in bb_students["Username"].values]

col_list = [
    "First Name",
    "Last Name",
    "Grade",
    "Student Email Address",
    "Student ID Number",
    "Username",
]
new_rows = []
existing_emails = set(existing_students["Student Email Address"].astype(str).str.strip())
existing_emails = {s.lower() for s in existing_emails if pd.notna(s)}

existing_ids = set(existing_students["Student ID Number"].astype(str).str.strip())

updated_students = existing_students

for index, row in bb_students.iterrows():
    student_email = str(row["Student Email Address"]).strip().lower() 
    student_id = str(row["Student ID Number"]).strip().lower()

    if student_email not in existing_emails:
        match_index = bb_students.index[bb_students["Student Email Address"].astype(str).str.strip().str.lower() == student_email][0]
        print(match_index)
        if student_id in existing_ids: 
           updated_students.loc[updated_students["Student ID Number"] == student_id, "Student Email Address"] = student_email
           print("updated" + student_email)
        else: 
            new_row = {}
            for col in col_list:
                new_row[col] = bb_students.loc[match_index, col]
            new_rows.append(new_row)

if new_rows:
    additions = pd.DataFrame(new_rows)
    additions = additions.reindex(columns=updated_students.columns)
    additions = pd.concat([updated_students, additions], ignore_index=True)
    additions["Do NOT Edit - Learning Ally Key"] = pd.to_numeric(additions["Do NOT Edit - Learning Ally Key"], errors="coerce").astype("Int64")
    additions["Learning Ally School Org ID"] = int(129941)
    additions.to_csv("StudentImport.csv", index=False, encoding="utf-8")
    print("wrote new file")