import sys
from pathlib import Path

# Adicionar o diretório raiz ao sys.path
sys.path.append(str(Path(__file__).parent))


from app.api import app

if __name__ == "__main__":
    app.run(debug=True)
