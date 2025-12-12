# Como Executar o Gerenciador de Ativos

## Pré-requisitos

Você precisa ter Flask instalado. Execute um dos comandos abaixo:

**Opção 1 (Recomendado):**

```bash
sudo apt install python3-flask python3-flask-cors
```

**Opção 2 (Alternativa):**

```bash
pip3 install --break-system-packages flask flask-cors
```

## Iniciar o Aplicativo

Após instalar as dependências, execute:

```bash
cd /home/rudi/Desktop/gerenciador-de-ativos-
./run.sh
```

Ou diretamente:

```bash
python3 server.py
```

O servidor iniciará em **<http://localhost:5000>**

## Como Funciona

- Os dados são salvos automaticamente no arquivo `data.json`
- Não usa mais o localStorage do navegador
- Todos os ativos, transações e configurações ficam salvos no disco
- Você pode fechar o navegador e os dados permanecerão salvos
