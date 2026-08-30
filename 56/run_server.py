"""
Entry point -- matches the run_server.py convention used in the 789 folder.

Usage:
    python run_server.py

Set PORT env var to change the port (default 5050, chosen to avoid
colliding with the Node backend on 5000 and the Task 2/3 engine on 5000
locally if both are run side by side during development).
"""

import os
from main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f"IP-SAKTI Jurisdiction & Citation Layer (Points 5 & 6) running on port {port}")
    print(f"Health check: http://127.0.0.1:{port}/api/health")
    app.run(debug=False, port=port)
