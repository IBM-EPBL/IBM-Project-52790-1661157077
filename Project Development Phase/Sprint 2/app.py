from turtle import st

import ibm_db
from flask import Flask, redirect, render_template, request, session, url_for
from markupsafe import escape

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME="8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud:30120";PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dkh61031;PWD=rqycm4sm7SZU2TYW",'','')
app = Flask(__name__)
app.secret_key='a'


@app.route('/')
@app.route('/register')
def register():
  return render_template('register.html')
@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/home')
def home():
  return render_template('home.html')



@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/addExpense')
def addExpense():
    return render_template('AddExpense.html')




@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
  if request.method == 'POST':

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    password= request.form['password']

    sql = "SELECT * FROM USERS WHERE NAME =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('login.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO USERS (Name,email,phone,password) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email )
      ibm_db.bind_param(prep_stmt, 3, phone)
      ibm_db.bind_param(prep_stmt, 4, password)
      ibm_db.execute(prep_stmt)
    
    return render_template('login.html', msg="Registered successfuly..")






@app.route('/signin', methods =['GET', 'POST'])
def signIn():
    global userid
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        sql ="SELECT * FROM USERS WHERE  email = ? AND password = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
            
        if account:
            session['loggedin'] = True
            session['id'] = account['USERID']
            userid=account['USERID']
            session['username']=account['NAME']

            #session["name"] = request.form.get("name")
            
            #session['username'] = account['Name']
            msg = 'Welcome'+" "+session['username']+"!!"
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
        return render_template('login.html', msg = msg)





@app.route('/add', methods =['GET', 'POST'])
def add():
    global id
    if request.method=='POST':
      date=request.form['date']
      name=request.form['expenseName']
      amount=request.form['expenseAmount']
      category=request.form['expenseCategory']
      paymethod=request.form['payMethod']
      id=session['id']
      print(id)
      insert_sql = "INSERT INTO EXPENSE (USERID,DATE,NAME,AMOUNT,CATEGORY,PAYMENTMETHOD) VALUES (?,?,?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, id)
      ibm_db.bind_param(prep_stmt, 2, date )
      ibm_db.bind_param(prep_stmt, 3, name)
      ibm_db.bind_param(prep_stmt, 4, amount)
      ibm_db.bind_param(prep_stmt, 5, category)
      ibm_db.bind_param(prep_stmt, 6, paymethod)
      ibm_db.execute(prep_stmt)
    
    return render_template('history.html', msg="Data saved successfuly..")

      
      

@app.route('/history')
def history():
  print(session['username'])
  students = []
  sql = "SELECT * FROM EXPENSE"
  stmt = ibm_db.exec_immediate(conn, sql)
  dictionary = ibm_db.fetch_both(stmt)
  while dictionary != False:
    # print ("The Name is : ",  dictionary)
    students.append(dictionary)
    dictionary = ibm_db.fetch_both(stmt)

  if students:
    return render_template("history.html", students = students)


@app.route('/logout')
def logout():
  session.pop('loggedin', None)
  session.pop('id', None)
  session.pop('username', None)
  return render_template('register.html')

if __name__ =='__main__':
    app.run(host='0.0.0.0',debug=True)