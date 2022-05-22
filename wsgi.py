# import sys
# sys.path.append('meal_app')

# from app import create_app as application

# app = application()

# if __name__ == "__main__":
#     app.run(host='0.0.0.0')

import os
import sys
sys.path.append('meal_app')

# from bla import app as application
from meal_app.app import create_app
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/meal_app')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')

# from meal_app.app import create_app

# from dotenv import load_dotenv

# load_dotenv()

# app = create_app()