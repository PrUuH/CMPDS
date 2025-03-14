from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/test', methods = ['GET'])
def test():
    return jsonify({"message": "API is working blyatt"})

if __name__ == '__main__':
    app.run(debug = True)
    