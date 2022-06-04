# Como contribuir com o projeto
> Siga os passos abaixo para contribuir com código ou sugestões de melhorias/correções na plataforma do projeto PC2I

## :open_file_folder: Conteúdo:
- [Pré-Requisitos](#1-pré-requisitos)
- [Instalação](#2-siga-os-passos-do-guia-de-instalação)
- [Sincronização](#3-antes-de-tudo-sincronize-com-o-repositório-remoto)
- [Criar uma _branch_](#4-crie-uma-branch)
- [Realizar as alterações](#5-realize-as-alterações-necessárias)
- [Registrar as alterações](#6-registre-as-alterações-realizadas)
- [Submeter contribuição](#7-enviar-as-modificações-para-análise)
- [Solicitar avaliação](#8-abra-um-pull-request-pr-para-os-mais-íntimos)
- :pencil: [Sugerir melhorias ou correções](#pencil-sugerir-melhorias-ou-correções)

---

## 1. Pré-Requisitos
- [Git](https://git-scm.com/downloads) - versionamento de código;  
- [Python](https://python.org/downloads) - desenvolvimento da plataforma;
- Editor de código (ex.: [Visual Studio Code](https://code.visualstudio.com/Download));

## 2. Siga os passos do [Guia de Instalação](./README.md#🧭-guia-de-instalação)
Com isso, você terá tudo o que é necessário para executar a aplicação.

Após seguir todos os passos do guia, execute as seguintes instruções:

## 3. Antes de tudo, sincronize com o repositório remoto
Para evitar conflitos com o código principal que está no repositório remoto (`github.com/lead-ifal/pc2i-platform`), **SEMPRE** execute o comando abaixo antes de realizar qualquer modificação:

```bash
git pull origin main
```

Assim, você evitará muitos problemas e todo mundo fica feliz ;)

## 4. Crie uma _branch_
> Não sabe o que é uma _branch_? Não tem problema, [clique aqui](https://git-scm.com/book/pt-br/v2/Branches-no-Git-Branches-em-poucas-palavras) para entender o seu significado e utilização.

```bash
git checkout -b <branch>
# Troque <branch> pelo nome da funcionalidade ou correção que você implementará (ex.: feature/login-route)
```

## 5. Realize as alterações necessárias
Agora você pode modificar os arquivos existentes no projeto ou até criar novos arquivos e pastas, caso seja necessário.

## 6. Registre as alterações realizadas
Após realizar as alterações necessárias, adicione-as ao Git com os seguintes comandos:

```bash
git add .
# Caso queira adicionar um arquivo específico, troque "." pelo endereço do arquivo (ex.: git add app/__init__.py)
```

```bash
git commit -m "Mensagem"
# No lugar de Mensagem, descreva as alterações que você fez, preferencialmente em inglês, de forma breve
```

## 7. Enviar as modificações para análise
Após fazer e registrar as alterações, é necessário enviá-las para o repositório remoto. Assim, todos poderão ver a sua contribuição.

Para enviar suas modificações, execute o seguinte comando:

```bash
git push origin <branch>
# Troque <branch> pelo nome da branch que você criou no passo 4 deste guia
```

## 8. Abra um _Pull Request_ (PR para os mais íntimos)
> Não sabe o que é um _Pull Request_? [Clique aqui](https://docs.github.com/pt/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) para entender o seu propósito.

Você pode seguir [este guia](https://docs.github.com/pt/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) para criar um _pull request_.

Após a criação do PR, espere alguém analisar o seu código e indicar o que deve ser feito.

Caso seja exigida alguma alteração, você pode realizar as correções, seguindo do [passo 5](#5-realize-as-alterações-necessárias) deste guia em diante.

## :pencil: Sugerir melhorias ou correções
Caso você ainda não sinta segurança em contribuir com código ou encontrou um problema/situação de melhoria e quer reportar, crie uma _issue_.

Utilize [este guia](https://docs.github.com/pt/issues/tracking-your-work-with-issues/creating-an-issue) para reportar um problema ou indicar uma melhoria através de _issues_.

---

Surgiu alguma dúvida? Entre em contato com um dos membros do repositório ;)
