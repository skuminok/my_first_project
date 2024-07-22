from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
con = sqlite3.connect('new.db', check_same_thread=False)
cur = con.cursor()

@app.route("/")
def index():
    return render_template('main.html')

@app.route("/travel/<id>")
def travel(id):
    res = cur.execute(f"select * from Travels where id = ?", (id,))
    travel = res.fetchone()
    if travel != None:
        return render_template('travel_new.html', travel=travel)
    else:
        return "Такого путешествия нет"

@app.route("/travels")
def travels():
    res = cur.execute("SELECT * FROM Travels")
    travels = res.fetchall()
    return render_template('travels.html', travels=travels)

@app.route("/travel_add", methods=['GET', 'POST'])
def travel_add():
    if request.method == 'POST':
        name = request.form['destination']
        date = request.form['travel_date']
        budget = request.form['budget']
        services = request.form['services']
        travel_data = (name, date, budget, services)
        cur.execute('INSERT INTO Travels (destination, travel_date, budget, services) VALUES (?, ?, ?, ?)', travel_data)
        con.commit()
        return redirect(url_for('travels'))
    return render_template('travel_add.html')

if __name__ == '__main__':
    app.run(debug=True)