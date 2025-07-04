from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize DB with category and description
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  date TEXT, 
                  title TEXT, 
                  amount REAL,
                  category TEXT,
                  description TEXT)''')
    conn.commit()
    conn.close()

# Home route - show all expenses
@app.route('/')
def index():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = c.fetchall()
    c.execute("SELECT SUM(amount) FROM expenses")
    total = c.fetchone()[0]
    conn.close()
    return render_template('index.html', expenses=expenses, total=total or 0)

# Add new expense
@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    title = request.form['title']
    amount = float(request.form['amount'])
    category = request.form.get('category', 'Other')
    description = request.form.get('description', '')

    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (date, title, amount, category, description) VALUES (?, ?, ?, ?, ?)",
              (date, title, amount, category, description))
    conn.commit()
    conn.close()
    return redirect('/')

# Delete expense
@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete(expense_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Run app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
