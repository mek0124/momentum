"""
Momentum - A local-first task manager web application.
Built with Flask, SQLite, and modern HTML/CSS/JS.
"""

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from pathlib import Path

# Initialize Flask app
app = Flask(__name__)

# Configure database - store in user's home directory
if os.environ.get('VERCEL'):
    data_dir = Path('/tmp/.momentum')
else:
    home = Path.home()
    data_dir = home / ".momentum"

data_dir.mkdir(parents=True, exist_ok=True)
db_path = data_dir / "main.db"

data_dir.mkdir(parents=True, exist_ok=True)
db_path = data_dir / "main.db"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.urandom(24).hex()

# Initialize database
db = SQLAlchemy(app)


# ==================== Models ====================

class Task(db.Model):
    """Task model for storing tasks."""
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# ==================== Routes ====================

@app.route("/")
def index():
    """Render the main application page."""
    return render_template("index.html")


# ==================== API Endpoints ====================

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Get all tasks, optionally filtered by status."""
    status = request.args.get("status")
    
    query = Task.query.order_by(Task.created_at.desc())
    
    if status == "completed":
        query = query.filter_by(completed=True)
    elif status == "active":
        query = query.filter_by(completed=False)
    
    tasks = query.all()
    return jsonify({"tasks": [task.to_dict() for task in tasks]})


@app.route("/api/tasks", methods=["POST"])
def create_task():
    """Create a new task."""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    
    if not title:
        return jsonify({"error": "Title is required"}), 400
    
    # Check for duplicate title
    existing = Task.query.filter_by(title=title).first()
    if existing:
        return jsonify({"error": "A task with this title already exists"}), 409
    
    try:
        task = Task(title=title, content=content)
        db.session.add(task)
        db.session.commit()
        return jsonify({"message": "Task created successfully", "task": task.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create task: {str(e)}"}), 500


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Get a single task by ID."""
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify({"task": task.to_dict()})


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update an existing task."""
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Update fields if provided
    if "title" in data:
        new_title = data["title"].strip()
        if new_title:
            # Check for duplicate title (excluding current task)
            existing = Task.query.filter(
                Task.title == new_title,
                Task.id != task_id
            ).first()
            if existing:
                return jsonify({"error": "A task with this title already exists"}), 409
            task.title = new_title
    
    if "content" in data:
        task.content = data["content"].strip()
    
    if "completed" in data:
        task.completed = bool(data["completed"])
    
    try:
        db.session.commit()
        return jsonify({"message": "Task updated successfully", "task": task.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update task: {str(e)}"}), 500


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task."""
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete task: {str(e)}"}), 500


@app.route("/api/tasks/bulk-delete", methods=["POST"])
def bulk_delete():
    """Delete multiple tasks at once."""
    data = request.get_json()
    task_ids = data.get("ids", [])
    
    if not task_ids:
        return jsonify({"error": "No task IDs provided"}), 400
    
    try:
        Task.query.filter(Task.id.in_(task_ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({"message": f"Deleted {len(task_ids)} task(s)"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete tasks: {str(e)}"}), 500


@app.route("/api/tasks/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    """Toggle task completion status."""
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    task.completed = not task.completed
    
    try:
        db.session.commit()
        return jsonify({"message": "Task toggled", "task": task.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to toggle task: {str(e)}"}), 500


# ==================== Database Initialization ====================

def init_db():
    """Initialize the database tables."""
    with app.app_context():
        db.create_all()
        print(f"Database initialized at: {db_path}")


init_db()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)