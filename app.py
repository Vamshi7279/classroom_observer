from flask import Flask, render_template, request, redirect, session
import pandas as pd
import os
from datetime import date
import attendance
from database import calculate_performance

app = Flask(__name__)
app.secret_key = 'classroom_observer_secret'  # Replace in production!

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users_df = pd.read_csv('data/users.csv')
        user = users_df[(users_df['username'] == username) & (users_df['password'] == password)]

        if not user.empty:
            user_data = user.iloc[0]
            session['username'] = username
            session['role'] = user_data['role']
            session['roll_number'] = user_data.get('roll_number', '')
            return redirect('/dashboard')
        else:
            return "Invalid username or password."

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    role = session['role']
    roll = session['roll_number']

    # Get list of dicts from calculate_performance()
    performance_data = calculate_performance()

    if role == 'student':
        marks_df = pd.read_csv('data/marks.csv')
        performance_df = pd.DataFrame(performance_data)  # Convert back to DataFrame for filtering

        student_marks = marks_df[marks_df['Roll Number'] == roll].iloc[0]
        student_perf = performance_df[performance_df['Roll Number'] == roll].iloc[0]

        return render_template('student_dashboard.html',
                               username=session['username'],
                               roll_number=roll,
                               attendance=round(student_perf['Attendance'], 2),
                               exam=student_marks['Exam'],
                               assignment=student_marks['Assignment'],
                               participation=student_marks['Participation'],
                               performance=round(student_perf['Final Score'], 2))

    elif role == 'teacher':
        return render_template('teacher_dashboard.html',
                               username=session['username'],
                               performance=performance_data)

@app.route('/take_attendance')
def take_attendance():
    if 'role' in session and session['role'] == 'teacher':
        attendance.take_attendance()
    return redirect('/dashboard')

@app.route('/upload_marks', methods=['GET', 'POST'])
def upload_marks():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            file.save(os.path.join('data', 'marks.csv'))
            return redirect('/dashboard')
        else:
            return "Upload a valid CSV file."
    
    return '''
        <form method="post" enctype="multipart/form-data">
            <h3>Upload Marks CSV</h3>
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
