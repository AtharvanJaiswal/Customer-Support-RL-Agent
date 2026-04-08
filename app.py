from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def run_agent():
    result = subprocess.run(
        ["python", "inference.py"],
        capture_output=True,
        text=True
    )
    return {"output": result.stdout}