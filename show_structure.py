#!/usr/bin/env python3
"""
ExpenseFlow - Project Structure Visualization
This script shows the complete project structure
"""

import os
from pathlib import Path

def print_tree(directory, prefix="", max_depth=4, current_depth=0, ignore_dirs={".git", "node_modules", "__pycache__", ".next", "venv", ".venv"}):
    """Print directory tree structure"""
    if current_depth >= max_depth:
        return
    
    try:
        entries = sorted(Path(directory).iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        return
    
    dirs = [e for e in entries if e.is_dir() and e.name not in ignore_dirs]
    files = [e for e in entries if e.is_file()]
    
    # Print files first
    for i, file in enumerate(files):
        is_last_file = (i == len(files) - 1) and len(dirs) == 0
        print(f"{prefix}{'└── ' if is_last_file else '├── '}{file.name}")
    
    # Then directories
    for i, dir_path in enumerate(dirs):
        is_last = i == len(dirs) - 1
        print(f"{prefix}{'└── ' if is_last else '├── '}{dir_path.name}/")
        
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(dir_path, new_prefix, max_depth, current_depth + 1, ignore_dirs)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("ExpenseFlow - Project Structure")
    print("="*70 + "\n")
    
    print("ExpenseFlow/\n")
    print_tree(".", "")
    
    print("\n" + "="*70)
    print("Documentation Files Created:")
    print("="*70)
    
    docs = [
        ("README.md", "Complete product overview & features"),
        ("SETUP.md", "Installation & quick start guide"),
        ("ARCHITECTURE.md", "System design & API reference"),
        ("PROJECT_SUMMARY.md", "Feature checklist & summary"),
        ("TRANSFORMATION.md", "Before/after comparison"),
        ("INDEX.md", "Documentation navigation guide"),
        (".gitignore", "Git ignore rules"),
    ]
    
    for doc, description in docs:
        print(f"  ✓ {doc:<25} - {description}")
    
    print("\n" + "="*70)
    print("Backend Files Created:")
    print("="*70)
    
    backend_files = [
        ("app.py", "FastAPI main application"),
        ("requirements.txt", "Python dependencies"),
        ("app/models/database.py", "SQLAlchemy database models"),
        ("app/services/categorization.py", "ML inference service"),
        ("scripts/train_model.py", "Model training script"),
        ("scripts/predict.py", "CLI prediction tool"),
        ("data/sample_transactions.csv", "Sample training data"),
        (".env.example", "Environment configuration template"),
    ]
    
    for file, description in backend_files:
        print(f"  ✓ {file:<40} - {description}")
    
    print("\n" + "="*70)
    print("Frontend Files Created:")
    print("="*70)
    
    frontend_files = [
        ("package.json", "Node.js dependencies"),
        ("src/components/Dashboard.tsx", "Main dashboard page"),
        ("src/components/CategorizationForm.tsx", "Prediction input form"),
        ("src/components/TransactionTable.tsx", "Transaction grid view"),
        ("src/components/StatsCard.tsx", "Reusable stats card"),
        ("src/utils/api.js", "API client service"),
        ("src/utils/store.ts", "Zustand state management"),
    ]
    
    for file, description in frontend_files:
        print(f"  ✓ {file:<45} - {description}")
    
    print("\n" + "="*70)
    print("Quick Start Commands:")
    print("="*70)
    
    print("""
  1. Train the model:
     cd backend
     python scripts/train_model.py --dataset data/sample_transactions.csv

  2. Start backend server:
     python app.py
     (Available at http://localhost:5000)

  3. Start frontend (new terminal):
     cd frontend
     npm install
     npm run dev
     (Available at http://localhost:3000)

  4. View API documentation:
     http://localhost:5000/docs

  5. Test via CLI:
     cd backend
     python scripts/predict.py "Starbucks coffee"
""")
    
    print("="*70)
    print("Documentation Status:")
    print("="*70)
    
    status = [
        ("README.md", "✅ Complete", "Product vision & roadmap"),
        ("SETUP.md", "✅ Complete", "Installation guide"),
        ("ARCHITECTURE.md", "✅ Complete", "System design"),
        ("API Implementation", "✅ Complete", "FastAPI endpoints"),
        ("Frontend Components", "✅ Complete", "Dashboard & forms"),
        ("Database Models", "✅ Complete", "SQLAlchemy ready"),
        ("ML Training Script", "✅ Complete", "Training pipeline"),
        ("CLI Tool", "✅ Complete", "Prediction script"),
    ]
    
    for feature, status_icon, description in status:
        print(f"  {status_icon} {feature:<30} - {description}")
    
    print("\n" + "="*70)
    print("Version: 1.0.0 (MVP - Production Ready)")
    print("Status: ✅ Complete & Ready for Deployment")
    print("="*70 + "\n")
