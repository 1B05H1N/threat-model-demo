import os
from flask import Flask, request, jsonify, session, render_template_string
from functools import wraps
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Security Configuration
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# Initialize security components
csrf = CSRFProtect(app)
limiter = Limiter(key_func=get_remote_address, app=app)

# In-memory storage for todos (replace with database in production)
todos = []

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.get("/")
def landing():
    return render_template_string("""
        <h1>Welcome to the Todo API</h1>
        <p>This is an API for managing todos.</p>
        <p>Use the following endpoints:</p>
        <ul>
            <li>POST /login - Authenticate</li>
            <li>POST /logout - Logout</li>
            <li>GET /dashboard - View your todos</li>
            <li>GET /todos - List all todos</li>
            <li>POST /todos - Create a todo</li>
            <li>PUT /todos/&lt;id&gt; - Update a todo</li>
            <li>DELETE /todos/&lt;id&gt; - Delete a todo</li>
        </ul>
    """)

@app.post("/login")
@limiter.limit("5 per minute")
def login():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400

    username = data['username']
    password = data['password']

    # In production, validate against database
    if username == os.getenv('ADMIN_USERNAME') and check_password_hash(
        generate_password_hash(os.getenv('ADMIN_PASSWORD')), password
    ):
        session['user_id'] = username
        return jsonify({'message': 'Login successful'}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.post("/logout")
@login_required
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@app.get("/dashboard")
@login_required
def dashboard():
    user_todos = [todo for todo in todos if todo.get('user_id') == session['user_id']]
    return render_template_string("""
        <h1>Your Todos</h1>
        <ul>
            {% for todo in todos %}
            <li>{{ todo.title }} - {{ todo.status }}</li>
            {% endfor %}
        </ul>
        <p><a href="/logout">Logout</a></p>
    """, todos=user_todos)

@app.get("/todos")
@login_required
@limiter.limit("10 per minute")
def get_todos():
    user_todos = [todo for todo in todos if todo.get('user_id') == session['user_id']]
    return jsonify(user_todos), 200

@app.post("/todos")
@login_required
@limiter.limit("10 per minute")
def create_todo():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    todo = {
        'id': len(todos) + 1,
        'title': data['title'],
        'status': 'pending',
        'user_id': session['user_id']
    }
    todos.append(todo)
    return jsonify(todo), 201

@app.put("/todos/<int:todo_id>")
@login_required
@limiter.limit("10 per minute")
def update_todo(todo_id):
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    todo = next((t for t in todos if t['id'] == todo_id and t['user_id'] == session['user_id']), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    if 'title' in data:
        todo['title'] = data['title']
    if 'status' in data:
        todo['status'] = data['status']

    return jsonify(todo), 200

@app.delete("/todos/<int:todo_id>")
@login_required
@limiter.limit("10 per minute")
def delete_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id and t['user_id'] == session['user_id']), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    todos.remove(todo)
    return '', 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000) 