import uvicorn
from infra.api.server import app

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except KeyboardInterrupt:
        print("Servidor encerrado.")
