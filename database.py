import pandas as pd

def calculate_performance():
    # Read attendance and marks data
    attendance = pd.read_csv("data/attendance.csv")
    marks = pd.read_csv("data/marks.csv")

    # Calculate attendance percentage
    total_classes = attendance["Date"].nunique()
    attendance_summary = attendance.groupby("Roll Number")["Status"].apply(lambda x: (x == "Present").sum())
    attendance_percentage = (attendance_summary / total_classes) * 100

    # Map attendance to marks dataframe
    marks["Attendance"] = marks["Roll Number"].map(attendance_percentage)
    marks["Attendance"].fillna(0, inplace=True)

    # Calculate final score (50% from marks, 50% from attendance)
    marks["Final Score"] = ((marks["Exam"] + marks["Assignment"] + marks["Participation"]) / 3) * 0.5 + marks["Attendance"] * 0.5

    # Round values for display
    marks["Attendance"] = marks["Attendance"].round(2)
    marks["Final Score"] = marks["Final Score"].round(2)

    # Save performance to CSV
    marks.to_csv("data/performance.csv", index=False)

    # Return the result as a list of dictionaries for rendering in HTML
    return marks.to_dict(orient="records")
