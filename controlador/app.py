# server.py
from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
servers_data = {}   

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    servers_data[data['name']] = data
    # Envia os dados atualizados
    socketio.emit('update_data', servers_data)
    return {"status": "ok"}

if __name__ == '__main__':
     
    socketio.run(app, host='0.0.0.0', port=5001, debug=True, use_reloader=True)



