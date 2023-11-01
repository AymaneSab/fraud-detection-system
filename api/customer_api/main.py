import sys
import time
from flask import Flask, jsonify

sys.path.append('/Users/sabri/Desktop/Study /Youcode/Github/Sprint_4/fraud-detection-system/api/') 

from generated_data import customers  

app = Flask(__name__)
socketio = SocketIO(app)

def json_entry():
    for customer in customers:
        yield jsonify(customer)
        time.sleep(2)

if __name__ == '__main__':
    app.run(debug=True, port=5002)


