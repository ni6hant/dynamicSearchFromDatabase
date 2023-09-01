import sys
import os

# Add your Flask app directory to the system path
sys.path.insert(0, '/home5/nishantco/public_html/test')

# Import your Flask app (replace 'app' with the actual name of your Flask app variable)
from app import app as application

# Optional: Set the environment variable 'FLASK_ENV' to 'production'
# This is useful to ensure that Flask runs in production mode
os.environ['FLASK_ENV'] = 'production'