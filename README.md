# AI-Assisted Resume Portfolio Generator

A Python application that reads resume content, sends it to the Gemini API, receives structured portfolio content in JSON, and generates a local HTML portfolio webpage.

## Quickstart Guide

Follow these steps to get the project running locally on your machine.

### 1. Clone the repository
```bash
git clone https://github.com/somyamaheshwari2612/aiportfoliogen.git
cd aiportfoliogen
```

### 2. Set up a Virtual Environment
It's highly recommended to use a virtual environment so dependencies don't conflict.
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
You need a Google Gemini API key for the AI to work.
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```
Open the `.env` file in your editor and replace `your_api_key_here` with your actual Gemini API key.

### 5. Run the Application
```bash
python app.py
```
Open your web browser and navigate to **http://127.0.0.1:5000** to use the generator!

---

*Note: For details on how the modules communicate, please see `INTERFACES.md`.*
