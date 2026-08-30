"""
IP-SAKTI Sahayak Main Entrypoint
Usage:
    python main.py             # Launches interactive CLI
    python run_server.py       # Launches Web Dashboard and REST API
"""

import sys
from ip_sakti.cli import run_cli

if __name__ == "__main__":
    run_cli()
