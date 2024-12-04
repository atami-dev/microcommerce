@echo off

:: Start each service in a new Command Prompt window
start cmd /k "cd gateway && uvicorn main:app --reload --host 127.0.0.1 --port 8000"
start cmd /k "cd user_service && uvicorn main:app --reload --host 127.0.0.1 --port 8001"
start cmd /k "cd product_service && uvicorn main:app --reload --host 127.0.0.1 --port 8002"
start cmd /k "cd order_service && uvicorn main:app --reload --host 127.0.0.1 --port 8003"
start cmd /k "cd payment_service && uvicorn main:app --reload --host 127.0.0.1 --port 8004"

pause
