from flask import Flask, request, render_template, url_for, redirect, flash, session
from markupsafe import escape
from dotenv import load_dotenv
from pathlib import Path

from core.database.db import get_base, get_engine, get_db
from core.models.user import User
from core.models.task import Task

import os


load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

root_dir = Path(__file__).parent
storage_dir = root_dir / "core" / "storage"
storage_dir.mkdir(parents=True, exist_ok=True)

get_base().metadata.create_all(bind=get_engine())


@app.route("/", methods=["GET"])
def index():
    db = None
    
    try:
        db = next(get_db())
        user = db.query(User).first()

        if not user:
            user = None
            session["user"] = None
        
        else:
            session["user"] = {
                "id": user.id,
                "username": user.username,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "tasks": user.tasks
            }

        return render_template('landing.html', user=session["user"])
    
    except Exception as e:
        print(f"Database error: {e}")
        session.pop('user', None)
    
    finally:
        if db:
            db.close()
    
    return redirect(url_for('index'))

@app.route("/register", methods=["POST"])
def register():
    db = None

    try:
        db = next(get_db())
        username = request.form.get("username", '').strip()
    
        if not username:
            flash("Username cannot be empty", "error")
            return redirect(url_for('index'))
    
        found_user = db.query(User).filter(User.username == escape(username)).first()
    
        if found_user:
            flash("Username Already Exists", "error")
            return redirect(url_for('index'))
    
        new_user = User(username=username)
        
        db.add(new_user)
        db.commit()

        session["user"] = {
            "id": new_user.id,
            "username": new_user.username,
            "created_at": new_user.created_at,
            "updated_at": new_user.updated_at,
            "tasks": new_user.tasks
        }
    
        return redirect(url_for('index'))
    
    except Exception as e:
        print(f"Unknown Exception: {e}")
        session.pop('user', None)
    
    finally:
        if db:
            db.close()
    
    return redirect(url_for('index'))

@app.route("/create_task", methods=["POST"])
def create_task():
    if "user" not in session or not session["user"]:
        flash("Please register first", "error")
        return redirect(url_for('index'))
    
    db = None
    try:
        db = next(get_db())
        
        title = request.form.get("title", '').strip()
        content = request.form.get("content", '').strip()
        priority = request.form.get("priority", '2')
        due_date_str = request.form.get("due_date", '')
        due_time_str = request.form.get("due_time", '')
        
        # Validate required fields
        if not all([title, content, due_date_str, due_time_str]):
            flash("All fields are required", "error")
            return redirect(url_for('index'))
        
        # Check if task title already exists
        existing_task = db.query(Task).filter(Task.title == escape(title)).first()
        if existing_task:
            flash("Task with this title already exists", "error")
            return redirect(url_for('index'))
        
        # Parse date and time
        from datetime import datetime as dt
        due_date = dt.strptime(due_date_str, '%Y-%m-%d').date()
        due_time = dt.strptime(due_time_str, '%H:%M').time()
        
        # Create new task
        new_task = Task(
            title=title,
            content=content,
            priority=int(priority),
            due_date=due_date,
            due_time=due_time,
            user_id=session["user"]["id"]
        )
        
        db.add(new_task)
        db.commit()
        
        # Update session with new task
        session["user"]["tasks"].append({
            "id": new_task.id,
            "title": new_task.title,
            "content": new_task.content,
            "priority": new_task.priority,
            "due_date": new_task.due_date.isoformat(),
            "due_time": new_task.due_time.isoformat(),
            "completed": new_task.completed
        })
        
        flash("Task created successfully!", "success")
        return redirect(url_for('index'))
        
    except ValueError as e:
        flash(f"Invalid date or time format: {str(e)}", "error")
    except Exception as e:
        print(f"Error creating task: {e}")
        flash("Error creating task", "error")
    finally:
        if db:
            db.close()
    
    return redirect(url_for('index'))