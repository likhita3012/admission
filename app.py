from flask import Flask, request, render_template, session, redirect, url_for
#from home import home_blueprint
#from home.home import home_blueprint

import mysql.connector

#home_blueprint = Blueprint('home', __name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MySQL connection
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="likitha",
    database="admission"
)
cursor = mysql_conn.cursor()

# Define a route to display the form
@app.route('/')
def index():
    return render_template('home.html')

#@home_blueprint.route('/redirect')
def redirect_to_home():
    # Redirect to the home page (assuming it's mapped to '/')
    return redirect(url_for('home'))
@app.route('/uni')
def univer():
    return render_template('university.html')

@app.route('/help')
def help():
    return render_template('help.html')   

@app.route('/reg')
def registration():
    return render_template('registration.html')    

   
# Define a route to handle the form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        email = request.form['email']
        password=request.form['password']
        confirmpassword=request.form['confirmpassword']

        # Insert data into MySQL
        query = "INSERT INTO registration (name, email,password,confirmpassword) VALUES (%s, %s, %s, %s)"
        values = (name, email,password,confirmpassword)
        cursor.execute(query, values)
        mysql_conn.commit()

        #return 'Data inserted successfully!'
        return render_template('success.html', msg='data inserted successfully!')

@app.route('/')
def home():
    if 'username' in session:
        return f'Logged in as {session["email"]}'
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        print(email)
        password = request.form['password']
        print(password)
        # Check if user exists in the database
        query = "SELECT * FROM registration WHERE email = %s AND password = %s"
        values = (email, password)
        cursor.execute(query, values)
        user = cursor.fetchone()
        if user:
            session['email'] = email
            return 'Student logged In Sucessufully'
        else:
            return 'Invalid username or password'
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')


@app.route('/sub', methods=['POST'])
def university():
    
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        email = request.form['email']
        location=request.form['location']
        naac=request.form['naac']
        ranking=request.form['ranking']
        iitcutoff=request.form['iitcutoff']
        scholardetails=request.form['scholardetails']
        placementrate=request.form['placementrate']

        # Insert data into MySQL
        query = "INSERT INTO university (name, email,location,naac,ranking,iitcutoff,scholardetails,placementrate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, email,location,naac,ranking,iitcutoff,scholardetails,placementrate)
        cursor.execute(query, values)
        mysql_conn.commit()

        #return 'University data inserted Sucessfully'
        return render_template('sucess2.html', msg='University inserted successfully!')


@app.route('/display_data')
def display_data():
    # Connect to MySQL database
    conn = mysql.connector.connect
    #conn = mysql_conn.cursor()
    cursor = mysql_conn.cursor()
    #cursor = conn.cursor()
    userrank = request.args.get("userrank")

    # Fetch data from MySQL table
    cursor.execute('SELECT * FROM university where iitcutoff>'+str(userrank))
    data = cursor.fetchall()

    # Close cursor and connection
    #cursor.close()
    #conn.close()


    # Pass data to HTML template
    return render_template('display.html', data=data)        

@app.route('/display_data_branch')
def display_data_branch():
    # Connect to MySQL database
    conn = mysql.connector.connect
    #conn = mysql_conn.cursor()
    cursor = mysql_conn.cursor()
    #cursor = conn.cursor()
    university = request.args.get("university")
    userrank = request.args.get("userrank")
    propability = request.args.get("propability")
    scholarship = request.args.get("scholarship")

    # Fetch data from MySQL table
    #cursor.execute('SELECT * FROM prediction where universityname=\''+university+'\' and cutoff>'+str(userrank))
    cursor.execute('SELECT * FROM prediction where universityname=\''+university+'\' and cutoff>'+str(propability)+str(scholarship)+str(userrank))
    data = cursor.fetchall()

    # Close cursor and connection
    #cursor.close()
    #conn.close()


    # Pass data to HTML template
    return render_template('display_branch.html', data=data)
    #return render_template('sucess3.html')

    



@app.route('/std')
def std():
    # Query data from MySQL table
    cursor.execute("SELECT * FROM university")
    data1 = cursor.fetchall()

    # Pass data to HTML template for rendering
    return render_template('std.html', data=data1)

@app.route('/std2', methods=['POST', 'GET'])
def std2():
    if request.method == 'GET':

        st='SELECT distinct name FROM university'
        conn = mysql.connector.connect
        #conn = mysql_conn.cursor()
        cursor = mysql_conn.cursor()
        cursor.execute(st);
        print(st)
        #print(st)
        #cursor.execute(st)
        data = cursor.fetchall()


        return render_template('std2.html',data=data)
    else:
        # Connect to MySQL database
        conn = mysql.connector.connect
        #conn = mysql_conn.cursor()
        cursor = mysql_conn.cursor()
        #cursor = conn.cursor()
        opuniv = request.form["opuniv"]
        tbrank = request.form["tbrank"]

        # Fetch data from MySQL table
        #cursor.execute('SELECT * FROM prediction where universityname=\''+university+'\' and cutoff>'+str(userrank))
        #st='SELECT * FROM prediction where universityname=\''+opuniv+'\' and cutoff>'+str(tbrank)
        

        st='SELECT *,(cutoff-'+tbrank+    ')/cutoff*100 as prob FROM prediction where universityname=\''+opuniv+'\' and cutoff>'+str(tbrank)
        cursor.execute(st);
        print(st)
        #print(st)
        #cursor.execute(st)
        data = cursor.fetchall()

        # Close cursor and connection
        #cursor.close()
        #conn.close()


        # Pass data to HTML template
        return render_template('display_branch.html', data=data)
        return render_template('sucess3.html')

    
if __name__ == '__main__':
    app.run(debug=True)
