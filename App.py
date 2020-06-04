from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import InputRequired, Email, Length
import pdfkit
import datetime

app = Flask(__name__)
#Base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'planillas'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'planillas'
mysql = MySQL(app)
#Sesion
app.secret_key = 'mysecretkey'

#Ruta inicial, muestra todos los empleados
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados')
    data = cur.fetchall()
    return render_template('index.html', employees = data)

#Añadir un empleado
#Muestra el formulario
@app.route('/employee_form')
def employee_form():
    form = employeeform()
    return render_template('employee_form.html',form=form)

#Formulario Flask, para realizar la validación 
class employeeform(FlaskForm):
    firstname = StringField('Firstname', validators=[InputRequired('Ingrese el Nombre')])
    lastname = StringField('Lastname', validators=[InputRequired('Ingrese el Apellido')])
    dateofbirth = DateField('Dateofbirth', validators=[InputRequired('Ingrese la Fecha de nacimiento')], format ='%Y-%m-%d')
    gender = StringField('Gender', validators=[InputRequired('Ingrese el Género')])
    hiredate = DateField('Hiredate', validators=[InputRequired('Ingrese la Fecha de contratación')])
    phone = StringField('Phone', validators=[InputRequired('Ingrese el Telefono'),Length(min=9, max=9, message='Teléfono no válido')])
    email = StringField('Email', validators=[InputRequired('Ingrese el Email'),Email('Email no válido')])
    designation = StringField('Designation', validators=[InputRequired('Ingrese la designación')])

#Inserta los datos del fomrulario en la base de datos
@app.route('/add_employeem', methods = ['POST'])
def add_employeem():
    if request.method == 'POST':
        form = employeeform()
        if form.validate_on_submit():
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
        return render_template('employee_form.html',form=form)
        
#Editar un empleado
#Muestra el formulario para editar un empelado
@app.route('/edit_employee/<id>')
def get_employee(id):
    form = employeeform()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados WHERE id= %s',[id])
    data = cur.fetchall()
    return render_template('edit_employee.html', employee = data[0], form=form)


#Eliminar un empleado
@app.route('/delete_employee/<string:id>', methods = ['POST','GET'])
def delete_employee(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM empleados WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Empleado removido')
    return redirect(url_for('Index'))

#Actualiza los datos del empleado
@app.route('/update/<id>', methods = ['POST'])
def update_employee(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados WHERE id= %s',[id])
    data = cur.fetchall()
    if request.method == 'POST':
        form = employeeform()
        if form.validate_on_submit():
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
        return render_template('edit_employee.html',form=form,employee=data[0])

#Añadir una licencia a un empleado
#Muestra el formulario para añadir una licencia
@app.route('/leave_index/<empleado>')
def leave_index(empleado):
    form = leaveform()
    employee=empleado
    return render_template('leave_index.html', employee=employee ,form=form)


#Formulario Flask, para realizar la validación 
class leaveform(FlaskForm):
    date = DateField('Date', validators=[InputRequired('Ingrese la Fecha')], format ='%Y-%m-%d')
    motiv = StringField('Motiv', validators=[InputRequired('Ingrese el Motivo')])


#Añade La licencia a la base de datos    
@app.route('/add_leave/<empleado>', methods = ['POST'])
def add_leave(empleado):
    employee=empleado
    if request.method == 'POST':
        form = leaveform()
        if form.validate_on_submit():
            employee = empleado
            date = request.form['date']
            motiv = request.form['motiv']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO licencias (empleado, fecha, motivo) VALUES (%s,%s,%s)", (employee,date,motiv))
            mysql.connection.commit()
            flash('Licencia agregada')
            return redirect(url_for('Index'))
        return render_template('leave_index.html', form=form,employee=employee)


#Añadir un Feriado
#Muestra los feriados y el formulario para un nuevo feriado
@app.route('/holiday_index')
def holiday_index():
    form=holidayform()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM feriados')
    data = cur.fetchall()
    return render_template('holiday_index.html', holidays = data,form=form)


#Formulario Flask, para realizar la validación 
class holidayform(FlaskForm):
    name = StringField('Name', validators=[InputRequired('Ingrese el Nombre')])
    date = DateField('Date', validators=[InputRequired('Ingrese la Fecha')], format ='%Y-%m-%d')
    
#Añade los datos del feriado a la base de datos
@app.route('/add_holiday', methods = ['POST'])
def add_holiday():
    form=holidayform()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM feriados')
    data = cur.fetchall()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form['name']
            date = request.form['date']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO feriados (nombre, fecha) VALUES (%s,%s)", (name, date))
            mysql.connection.commit()
            cur.execute('SELECT * FROM feriados')
            data = cur.fetchall()
            flash('Feriado agregado')
            return render_template('holiday_index.html',holidays = data, form=form)
        return render_template('holiday_index.html',holidays = data, form=form)

#Elimina un feriado
@app.route('/delete_holiday/<string:id>', methods = ['POST','GET'])
def delete_holiday(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM feriados WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Feriado removido')
    return redirect(url_for('holiday_index'))

#Generar planillas
#Calcula los datos necesarios de la planilla, y los envia a un HTML, luego es convertido en pdf
@app.route('/make_slips/<id>')
def make_slips(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados WHERE id= %s',[id])
    data = cur.fetchall()

    now=datetime.datetime.now()

    curb = mysql.connection.cursor()
    curb.execute('SELECT COUNT(*) FROM licencias WHERE empleado = %s AND EXTRACT(MONTH FROM fecha) = %s AND EXTRACT(YEAR FROM fecha) = %s',(id,now.month,now.year))
    licencia=curb.fetchall()
    licencias=licencia[0][0]*47
    minimo=930
    desig = data[0][8]
    switcher = {
         "Gerente": 570,
         "Empleado":270,
         "Contratado":0
    }
    cargo=switcher.get(desig)
    tIngresos=minimo+cargo
    afp=(10/100)*tIngresos
    tdescuentos=afp+licencias
    tneto=tIngresos-tdescuentos
    rendered = render_template('planilla.html', employee = data[0],minimo = minimo,cargo = cargo,tIngresos=tIngresos,afp=afp,licencias=licencias,tdescuentos=tdescuentos,tneto=tneto,fecha=now)
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition']='inline; filename=planilla.pdf'
    return response

if __name__=='__main__':
    app.run(port = 3000, debug=True)