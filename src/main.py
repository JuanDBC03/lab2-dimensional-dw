import os
import sys
import subprocess

def install_requirements(script_dir):
    req_path = os.path.join(script_dir, "..", "requirements.txt")
    print("Checking and installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])
        print("Dependencies ready.\n")
    except Exception as e:
        print(f"Error installing requirements: {e}")
        sys.exit(1)

def run_pipeline():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 0. Install dependencies
    install_requirements(script_dir)

    # 1. Create schema
    print("1. Creating database schema...")
    subprocess.run([sys.executable, os.path.join(script_dir, "create_dw.py")])

    # 2. Load dimensions
    print("2. Loading dimensions...")
    subprocess.run([sys.executable, os.path.join(script_dir, "load_dimensions.py")])

    # 3. Load fact table
    print("3. Loading fact table...")
    subprocess.run([sys.executable, os.path.join(script_dir, "load_fact.py")])

    # 4. Generate visualizations
    print("4. Generating analytical visualizations...")
    subprocess.run([sys.executable, os.path.join(script_dir, "visualizations.py")])

    # 5. Launch query console
    print("\nPipeline completed successfully! Opening query console...\n")
    subprocess.run([sys.executable, os.path.join(script_dir, "queries.py")])

if __name__ == "__main__":
    run_pipeline()