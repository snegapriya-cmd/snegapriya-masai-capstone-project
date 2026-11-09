"""Run the complete synthetic project from data generation to outputs."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
subprocess.run([sys.executable, str(ROOT / "generate_data.py")], check=True)
subprocess.run([sys.executable, "-c",
                "from src.pipeline import run_all; run_all()"], cwd=ROOT, check=True)
print("Project completed successfully.")
