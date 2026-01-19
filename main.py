from flask import Flask, request, render_template, url_for, redirect, flash, session
from markupsafe import escape
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime as dt
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
        if "user_id" in session:
            user = db.query(User).filter(User.id == session["user_id"]).first()
            if not user:
                session.pop("user_id", None)
                user = None
        else:
            user = None
        if not user:
            user = db.query(User).first()
            if user:
                session["user_id"] = user.id
        if not user:
            return render_template('landing.html', user=None)
        
        tasks = db.query(Task).filter(Task.user_id == user.id).all()
        tasks_list = []
        for task in tasks:
            task_dict = {
                "id": task.id,
                "title": task.title,
                "content": task.content,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "due_time": str(task.due_time) if task.due_time else None
            }
            tasks_list.append(task_dict)
        
        user_data = {
            "id": user.id,
            "username": user.username,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            "tasks": tasks_list
        }
        
        form_data = session.get("form_data", {})
        
        return render_template('landing.html', user=user_data, form_data=form_data)
    
    except Exception as e:
        session.pop('user_id', None)
        flash("Database error", "error")
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
        db.refresh(new_user)
        session["user_id"] = new_user.id
        flash(f"Welcome {username}!", "success")
        return redirect(url_for('index'))
    except Exception:
        session.pop('user_id', None)
        flash("Error creating user", "error")
    finally:
        if db:
            db.close()
    return redirect(url_for('index'))

@app.route("/create_task", methods=["POST"])
def create_task():
    if "user_id" not in session:
        flash("Please register first", "error")
        return redirect(url_for('index'))
    db = None
    try:
        db = next(get_db())
        user = db.query(User).filter(User.id == session["user_id"]).first()
        if not user:
            flash("User not found. Please register again.", "error")
            session.pop("user_id", None)
            return redirect(url_for('index'))
        
        title = request.form.get("title", '').strip()
        content = request.form.get("content", '').strip()
        priority = request.form.get("priority", '2')
        due_date_str = request.form.get("due_date", '')
        due_time_str = request.form.get("due_time", '')
        
        if not title or not content:
            flash("Title and description are required", "error")
            session["form_data"] = request.form.to_dict()
            return redirect(url_for('index'))
        
        existing_task = db.query(Task).filter(Task.title == escape(title)).first()
        if existing_task:
            flash("Task with this title already exists", "error")
            session["form_data"] = request.form.to_dict()
            return redirect(url_for('index'))
        
        due_date = None
        due_time = None
        
        # Only parse if strings are not empty
        if due_date_str and due_date_str.strip():
            try:
                due_date = dt.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                # If invalid format, just leave as None
                due_date = None
                
        if due_time_str and due_time_str.strip():
            try:
                due_time = dt.strptime(due_time_str, '%H:%M').time()
            except ValueError:
                # If invalid format, just leave as None
                due_time = None
        
        new_task = Task(
            title=title,
            content=content,
            priority=int(priority),
            due_date=due_date,
            due_time=due_time,
            user_id=session["user_id"]
        )
        
        db.add(new_task)
        db.commit()
        
        if "form_data" in session:
            session.pop("form_data", None)
        
        flash("Task created successfully!", "success")
        return redirect(url_for('index'))
        
    except Exception:
        flash("Error creating task", "error")
        session["form_data"] = request.form.to_dict()
    finally:
        if db:
            db.close()
    
    return redirect(url_for('index'))

@app.route("/update_task", methods=["POST"])
def update_task():
    if "user_id" not in session:
        flash("Please register first", "error")
        return redirect(url_for('index'))
    db = None
    try:
        db = next(get_db())
        task_id = request.form.get("task_id")
        if not task_id:
            flash("Task ID is required", "error")
            session["form_data"] = request.form.to_dict()
            return redirect(url_for('index'))
        
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == session["user_id"]).first()
        if not task:
            flash("Task not found", "error")
            session["form_data"] = request.form.to_dict()
            return redirect(url_for('index'))
        
        title = request.form.get("title", '').strip()
        content = request.form.get("content", '').strip()
        priority = request.form.get("priority", '2')
        due_date_str = request.form.get("due_date", '')
        due_time_str = request.form.get("due_time", '')
        
        if not title or not content:
            flash("Title and description are required", "error")
            session["form_data"] = request.form.to_dict()
            return redirect(url_for('index'))
        
        existing_task = db.query(Task).filter(Task.title == escape(title), Task.id != task_id).first()
        if existing_task:
            flash("Task with this title already exists", "error")
            session["form_data"] = request.form.to_dict()
            return redirect(url_for('index'))
        
        due_date = None
        due_time = None
        if due_date_str:
            due_date = dt.strptime(due_date_str, '%Y-%m-%d').date()
        if due_time_str:
            due_time = dt.strptime(due_time_str, '%H:%M').time()
        
        task.title = title
        task.content = content
        task.priority = int(priority)
        task.due_date = due_date
        task.due_time = due_time
        
        db.commit()
        
        if "form_data" in session:
            session.pop("form_data", None)
        
        flash("Task updated successfully!", "success")
        return redirect(url_for('index'))
        
    except ValueError:
        flash("Invalid date or time format", "error")
        session["form_data"] = request.form.to_dict()
    except Exception:
        flash("Error updating task", "error")
        session["form_data"] = request.form.to_dict()
    finally:
        if db:
            db.close()
    
    return redirect(url_for('index'))