"""
Server Runner for IP-SAKTI Sahayak
Launches FastAPI backend and Web Dashboard on http://localhost:8000
"""

import uvicorn
import os

if __name__ == "__main__":
    print("=================================================================")
    print("🌿 IP-SAKTI Sahayak Web Server & API")
    print("   House of Cards Multi-Agent Framework (Layers 7, 8, and 9)")
    print("   Serving at: http://localhost:8000")
    print("=================================================================")
    uvicorn.run("ip_sakti.api:app", host="127.0.0.1", port=8000, reload=True)
