from flask import Flask, render_template
import datetime
import psycopg2
#from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
#load_dotenv()
# Access environment variables
#DATABASE_HOST = os.getenv('DATABASE_HOST')
#DATABASE_PORT = os.getenv('DATABASE_PORT')
#DATABASE_USER = os.getenv('DATABASE_USER')
#DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
#DATABASE = os.getenv('DATABASE')

now = datetime.datetime.now()
next= datetime.datetime.now()
dbentry = (0,17,42,0,now,next,1) #id, len, height, gate, ts1, ts2, status, (features)

# def get_db_connection():
#     conn = psycopg2.connect(
#         host=DATABASE_HOST,
#         database=DATABASE,
#         user=DATABASE_USER,
#         password=DATABASE_PASSWORD,
#         port=DATABASE_PORT
#     )
#     return conn

@app.route('/')
def hello():
    #conn = get_db_connection()
    #cursor = conn.cursor()
    #cursor.execute('SELECT id, lenght, height, lastGate, lastSeenAt,expectedNext, status FROM parceldump')
    #rows = cursor.fetchall()
    rows=(dbentry,)
    #cursor.close()
    #conn.close()
    return render_template('index.html', rows=rows)
    #return 'Hello World'
