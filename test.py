import os
from pathlib import Path

PROJECT_STRUCTURE = {
    "GhostTrace": {
        "scrapers": {
            "__init__.py": None,
            "base_scraper.py": None,
            "proxy_scrapers.py": None,
            "validator.py": None,
            "pool_manager.py": None
        },
        "docker": {
            "Dockerfile": None,
            "docker-compose.yml": None,
            ".dockerignore": None
        },
        ".github": {
            "workflows": {
                "tests.yml": None,
                "lint.yml": None
            }
        }
    }
}

def create_structure(base_path, structure):
    for name, contents in structure.items():
        path = os.path.join(base_path, name)
        if contents is None:
            Path(path).touch()
            print(f"📄 {path}")
        else:
            os.makedirs(path, exist_ok=True)
            print(f"📁 {path}")
            create_structure(path, contents)

if __name__ == "__main__":
    base = os.path.join(os.getcwd(), "GhostTrace")
    print("\nAdding Proxy Scraper + Docker + CI/CD structure...\n")
    create_structure(base, PROJECT_STRUCTURE["GhostTrace"])
    print("\nDone. New modules ready.")