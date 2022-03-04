# PC2I - Platform
Repositório de código da plataforma e API para gerenciamento de irrigação promovido pelo projeto PC2I.

## Pré-Requisitos
> Antes de começar, verifique se as seguintes ferramentas estão instaladas em sua máquina
- [Git](https://git-scm.com/downloads)
- [Python 3](https://python.org/downloads)

## Guia de Instalação
> Com as ferramentas devidamente instaladas, execute os seguintes comandos no terminal (bash, powershell, cmd...)

### 1. Clonar repositório
```
git clone https://github.com/lead-ifal/pc2i-platform.git
```

### 2. Entrar na pasta do projeto
```
cd pc2i-platform
```

### 3. Criar ambiente virtual do Flask
- Linux/MacOS:
```
python -m venv venv
```

- Windows:
```
py -3 -m venv venv
```

### 4. Ativar ambiente virtual
- Linux/MacOS:
```
. venv/bin/activate
```

- Windows:
```
venv\Scripts\activate
```

### 5. Instalar dependências
- Linux/MacOS e Windows:
```
pip install -r requirements.txt
```

### 6. Criar arquivo de variáveis de ambiente
Você pode usar o arquivo [`.env-example`](./.env-example) como base, definindo a localização (URL) do _cluster_ do _MongoDB_.

### 7. Executar aplicação
- Linux/MacOS e Windows:
```
python __init__.py
```
