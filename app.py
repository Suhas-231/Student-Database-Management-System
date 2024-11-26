from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# MySQL database connection settings
username = 'root'
password = 'Suhas@23'
host = 'localhost'
database = 'bcs403'

# Create a MySQL connection
cnx = pymysql.connect(
    user=username,
    password=password,
    host=host,
    database=database
)

# Create a cursor object
cursor = cnx.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view_all_students_personal_details')
def view_all_students_personal_details():
    query = "SELECT * FROM students"
    cursor.execute(query)
    students = cursor.fetchall()
    return render_template('personal_details.html', students=students)

@app.route('/show_top_10_students')
def show_top_10_students():
    query = "SELECT USN, NAME, SGPA FROM final_vtu ORDER BY SGPA DESC LIMIT 10"
    cursor.execute(query)
    students = cursor.fetchall()
    return render_template('top_10_students.html', students=students)

@app.route('/show_all_students')
def show_all_students():
    query = "SELECT USN, NAME, GRADES FROM students"
    cursor.execute(query)
    students = cursor.fetchall()
    return render_template('all_students.html', students=students)

@app.route('/cgpa_calculation')
def cgpa_calculation():
    query = "SELECT USN, NAME, CGPA FROM students"
    cursor.execute(query)
    students = cursor.fetchall()
    return render_template('cgpa_calculation.html', students=students)

@app.route('/check_backlogs', methods=['GET', 'POST'])
def check_backlogs():
    search_data = []
    if request.method == 'POST':
        usn = request.form['usn']
        search_query = """
            SELECT 
                s.NAME, 
                s.USN, 
                COALESCE(GROUP_CONCAT(CASE WHEN fv.18CS81 < 35 THEN '18CS81' WHEN fv.18CS82 < 35 THEN '18CS82' WHEN fv.18CSP83 < 35 THEN '18CSP83' WHEN fv.18CS84 < 35 THEN '18CS84' WHEN fv.18CSI85 < 35 THEN '18CSI85' END), '') AS backlog_subjects,
                COALESCE(SUM(CASE WHEN fv.18CS81 < 35 THEN 1 WHEN fv.18CS82 < 35 THEN 1 WHEN fv.18CSP83 < 35 THEN 1 WHEN fv.18CS84 < 35 THEN 1 WHEN fv.18CSI85 < 35 THEN 1 END), 0) AS total_backlogs
            FROM 
                students s 
                JOIN final_vtu fv ON s.USN = fv.USN
            WHERE s.USN = %s
            GROUP BY 
                s.NAME, 
                s.USN;
        """
        cursor.execute(search_query, (usn,))
        search_results = cursor.fetchall()
        for row in search_results:
            student = {
                'name': row[0],
                'usn': row[1],
                'subject_backlogs': row[2],
                'total_backlogs': row[3]
            }
            search_data.append(student)

    all_students_query = """
        SELECT 
            s.NAME, 
            s.USN, 
            COALESCE(GROUP_CONCAT(CASE WHEN fv.18CS81 < 35 THEN '18CS81' WHEN fv.18CS82 < 35 THEN '18CS82' WHEN fv.18CSP83 < 35 THEN '18CSP83' WHEN fv.18CS84 < 35 THEN '18CS84' WHEN fv.18CSI85 < 35 THEN '18CSI85' END), '') AS backlog_subjects,
            COALESCE(SUM(CASE WHEN fv.18CS81 < 35 THEN 1 WHEN fv.18CS82 < 35 THEN 1 WHEN fv.18CSP83 < 35 THEN 1 WHEN fv.18CS84 < 35 THEN 1 WHEN fv.18CSI85 < 35 THEN 1 END), 0) AS total_backlogs
        FROM 
            students s 
            JOIN final_vtu fv ON s.USN = fv.USN
        GROUP BY 
            s.NAME, 
            s.USN
        HAVING 
            total_backlogs > 0;
    """
    cursor.execute(all_students_query)
    all_students_results = cursor.fetchall()
    all_students_data = []
    for row in all_students_results:
        student = {
            'name': row[0],
            'usn': row[1],
            'subject_backlogs': row[2],
            'total_backlogs': row[3]
        }
        all_students_data.append(student)

    return render_template('check_backlogs.html', search_data=search_data, all_students_data=all_students_data)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        cnx.close()
