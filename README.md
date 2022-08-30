# PC2I - Platform
Repositório de código da plataforma e API para gerenciamento de irrigação promovido pelo projeto PC2I.

Siga os passos do arquivo [CONTRIBUTING.md](./CONTRIBUTING.md), caso queira contribuir com novas funcionalidades, melhorias e/ou correções no projeto.

## :open_file_folder: Conteúdo:
- [Pré-requisitos](#warning-pré-requisitos)
- [Rotas da API](#twisted_rightwards_arrows-rotas-da-api)
- [Guia de Instalação](#compass-guia-de-instalação)

## :warning: Pré-Requisitos
> Antes de começar, verifique se as seguintes ferramentas estão instaladas em sua máquina
- [Git](https://git-scm.com/downloads)
- [Python](https://python.org/downloads)

## :twisted_rightwards_arrows: Rotas da API
<<<<<<< HEAD
Todas as rotas da API estão documentadas no arquivo [ROUTES.md](./ROUTES.md).

## :compass: Guia de Instalação
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

=======
Todas as rotas da API foram documentadas utilizando o [Postman](https://postman.com).

Para acessar a documentação, [clique aqui](https://documenter.getpostman.com/view/21952024/UzQypiBw).

## :compass: Guia de Instalação
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

>>>>>>> e85246450d871000a2ae4bb0838dcf3bb183511b
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

### **8. Realizando solicitação à API**
Utilizando uma ferramenta como Postman ou Thunder Client, realize uma solicitação de teste à API. No exemplo abaixo, requisitamos que a API nos retorne a lista de zonas de irrigação cadastradas na banco:
```bash
GET http://localhost:5000/irrigation-zones
```
