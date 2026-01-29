from flask import Flask, jsonify, request
import psycopg2
import os
import time

app = Flask(__name__)

def get_db_connection():
    """Read secrets and connect to PostgreSQL with retry logic"""
    with open('/run/secrets/db_user') as f:
        db_user = f.read().strip()
    with open('/run/secrets/db_password') as f:
        db_password = f.read().strip()
    
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host='db',
                database='mydb',
                user=db_user,
                password=db_password,
                connect_timeout=3
            )
            return conn
        except psycopg2.OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Database connection failed (attempt {attempt + 1}/{max_retries}), retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to connect after {max_retries} attempts")
                raise

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, title, completed FROM todos ORDER BY id')
    todos = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify([
        {'id': todo[0], 'title': todo[1], 'completed': todo[2]}
        for todo in todos
    ])

@app.route('/api/todos', methods=['POST'])
def create_todo():
    """Create new todo"""
    data = request.get_json()
    title = data.get('title', '')
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO todos (title, completed) VALUES (%s, %s) RETURNING id',
        (title, False)
    )
    todo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({'id': todo_id, 'title': title, 'completed': False}), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update todo (toggle completed status)"""
    data = request.get_json()
    completed = data.get('completed')
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'UPDATE todos SET completed = %s WHERE id = %s',
        (completed, todo_id)
    )
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({'id': todo_id, 'completed': completed})

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete todo"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM todos WHERE id = %s', (todo_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

