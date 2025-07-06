# 📈 ICICI Direct Breeze API Trading Suite  
*A Python-based toolkit for real-time market data streaming, historical analysis, and automated trading with ICICI Direct’s Breeze API.*  

---

## 🚀 Key Features  
✅ **Seamless Authentication** – OAuth2 login and session management  
✅ **Real-time Market Data** – WebSocket streaming for live ticks (NIFTY, Options, etc.)  
✅ **Historical Data Fetcher** – Download and consolidate minute-level options data  
✅ **Multi-threaded** – Non-blocking WebSocket streams with Flask integration  
✅ **Excel Automation** – Merge and process market data with Pandas  


## ⚙️ Setup  

### Prerequisites  
- ICICI Direct Breeze API credentials (Get from [ICICI API Portal](https://api.icicidirect.com))  
- Python 3.7+  

---

### Installation  
1. Clone the repo:  
   ```bash  
   git clone https://github.com/StArLorDd88/Stock-Analysis_ICICI.git
   ```  

2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Add your credentials to `.env`:  
   ```ini  
   API_KEY="your_api_key"  
   API_SECRET="your_api_secret"  
   FLASK_SECRET_KEY="a_random_secret_string"  
   ```  

---

## 🧑‍💻 Usage  

### 1️⃣ **Web App (Flask)**  
Start the server:  
```bash  
python app.py  
```  
**Endpoints**:  
- `/` → Redirects to ICICI login  
- `/callback` → Handles auth (automatically called by ICICI)  
- `/start_stream` → Starts real-time WebSocket streaming  
- `/stop_stream` → Stops streaming  

### 2️⃣ **Historical Data Pipeline**  
Fetch and merge options data:  
```bash  
python dataGenerator.py  
```  
*Modify dates in `dataGenerator.py` for custom ranges.*  

### 3️⃣ **Standalone WebSocket Stream**  
For direct streaming without Flask:  
```bash  
python webSocketStream.py  
```  

---

## 📂 Project Structure  
```  
├── app.py                # Flask server (auth + streaming control)  
├── webSocketStream.py    # WebSocket client for real-time data  
├── dataFetcher.py        # Fetch historical options data  
├── dataProcessor.py      # Merge Excel files with Pandas  
├── dataGenerator.py      # Data pipeline coordinator  
└── requirements.txt      # Dependencies  
```  

---

## 📊 Example Use Cases  
- **Algo Trading**: Feed real-time ticks to your strategy engine  
- **Backtesting**: Use historical data to validate trading models  
- **Research**: Analyze options volatility patterns  

---

## ⚠️ Notes  
🔹 **Rate Limits**: ICICI API has strict rate limits—space out historical requests.  
🔹 **WebSocket Stability**: Add reconnection logic for long-running streams.  
🔹 **Sensitive Data**: Never commit `.env` to version control!  

---

## 📜 License  
MIT © 2024 Himanshu__808  

--- 

### 🌟 Show Your Support  
Star ⭐ the repo if you find this useful!  

--- 