from dotenv import load_dotenv
from config.database import init_db
from flask import Flask

load_dotenv()

app = Flask(__name__)

try:
    init_db(app)
    print("✓ Database connection successful!")
except Exception as e:
    print(f"✗ Connection failed: {e}")
