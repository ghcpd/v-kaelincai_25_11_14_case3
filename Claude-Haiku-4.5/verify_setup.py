"""Initialize the project and verify all components are in place."""

import os
import json
from pathlib import Path

def verify_project_structure():
    """Verify that all required files are in place."""
    
    repo_root = Path(__file__).parent
    
    required_files = {
        "Project_A_BeforeUI": [
            "src/index.html",
            "src/style.css",
            "src/app.js",
            "src/server.py",
            "tests/test_pre_unit.py",
            "tests/test_pre_e2e.py",
            "tests/layout_validator.py",
            "requirements.txt",
            "setup.sh",
            "setup.bat",
            "run_tests.sh",
            "run_tests.bat",
        ],
        "Project_B_AfterUI": [
            "src/index.html",
            "src/style.css",
            "src/app.js",
            "src/server.py",
            "tests/test_post_unit.py",
            "tests/test_post_e2e.py",
            "tests/layout_validator.py",
            "requirements.txt",
            "setup.sh",
            "setup.bat",
            "run_tests.sh",
            "run_tests.bat",
        ],
        ".": [
            "test_data.json",
            "README.md",
            "generate_comparison_report.py",
            "run_all.sh",
            "run_all.bat",
        ]
    }
    
    print("Verifying project structure...")
    print()
    
    all_ok = True
    
    for folder, files in required_files.items():
        print(f"Checking {folder}...")
        if folder == ".":
            base_path = repo_root
        else:
            base_path = repo_root / folder
        
        for file in files:
            file_path = base_path / file
            if file_path.exists():
                print(f"  ✓ {file}")
            else:
                print(f"  ✗ {file} (MISSING)")
                all_ok = False
        
        print()
    
    # Verify test_data.json structure
    print("Verifying test_data.json structure...")
    test_data_path = repo_root / "test_data.json"
    if test_data_path.exists():
        with open(test_data_path, encoding='utf-8') as f:
            data = json.load(f)
        
        if "test_cases" in data and len(data["test_cases"]) >= 5:
            print(f"  ✓ Test cases: {len(data['test_cases'])}")
            for case in data["test_cases"]:
                print(f"    - {case['id']}: {case['name']}")
        else:
            print("  ✗ Missing or insufficient test cases")
            all_ok = False
    else:
        print("  ✗ test_data.json not found")
        all_ok = False
    
    print()
    print("=" * 50)
    if all_ok:
        print("✓ Project structure verified successfully!")
    else:
        print("✗ Some files are missing. Please run setup scripts.")
    print("=" * 50)
    print()
    
    return all_ok

def show_next_steps():
    """Display next steps for running the project."""
    
    print("Next Steps:")
    print()
    print("Option 1: Run everything (Recommended)")
    print("  Windows: run_all.bat")
    print("  Linux/Mac: bash run_all.sh")
    print()
    print("Option 2: Run individual projects")
    print("  Project A:")
    print("    Windows: cd Project_A_BeforeUI && setup.bat && run_tests.bat")
    print("    Linux/Mac: cd Project_A_BeforeUI && bash setup.sh && bash run_tests.sh")
    print()
    print("  Project B:")
    print("    Windows: cd Project_B_AfterUI && setup.bat && run_tests.bat")
    print("    Linux/Mac: cd Project_B_AfterUI && bash setup.sh && bash run_tests.sh")
    print()
    print("Option 3: Manual setup and testing")
    print("  1. Create virtual environment: python -m venv venv")
    print("  2. Activate: venv/Scripts/activate (Windows) or source venv/bin/activate")
    print("  3. Install: pip install -r requirements.txt")
    print("  4. Install browsers: playwright install chromium")
    print("  5. Run server: python src/server.py")
    print("  6. Run tests: python -m pytest tests/ -v")
    print()

if __name__ == "__main__":
    print()
    print("=" * 50)
    print("UI/UX Improvement Evaluation - Project Verification")
    print("=" * 50)
    print()
    
    ok = verify_project_structure()
    
    if ok:
        show_next_steps()
    else:
        print("Please ensure all files are in place before proceeding.")
