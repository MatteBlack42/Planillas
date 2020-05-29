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

@app.route('/add_leave')
def add_leave():
    return 'Añadir licencia'

@app.route('/add_holiday')
def add_holiday():
    return 'Añadir feriado corporativo'

@app.route('/make_slips')
def make_slips():
    return 'Generar planilla'


if __name__=='__main__':
    app.run(port = 3000, debug=True)