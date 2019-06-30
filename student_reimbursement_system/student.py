import sqlite3
from flask import Flask, render_template, g, request, abort
import json
app = Flask(__name__)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect('student.db')
    rv.row_factory = sqlite3.Row
    return rv

def setup_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def dict_from_row(row):
    return dict(zip(row.keys(), row))

@app.route('/')
def index():
    return "Student reimbursement system"

@app.route('/student', methods=['POST'])
def insert_student():
    data = request.get_json()
    db = connect_db()
    db.execute('insert into student (name, email, ph_no, international, dept_id) values (?, ?, ?, ?, ?)',
                 [data['name'], data['email'], data['ph_no'],data['int'],data['dept']])
    db.commit()
    print 'ok'
    cur = db.execute('select * from student where email=?',[data['email']])
    ids = []
    row = cur.fetchone()
    try:
        response = str(row['id'])
    except:
        abort(404)
    return response
    # for row in cur.fetchone():
    #     ids += str(row['id'])
    # return " ".join(ids)

@app.route('/student/<int:student_id>',methods=['GET'])
def get_student(student_id):
    db = connect_db()
    cur = db.execute('select * from student where id=?',[student_id])
    out = []
    row = cur.fetchone()
    try:
        response = json.dumps(dict_from_row(row))
    except:
        abort(404)
    return response
    
@app.route('/student/<int:student_id>/expense', methods=['POST'])
def insert_expense(student_id):
    data = request.get_json()
    db = connect_db()
    db.execute('insert into expenses (title, amount, description, s_id) values (?, ?, ?, ?)',
                [data['title'],data['amt'],data['desc'],student_id])
    db.commit()
    cur = db.execute('select * from expenses where s_id=?',[student_id])
    out = ""
    try:
        for row in cur.fetchall():
            out += json.dumps(dict_from_row(row)) + "\n"
            print out
        return str(out)
    except:
        abort(404)

@app.route('/dept/<int:dept_id>')
def get_dept(dept_id):
    return


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
