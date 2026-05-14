# GameRoute: High-Performance Latency Monitor 🎮

A professional-grade asynchronous API and dashboard built with **FastAPI** to track real-time network performance for gaming infrastructure.

## 🚀 Overview
GameRoute is a network diagnostic tool that bridges the gap between low-level system operations and high-level web interfaces. It allows users to analyze server latency across multiple global regions or investigate any custom IP address with precision.

## ✨ Key Features
- **Asynchronous Execution:** High-speed network checks without blocking the main event loop.
- **Regex-Driven Parsing:** Advanced string parsing to extract clean numeric latency data from raw OS output.
- **RESTful v1 API:** Industry-standard API versioning (`/api/v1/`).
- **Interactive Dashboard:** Modern, dark-themed UI for immediate visual feedback.
- **Cross-Platform Compatibility:** Intelligent logic to handle both Windows and Linux network commands.

## 🛠️ Technology Stack
- **Backend:** Python 3.x, FastAPI, Uvicorn
- **Frontend:** Modern HTML5, CSS3 (Inter fonts), JavaScript (Fetch API)

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/BeytullahCaglayan/GameRoute-API.git](https://github.com/BeytullahCaglayan/GameRoute-API.git)

2. Setup Environment:
 python -m venv venv
 # Activate (Windows): .\venv\Scripts\activate

3. Install Dependencies:

 pip install -r requirements.txt


4. Run application 
 uvicorn main:app --reload
