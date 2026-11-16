import os
import pandas as pd

def calculate_grade(percentage):
    """Calculates grade based on percentage brackets."""
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 50:
        return 'D'
    elif percentage >= 40:
        return 'E'
    else:
        return 'F'

def load_and_validate_data(filename="marks.csv"):
    """Reads marks.csv using Pandas, validates marks, and skips invalid rows with a warning."""
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return None

    try:
        df = pd.read_csv(filename)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    expected_columns = ['RollNo', 'Name', 'Maths', 'Physics', 'Programming']
    for col in expected_columns:
        if col not in df.columns:
            print(f"Error: Missing expected column '{col}' in CSV.")
            return None

    valid_rows = []
    for index, row in df.iterrows():
        roll = row['RollNo']
        name = row['Name']
        try:
            maths = float(row['Maths'])
            physics = float(row['Physics'])
            programming = float(row['Programming'])
        except ValueError:
            print(f"Warning: Row for roll {roll} skipped - non-numeric marks found.")
            continue

        # Validate that each mark is between 0 and 100
        if not (0 <= maths <= 100 and 0 <= physics <= 100 and 0 <= programming <= 100):
            print(f"Warning: Row for roll {roll} skipped - marks must be between 0 and 100.")
            continue

        valid_rows.append({
            'RollNo': int(roll),
            'Name': str(name),
            'Maths': maths,
            'Physics': physics,
            'Programming': programming
        })

    return pd.DataFrame(valid_rows)

def generate_marksheet(df, roll_no):
    """Generates and prints a neat marksheet for the specified roll number."""
    if df is None or df.empty:
        print("No valid student data available.")
        return

    student = df[df['RollNo'] == roll_no]
    if student.empty:
        print(f"Roll number {roll_no} not found.")
        return

    student = student.iloc[0]
    maths = student['Maths']
    physics = student['Physics']
    programming = student['Programming']

    total = maths + physics + programming
    percentage = (total / 300) * 100
    grade = calculate_grade(percentage)

    # Determine result (FAIL if any subject is below 40)
    failed_subjects = []
    if maths < 40:
        failed_subjects.append("Maths")
    if physics < 40:
        failed_subjects.append("Physics")
    if programming < 40:
        failed_subjects.append("Programming")

    if failed_subjects:
        result = f"FAIL ({', '.join(failed_subjects)} below 40)"
    else:
        result = "PASS"

    # Neat console formatting
    print("\n" + "="*30)
    print("        MARK SHEET        ")
    print("="*30)
    print(f"Roll No: {int(student['RollNo'])} | Name: {student['Name']}")
    print(f"Maths: {maths:g} | Physics: {physics:g} | Programming: {programming:g}")
    print(f"Total: {int(total) if total.is_integer() else total}/300 | Percentage: {percentage:.2f}%")
    print(f"Grade: {grade} | Result: {result}")
    print("="*30 + "\n")

def main():
    # Automatically generate 'marks.csv' with sample test data if it does not exist
    if not os.path.exists("marks.csv"):
        sample_data = """RollNo,Name,Maths,Physics,Programming
101,Anita,85,95,80
102,Rahul,40,45,50
103,Suman,35,70,60
104,Vikas,100,100,100
106,Kiran,105,60,70
"""
        with open("marks.csv", "w") as f:
            f.write(sample_data)
        print("Created sample 'marks.csv' file successfully.")

    df = load_and_validate_data("marks.csv")

    while True:
        print("\n--- Automated Marksheet Generator Menu ---")
        print("1. Single Marksheet")
        print("2. Exit")
        choice = input("Enter your choice (1-2): ").strip()

        if choice == '1':
            try:
                roll_input = int(input("Enter Roll No: ").strip())
                generate_marksheet(df, roll_input)
            except ValueError:
                print("Invalid input. Please enter a valid numeric Roll No.")
        elif choice == '2':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()