# Configuração do Banco de Dados

## Crie uma conta
1. Acesse https://account.mongodb.com/account/login

2. Escolha o meio de autenticação e crie a conta (ou faça login, caso já tenha uma)

---

## Crie uma organização
> Se já tiver uma organização criada, pule este passo

1. Acesse https://cloud.mongodb.com/v2#/preferences/organizations

2. Clique em "**Create New Organization**"

![imagem](https://user-images.githubusercontent.com/63798776/188275387-9f80e7af-34f7-4984-9f2d-26d2665b81e7.png)

3. Informe o nome da organização e clique em "**Next**"

![imagem](https://user-images.githubusercontent.com/63798776/188275490-e11e424d-6fd5-47fc-a8f4-73706ec8ea08.png)

4. Clique em "**Create Organization**"

![imagem](https://user-images.githubusercontent.com/63798776/188275549-16236411-e936-4228-a11e-65285053257c.png)

---

## Crie um projeto
1. Clique em "**New Project**"

![imagem](https://user-images.githubusercontent.com/63798776/188275607-3d013048-c8c9-4009-bd8a-f07dbb736aad.png)

2. Informe o nome do projeto e clique em "**Next**"

![imagem](https://user-images.githubusercontent.com/63798776/188275903-01b84d0b-6ea2-4133-92b0-36b05fe9104e.png)

3. Clique em "**Create Project**"

![imagem](https://user-images.githubusercontent.com/63798776/188275952-94cab590-8c34-40a5-853f-2037cad2c292.png)

---

## Crie o banco de dados
1. Clique em "**Build a Database**"

![imagem](https://user-images.githubusercontent.com/63798776/188276061-ab428b17-fad2-41c7-bc3f-8c12a3ee0ef9.png)

2. Selecione o tipo de banco de dados (_Shared_, por ser gratuito).

![imagem](https://user-images.githubusercontent.com/63798776/171946060-a1c5b919-7ef4-44b7-b9e7-fdf51692867e.png)

3. Clique em **Create Cluster**.

4. Informe o nome e a senha do usuário do banco de dados e clique em "**Create User**"

![imagem](https://user-images.githubusercontent.com/63798776/188276205-d6b42c03-d34d-449c-9fc2-de66e2167110.png)

5. Adicione o endereço `0.0.0.0/0` e clique em "**Add Entry**"

![imagem](https://user-images.githubusercontent.com/63798776/188276321-05819081-48af-44a7-b22c-5d1f7b5e52ed.png)

6. Clique em "**Finish and Close**", depois em "**Go to Database**" (no _popup_ que aparecer)

7. Clique em **Connect**

![imagem](https://user-images.githubusercontent.com/63798776/171948956-e92e426d-6265-4987-89da-070cf5ecc43c.png)

8. Clique em **Connect your application**

![imagem](https://user-images.githubusercontent.com/63798776/188276469-a35b6ccb-b1a2-4d30-acdb-75066e3c2b16.png)

9. Selecione o _driver_ do Python e copie a URL que será gerada

![imagem](https://user-images.githubusercontent.com/63798776/171949064-4b8f1a82-0b3c-4eb7-92e8-2f8d7964542a.png)


```env
# Estrutura da URL:
mongodb+srv://USERNAME:PASSWORD@CLUSTER.HASH.mongodb.net/DATABASE?retryWrites=true&w=majority
```

> OBS.: CLUSTER e HASH são definidos pelo MongoDB, não altere!

10. Troque **USERNAME** e **PASSWORD** pelos dados que foram informados no ponto **4** da [criação do banco de dados](#crie-o-banco-de-dados).

11. Troque **DATABASE** pelo nome do banco de dados (ex.: **pc2i-db**)

```env
# Exemplo de URL válida:
mongodb+srv://nome-do-usuario:senha-forte@cluster0.rxjhpdm.mongodb.net/pc2i-db?retryWrites=true&w=majority
```

## Agora volte para a [configuração da plataforma](./README.md#6-crie-o-arquivo-de-variáveis-de-ambiente) e adicione a URL no arquivo `.env`
