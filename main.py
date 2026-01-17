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


@app.route("/")
def index():
    db = None
    
    try:
        db = next(get_db())
        user = db.query(User).first()

        if not user:
            user = None

        return render_template('landing.html', user=user)
    
    except Exception as e:
        print(f"Database error: {e}")
        session.pop('user', None)
    
    finally:
        if db:
            db.close()
    
    return redirect(url_for('index'))