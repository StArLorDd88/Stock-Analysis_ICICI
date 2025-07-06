from flask import Flask, request, jsonify, redirect, session
from breeze_connect import BreezeConnect
import urllib.parse
from dotenv import load_dotenv
import os
from webSocketStream import BreezeStreamer
import threading

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Initialize Breeze connection
breeze = BreezeConnect(api_key=os.getenv("API_KEY"))
streamer = None

@app.route('/')
def login():
    login_url = f"https://api.icicidirect.com/apiuser/login?api_key={urllib.parse.quote_plus(os.getenv('API_KEY'))}"
    return redirect(login_url)

@app.route('/callback', methods=['POST'])
def callback():
    global streamer
    session_token = request.args.get("apisession")
    
    if not session_token:
        return "Authorization failed", 400

    try:
        breeze.generate_session(
            api_secret=os.getenv("API_SECRET"),
            session_token=session_token
        )
        session["access_token"] = session_token
        
        # Initialize streamer with session token
        os.environ["ACCESS_TOKEN"] = session_token
        streamer = BreezeStreamer()
        
        customer_details = breeze.get_customer_details(api_session=session_token)
        return jsonify({
            "message": "Session active", 
            "customer_details": customer_details
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/start_stream')
def start_stream():
    if not streamer:
        return jsonify({"error": "Streamer not initialized"}), 400
    
    threading.Thread(target=streamer.connect).start()
    return jsonify({"message": "Streaming started"})

@app.route('/stop_stream')
def stop_stream():
    if not streamer:
        return jsonify({"error": "Streamer not initialized"}), 400
    
    streamer.disconnect()
    return jsonify({"message": "Streaming stopped"})

def run_flask():
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    run_flask()