### English version
To access the English version click here: [**English version**](README_ENGLISH.md) 

# PC2I - Platform
Repositório de código da plataforma e API para gerenciamento de irrigação promovido pelo projeto PC2I.

#### :pushpin: Por enquanto, acessível apenas em _localhost_

---

## :warning: Pré-Requisitos
> Antes de começar, verifique se as seguintes ferramentas estão instaladas em sua máquina
- [Git](https://git-scm.com/downloads)
- [Python](https://python.org/downloads)

## :fire: Como contribuir
Para contribuir com código ou sugestões de melhorias/correções na plataforma do projeto PC2I, acesse o arquivo [CONTRIBUTING.md](./docs/CONTRIBUTING.md).

Caso possua alguma dúvida ou curiosidade sobre trabalho colaborativo com Git e GitHub, entre em contato com um dos membros do repositório.

## :compass: Guia de Instalação
> Com as ferramentas devidamente instaladas, execute os seguintes comandos no terminal (bash, powershell, cmd...)

### 1. Clone o repositório
```bash
git clone https://github.com/lead-ifal/pc2i-platform.git
```

### 2. Entre na pasta do projeto
```bash
cd pc2i-platform
```

### 3. Crie o ambiente virtual do Flask
```bash
# Linux e MacOS
python -m venv venv
```

```bash
# Windows
py -3 -m venv venv
```

### 4. Ative o ambiente virtual
```bash
# Linux e MacOS
. venv/bin/activate
```

```bash
# Windows
venv\Scripts\activate
```

### 5. Instale as dependências
```bash
# Linux, MacOS e Windows
pip install -r requirements.txt
```

### 6. Crie o arquivo de variáveis de ambiente
Acesse o arquivo [MONGO_CONFIG.md](./docs/MONGO_CONFIG.md) e obtenha a URL do banco de dados.

Com a URL do banco, crie uma cópia do arquivo [`.env.example`](./.env.example) com o nome de `.env`.

No arquivo `.env`, coloque a URL do banco depois de `MONGO_URI=(aqui)`.

### 7. Execute a aplicação
```bash
# Linux, MacOS e Windows
python __init__.py
```

No terminal, aparecerá algo assim:

```bash
* Serving Flask app 'app' (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: on
* Running on all addresses.
  WARNING: This is a development server. Do not use it in a production deployment.
* Running on http://192.168.1.110:1026/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 103-964-359
```

A plataforma estará executando na URL informada (por exemplo, `http://192.168.1.110:1026/`)

## :fire: Teste da plataforma/API
Acesse a rota `/api/docs` no navegador para ter acesso via [Swagger](https://swagger.io/tools/swagger-ui/) ou instale um cliente HTTP, como o [Postman](https://postman.com/downloads/), e obtenha as rotas da API acessando [esta documentação](https://documenter.getpostman.com/view/21952024/UzQypiBw).
