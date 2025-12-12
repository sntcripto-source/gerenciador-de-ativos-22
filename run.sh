#!/bin/bash
# Script to run Asset Manager with local file storage (Zero Dependency)

echo "======================================"
echo "Asset Manager - Starting Server"
echo "======================================"

# Start the Simple Python server
echo "Iniciando servidor local (não requer instalação de bibliotecas)..."
echo "Acesse: http://localhost:8000"
echo "Dados serão salvos na pasta: ./SAVE/"
echo ""
echo "Pressione Ctrl+C para parar"
echo "======================================"
echo ""

python3 simple_server.py
