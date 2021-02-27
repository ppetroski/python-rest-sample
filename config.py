"""
This file is intended to be git ignored and replaced with the appropriate version
from the environments folder. Including just so you don't need to worry about that step
"""

# Connection info for the database. I choose MySQL, but you can use whatever
database = {
    'driver': 'mysql+pymysql',
    'host': '127.0.0.1',  # TODO: This may need to be adjusted depending on how it is run. Docker uses it's own network IP
    'port': 3306,
    'user': 'web_user',
    'password': 'dev',
    'database': 'sample',
}

# Additional configurations will go here