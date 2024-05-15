from app import socketio, app

if __name__ == "__main__":
    socketio.run(app, debug=True, port=80, host="164.92.81.139")