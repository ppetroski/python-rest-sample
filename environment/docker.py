# Connection info for the database. I choose MySQL, but you can use whatever
database = {
    'driver': 'mysql+pymysql',
    'host': '172.17.0.1',  # TODO: This is my docker network IP. Yours might differ
    'port': 3306,
    'user': 'web_user',
    'password': 'dev',
    'database': 'sample',
}

# Additional configurations will go here
