import os
import sys
sys.path.append('meal_app')

from meal_app.app import create_app
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/meal_app')
load_dotenv(os.path.join(project_folder, '.env'))

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
