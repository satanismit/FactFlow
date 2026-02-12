import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from app.orchestration.graph import run_factflow

def main():
    query = "what is the outline of this course DESIGN PATTERNS & FRAMEWORKS?"
    result = run_factflow(query)

if __name__ == "__main__":
    main()
