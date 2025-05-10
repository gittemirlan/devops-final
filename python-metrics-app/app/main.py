from flask import Flask, request
import psycopg2
import logging
from prometheus_client import Counter, generate_latest

app = Flask(__name__)
logging.basicConfig(filename='app.log', level=logging.INFO)

REQUEST_COUNT = Counter('flask_request_count', 'Total number of HTTP requests')

def connect_db():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="db"
    )

@app.route('/')
def hello():
    REQUEST_COUNT.inc()
    logging.info("Root endpoint was accessed")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT NOW()")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return f"Hello! Current time: {result[0]}"

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0')
