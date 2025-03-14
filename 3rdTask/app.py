from flask import Flask, request, jsonify
import psycopg2

from taganrog_modified import parse


DB_CONFIG = {"dbname": "CompNet", "user": "postgres", "password": "doomer2002", "host": "localhost", "port": 5432}

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/parse', methods = ['GET'])
def handle_parse():
    url = request.args.get('url')
    num_pages = request.args.get('pages', default = 1, type = int)

    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    if num_pages == 0:
        return jsonify({"Error": "Number of pages should be greater than 0"}), 400
    
    try:
        parsed_data = parse(url, num_pages)

        conn = get_db_connection()
        cursor = conn.cursor()
        for item in parsed_data:
            cursor.execute("INSERT INTO parsed_data_2 (url, title, description, date, comments) VALUES (%s, %s, %s, %s, %s)", (url, item['title'], item['description'], item['date'], item['comments']))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "parsed and saved", "data": parsed_data}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, url, title, description, date, comments FROM parsed_data")
        rows = cursor.fetchall()
        result = [
            {"id": row[0], "url": row[1], "title": row[2], "description": row[3], "date": row[4], "comments": row[5]}
            for row in rows
        ]
        cursor.close()
        conn.close()

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug = True)


    #http://127.0.0.1:5000/parse?url=https://bloknot-taganrog.ru/&pages=2
    #http://127.0.0.1:5000/get_data