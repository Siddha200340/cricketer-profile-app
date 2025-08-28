from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS players
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  style TEXT NOT NULL,
                  matches INTEGER DEFAULT 0,
                  runs INTEGER DEFAULT 0,
                  wickets INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        name = request.form['name']
        style = request.form['style']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO players (name, style) VALUES (?, ?)", (name, style))
        conn.commit()
        conn.close()

        return redirect('/performance')

    return render_template('add_player.html')

@app.route('/performance')
def performance():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM players")
    players = c.fetchall()
    conn.close()
    return render_template('performance.html', players=players)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

