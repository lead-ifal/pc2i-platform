# PC2I - Platform
Repositório de código da plataforma e API para gerenciamento de irrigação promovido pelo projeto PC2I.

## :open_file_folder: Conteúdo:
- [Pré-requisitos](#⚠️-pré-requisitos)
- [Rotas da API](#🔀-rotas-da-api)
- [Guia de Instalação](#🧭-guia-de-instalação)

## ⚠️ Pré-Requisitos
> Antes de começar, verifique se as seguintes ferramentas estão instaladas em sua máquina
- [Git](https://git-scm.com/downloads)
- [Python](https://python.org/downloads)

## 🔀 Rotas da API
Todas as rotas da API estão documentadas no arquivo [ROUTES.md](./ROUTES.md).

## 🧭 Guia de Instalação
> Com as ferramentas devidamente instaladas, execute os seguintes comandos no terminal (bash, powershell, cmd...)

### **1. Clonar repositório**
```bash
git clone https://github.com/lead-ifal/pc2i-platform.git
```

### **2. Entrar na pasta do projeto**
```bash
cd pc2i-platform
```

### **3. Criar ambiente virtual do Flask**
```bash
# Linux e MacOS
python -m venv venv
```

```bash
# Windows
py -3 -m venv venv
```

### **4. Ativar ambiente virtual**
```bash
# Linux e MacOS
. venv/bin/activate
```

```bash
# Windows
venv\Scripts\activate
```

### **5. Instalar dependências**
```bash
# Linux, MacOS e Windows
pip install -r requirements.txt
```

### **6. Criar arquivo de variáveis de ambiente**
Você pode usar o arquivo [`.env-example`](./.env-example) como base, definindo a localização (URL) do _cluster_ do _MongoDB_.

Você pode encontrar no arquivo [MONGO_CONFIG.md](./MONGO_CONFIG.md) um guia de como criar e obter a URL do _cluster_.

### **7. Executar aplicação**
```bash
# Linux, MacOS e Windows
python __init__.py
```

A aplicação será executada em `http://localhost:5000`.
