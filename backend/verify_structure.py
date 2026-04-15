#!/usr/bin/env python3
"""
Vantrack Backend Verification Script
Validates that all files are created and structure is correct
"""

import os
import sys

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

REQUIRED_FILES = {
    'Root': [
        'app.py',
        'config.py',
        'database.py',
        'exceptions.py',
        'requirements.txt',
        '.env.example',
        'README.md'
    ],
    'domain': [
        'usuario.py',
        'validadores.py',
        '__init__.py'
    ],
    'infra': [
        'usuario_repository.py',
        'repository_interface.py',
        '__init__.py'
    ],
    'use_cases': [
        'cadastrar_usuario.py',
        'autenticar_usuario.py',
        'recuperar_senha.py',
        '__init__.py'
    ],
    'presentation': [
        'dtos.py',
        '__init__.py',
        'routes/__init__.py',
        'routes/auth_routes.py'
    ],
    'middleware': [
        'token_middleware.py',
        '__init__.py'
    ],
    'tests': [
        'test_validadores.py',
        '__init__.py'
    ]
}

def check_files():
    print("🔍 Vantrack Backend Structure Verification\n")
    
    all_good = True
    total_files = 0
    found_files = 0
    
    for directory, files in REQUIRED_FILES.items():
        dir_path = BACKEND_DIR if directory == 'Root' else os.path.join(BACKEND_DIR, directory)
        print(f"📁 {directory}/")
        
        for file in files:
            total_files += 1
            file_path = os.path.join(dir_path, file)
            exists = os.path.exists(file_path)
            
            if exists:
                found_files += 1
                status = "✅"
            else:
                status = "❌"
                all_good = False
            
            print(f"  {status} {file}")
        print()
    
    print("=" * 50)
    print(f"Summary: {found_files}/{total_files} files found")
    
    if all_good:
        print("✅ All backend files present!")
        return 0
    else:
        print("❌ Some files are missing!")
        return 1

if __name__ == '__main__':
    sys.exit(check_files())
