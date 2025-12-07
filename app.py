from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key' # Needed for flashing messages

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    # Create Books Table
    c.execute('''CREATE TABLE IF NOT EXISTS books 
                 (id INTEGER PRIMARY KEY, title TEXT, author TEXT, category TEXT, quantity INTEGER)''')
    # Create Transactions Table
    c.execute('''CREATE TABLE IF NOT EXISTS transactions 
                 (id INTEGER PRIMARY KEY, book_id INTEGER, student_name TEXT, 
                  issue_date DATE, return_date DATE, status TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- Helper to query DB ---
def query_db(query, args=(), one=False):
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# --- Routes ---

@app.route('/')
def dashboard():
    # Fetch stats for the dashboard
    total_books = query_db('SELECT SUM(quantity) as count FROM books', one=True)['count'] or 0
    active_issues = query_db('SELECT COUNT(*) as count FROM transactions WHERE status="Issued"', one=True)['count']
    recent_transactions = query_db('SELECT * FROM transactions ORDER BY id DESC LIMIT 5')
    return render_template('dashboard.html', total=total_books, active=active_issues, recent=recent_transactions)

@app.route('/books', methods=['GET', 'POST'])
def manage_books():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        category = request.form['category']
        quantity = request.form['quantity']
        query_db('INSERT INTO books (title, author, category, quantity) VALUES (?, ?, ?, ?)', 
                 (title, author, category, quantity))
        flash('Book Added Successfully!')
        return redirect(url_for('manage_books'))
    
    books = query_db('SELECT * FROM books')
    return render_template('books.html', books=books)

@app.route('/issue', methods=['GET', 'POST'])
def issue_return():
    if request.method == 'POST':
        action = request.form['action']
        
        if action == 'issue':
            book_id = request.form['book_id']
            student = request.form['student_name']
            
            # Check availability
            book = query_db('SELECT * FROM books WHERE id = ?', [book_id], one=True)
            if book and book['quantity'] > 0:
                query_db('INSERT INTO transactions (book_id, student_name, issue_date, status) VALUES (?, ?, ?, ?)',
                         (book_id, student, datetime.date.today(), 'Issued'))
                query_db('UPDATE books SET quantity = quantity - 1 WHERE id = ?', [book_id])
                flash(f'Book issued to {student}')
            else:
                flash('Error: Book not available or ID invalid.')

        elif action == 'return':
            trans_id = request.form['trans_id']
            trans = query_db('SELECT * FROM transactions WHERE id = ?', [trans_id], one=True)
            if trans and trans['status'] == 'Issued':
                query_db('UPDATE transactions SET status = "Returned", return_date = ? WHERE id = ?', 
                         (datetime.date.today(), trans_id))
                query_db('UPDATE books SET quantity = quantity + 1 WHERE id = ?', [trans['book_id']])
                flash('Book returned successfully.')
            else:
                flash('Error: Invalid Transaction ID.')
                
        return redirect(url_for('issue_return'))

    transactions = query_db('SELECT * FROM transactions WHERE status="Issued"')
    return render_template('issue.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
