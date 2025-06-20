#!/bin/bash

# Navega para o diretório do projeto
cd /home/ubuntu/madero_dashboard

# Ativa o ambiente virtual
source venv/bin/activate

# Inicia o servidor Flask em segundo plano, redirecionando a saída para um log
nohup python src/main.py > server.log 2>&1 &

echo "Dashboard iniciado! Acesse http://localhost:5000 no seu navegador."
echo "Para parar o dashboard, use o comando: pkill -f \"python src/main.py\""


