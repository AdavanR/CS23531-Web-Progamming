"""
PromptGuard Launcher Script.
Run the Web UI, FastAPI REST server, or CLI Benchmark.

Usage:
    python run.py               # Launch Streamlit Web Dashboard
    python run.py --api         # Launch FastAPI REST Server
    python run.py --benchmark   # Run CLI Red-Team Benchmark
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

def run_ui(port=8501):
    print(f"\n=======================================================")
    print(f"🛡️  PromptGuard — Prompt Injection Testing Sandbox")
    print(f"=======================================================")
    print(f"Launching Streamlit Dashboard at http://localhost:{port}")
    print(f"Press Ctrl+C to stop.\n")
    app_path = PROJECT_ROOT / "promptguard" / "ui" / "app.py"
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port",
        str(port),
        "--server.headless",
        "false",
        "--theme.base",
        "dark",
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    subprocess.run(cmd, env=env)

def run_api(host="127.0.0.1", port=8000):
    print(f"\n=======================================================")
    print(f"🛡️  PromptGuard REST API Server")
    print(f"=======================================================")
    print(f"API Docs available at http://{host}:{port}/docs")
    print(f"Press Ctrl+C to stop.\n")
    import uvicorn
    from promptguard.api.server import app
    uvicorn.run(app, host=host, port=port)

def run_cli_benchmark():
    from promptguard.benchmark.runner import BenchmarkRunner
    from promptguard.library.scenarios import TARGET_SCENARIOS

    runner = BenchmarkRunner()
    scen = TARGET_SCENARIOS[0]
    print(f"\n=======================================================")
    print(f"🛡️  PromptGuard Automated Red-Team Matrix")
    print(f"Target Scenario: {scen.name}")
    print(f"=======================================================\n")
    summary = runner.run_benchmark(scenario=scen)

    print("=== SUMMARY METRICS ===")
    print(f"Total Attack Tests: {summary.total_tests}")
    print(f"Attack Success Rate (ASR): {summary.attack_success_rate}%")
    print(f"Defense Block Rate (DBR): {summary.defense_block_rate}%")
    print(f"False Positive Rate (FPR): {summary.false_positive_rate}%")
    print(f"Average Evaluation Latency: {summary.average_latency_ms} ms\n")

    print("=== PRESET PERFORMANCE ===")
    for preset_name, data in summary.results_by_preset.items():
        print(f"  • {preset_name:35} | ASR: {data['attack_success_rate']:5}% | Blocked: {data['defense_block_rate']:5}% | Latency: {data['avg_latency_ms']} ms")
    print("\nBenchmark completed successfully.")

def main():
    parser = argparse.ArgumentParser(description="PromptGuard Launcher")
    parser.add_argument("--api", action="store_true", help="Launch FastAPI REST server instead of UI")
    parser.add_argument("--benchmark", action="store_true", help="Run automated CLI benchmark and exit")
    parser.add_argument("--port", type=int, default=None, help="Port to run the service on")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host interface to bind to")

    args = parser.parse_args()

    if args.benchmark:
        run_cli_benchmark()
    elif args.api:
        port = args.port or 8000
        run_api(host=args.host, port=port)
    else:
        port = args.port or 8501
        run_ui(port=port)

if __name__ == "__main__":
    main()
