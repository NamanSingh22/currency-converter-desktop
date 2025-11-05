#  Currency Converter Desktop Application

A Python desktop application built using **Tkinter** that allows users to convert between world currencies in real time using the **ExchangeRate API**.

## Features
- Live currency conversion using ExchangeRate API  
- Caching of daily rates using SQLite  
- Persistent history of past conversions  
- CSV export support  
- Simple and user-friendly Tkinter interface  


## ️Technologies Used
- Python 3.12  
- Tkinter  
- SQLite  
- Requests & dotenv  

## How to Run
```bash
pip install -r requirements.txt
Create a .env file with: API_KEY=your_api_key_here
python main.py
```
## using pyinstaller
```bash
pyinstaller --onefile --noconsole --icon=images/logo.ico main.py

Created as part of college Project