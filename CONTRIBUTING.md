# Como contribuir com o projeto
> Siga os passos abaixo para contribuir com código ou sugestões de melhorias/correções na plataforma do projeto PC2I

## Pré-Requisitos
> Instale as ferramentas abaixo

- [Git](https://git-scm.com/downloads) - versionamento de código;
- [Python](https://python.org/downloads) - desenvolvimento da plataforma;
- Editor de código (ex.: [Visual Studio Code](https://code.visualstudio.com/Download));

---

## Execute a plataforma
Vá até o [guia de instalação](./README.md#compass-guia-de-instalação) e siga o passo a passo para ter a plataforma executando na sua máquina.

---

## Crie uma _branch_
O `nome-da-branch` deve descrever de forma clara e objetiva as alterações que você fará

```bash
git checkout -b nome-da-branch

# Exemplos:
# git checkout -b rota-listagem-usuarios
# git checkout -b corrigir-cadastro-zonas
# git checkout -b autenticacao-usuarios
```

---

## Altere o código
Agora você pode modificar os arquivos existentes no projeto ou até criar novos arquivos e pastas, caso seja necessário.

:warning: Tome cuidado para alterar apenas o que foi proposto na _branch_. Não faça grandes alterações, pois quanto maior a quantidade de alterações, mais dificíl será revisar seu código.

- Caso tenha adicionado uma nova importação execute no terminal os comandos:

```bash
pip pip install pipreqs
```
e
```bash
pipreqs --force
```
para atualizar o arquivo requirements.txt

---

## Registre as alterações
### 1. Adicione as alterações ao Git:

```bash
git add .
```

- Caso queira adicionar um arquivo específico, troque `.` pelo endereço do arquivo. Exemplo:

```bash
git add app/__init__.py
```

### 2. Registre as alterações

```bash
git commit -m "Mensagem"
```

- No lugar de `Mensagem`, descreva as alterações que você fez de forma clara e objetiva. Exemplo:

```bash
git commit -m "Adicao da rota de listagem de usuarios"
```

---

## Envie para análise
```bash
git push -u origin nome-da-branch
```

O `nome-da-branch` deve ser o mesmo que foi informado na [criação da _branch_](#crie-uma-branch).

---

## Abra um _Pull Request_ (PR)
### 1. Clique em "**Pull Requests**"

![imagem](https://user-images.githubusercontent.com/63798776/188283632-c4941df5-ca48-4964-8faa-98213f36fbf3.png)

### 2. Clique em "**New pull request**"

![imagem](https://user-images.githubusercontent.com/63798776/188283687-05181d74-87da-4f32-80a0-75d1a4a5ee4c.png)

### 3. Escolha as _branchs_
Garanta que a comparação de _branches_ esteja assim:

![imagem](https://user-images.githubusercontent.com/63798776/188282775-345e460a-fb70-4887-a8c1-6d9e5011ec63.png)

- Onde `sua-branch` é o nome que você definiu na [criação da _branch_](#crie-uma-branch).

### 4. Abra o PR
Clique em "**Create pull request**", descreva o que você fez, adicione um revisor e espere as revisões

---

## Faça as correções
Caso alguém peça correções no seu _pull request_, siga esse passo a passo:

### 1. Verifique se a _branch_ ativa é a mesma do PR
```bash
git branch

# Vai aparecer algo assim:
# * nome-da-branch
#   main

# A branch ativa é a que tem o asterisco
```

- Se a _branch_ for diferente, altere pra ela:
```bash
git checkout nome-da-branch
```

### 2. Faça as correções que foram pedidas no PR

### 3. Adicione ao versionamento
```bash
git add .
```

### 4. Registre as correções
```bash
git commit --amend --no-edit
```

### 5. Envie pro GitHub
```bash
git push origin nome-da-branch --force
```

- Caso resulte em erro, sincronize com o GitHub:

```bash
git pull origin nome-da-branch --rebase
```

### 7. Avise os revisores
Adicione um comentário abaixo da revisão que você corrigiu pra quem fez ser notificado e avaliar novamente

---

## Finalize a _branch_
> :warning: Só execute este passo quando o seu _pull request_ for **aprovado e adicionado à _branch_ principal** (_merge_) por uma pessoa autorizada (revisor).

1. Altere para a _branch_ principal

```bash
git checkout main
```

2. Sincronize com o GitHub

```bash
git pull origin main
```

3. Exclua a _branch_ que você estava trabalhando

```bash
git branch -d nome-da-branch
```

Caso queira trabalhar em outra funcionalidade/correção, [crie uma nova _branch_](#crie-uma-branch).

---

## :pencil: Sugerir melhorias ou correções
Caso você ainda não sinta segurança em contribuir com código ou encontrou um problema/situação de melhoria e quer reportar, crie uma _issue_.

Utilize [este guia](https://docs.github.com/pt/issues/tracking-your-work-with-issues/creating-an-issue) para reportar um problema ou indicar uma melhoria através de _issues_.

### :question: Surgiu alguma dúvida? Entre em contato com um dos membros do repositório
