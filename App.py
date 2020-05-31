from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
#Base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'planillas'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'planillas'
mysql = MySQL(app)
#Sesion
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados')
    data = cur.fetchall()
    return render_template('index.html', employees = data)

@app.route('/employee_form')
def employee_form():
    return render_template('employee_form.html')

@app.route('/add_employeem', methods = ['POST'])
def add_employeem():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dateofbirth = request.form['dateofbirth']
        gender = request.form['gender']
        hiredate = request.form['hiredate']
        phone = request.form['phone']
        email = request.form['email']
        designation = request.form['designation']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO empleados (nombre, apellido, nacimiento, genero, contrato, teléfono, email, designación) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (firstname, lastname, dateofbirth, gender, hiredate, phone, email, designation))
        mysql.connection.commit()
        flash('Empleado agregado')
        return redirect(url_for('Index'))

@app.route('/edit_employee/<id>')
def get_employee(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados WHERE id= %s',(id))
    data = cur.fetchall()
    return render_template('edit_employee.html', employee = data[0])

@app.route('/delete_employee/<string:id>', methods = ['POST','GET'])
def delete_employee(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM empleados WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Empleado removido')
    return redirect(url_for('Index'))

@app.route('/update/<id>', methods = ['POST'])
def update_employee(id):
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dateofbirth = request.form['dateofbirth']
        gender = request.form['gender']
        hiredate = request.form['hiredate']
        phone = request.form['phone']
        email = request.form['email']
        designation = request.form['designation']
        cur = mysql.connection.cursor()
        cur.execute(""" 
        UPDATE empleados 
        SET nombre = %s,
            apellido = %s,
            nacimiento = %s,
            genero = %s,
            contrato = %s,
            teléfono = %s,
            email = %s,
            designación = %s
        WHERE id = %s
        """, (firstname, lastname, dateofbirth, gender, hiredate, phone, email, designation, id))
        mysql.connection.commit()
        flash('Empleado actualizado')
        return redirect(url_for('Index'))

@app.route('/leave_index/<empleado>')
def leave_index(empleado):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM licencias WHERE empleado = %s',(empleado))
    data = cur.fetchall()
    return render_template('leave_index.html', leave = data)

@app.route('/add_leave/<empleado>', methods = ['POST'])
def add_leave(empleado):
    if request.method == 'POST':
        employee = empleado
        date = request.form['date']
        motiv = request.form['motiv']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO licencias (empleado, fecha, motivo) VALUES (%s,%s,%s)", (employee,date,motiv))
        mysql.connection.commit()
        flash('Licencia agregada')
        return redirect(url_for('Index'))


@app.route('/holiday_index')
def holiday_index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM feriados')
    data = cur.fetchall()
    return render_template('holiday_index.html', holidays = data)

@app.route('/add_holiday', methods = ['POST'])
def add_holiday():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO feriados (nombre, fecha) VALUES (%s,%s)", (name, date))
        mysql.connection.commit()
        flash('Feriado agregado')
        return redirect(url_for('holiday_index'))

@app.route('/delete_holiday/<string:id>', methods = ['POST','GET'])
def delete_holiday(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM feriados WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Feriado removido')
    return redirect(url_for('holiday_index'))

@app.route('/make_slips')
def make_slips():
    return 'Generar planilla'


if __name__=='__main__':
    app.run(port = 3000, debug=True)