@echo off
title NOTIFICACOES TELEGRAM
CD C:\caminho\do\projeto\notificacoes-telegram
CALL venv\Scripts\activate.bat
python main.py
timeout 2