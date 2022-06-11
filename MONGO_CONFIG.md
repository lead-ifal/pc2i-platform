# Configuração do MongoDB Atlas

1. Crie uma conta no [MongoDB Atlas](https://account.mongodb.com/account/login).

2. Selecione o tipo de banco de dados (_Shared_, por ser gratuito).

![imagem](https://user-images.githubusercontent.com/63798776/171946060-a1c5b919-7ef4-44b7-b9e7-fdf51692867e.png)

3. Clique em **Create Cluster**.

4. Crie um usuário, informando o _Username_ e _Password_, clique em **Create User** e depois em **Add My Current IP Address**. Por último, clique em **Finish and Close**.

5. Para obter a URL do _Cluster_, clique em **Connect**.

![imagem](https://user-images.githubusercontent.com/63798776/171948956-e92e426d-6265-4987-89da-070cf5ecc43c.png)

6. Selecione a opção **Connect your application**.

7. Selecione o _driver_ do Python e copie a URL que será gerada.

![imagem](https://user-images.githubusercontent.com/63798776/171949064-4b8f1a82-0b3c-4eb7-92e8-2f8d7964542a.png)

```env
# Estrutura final da URL:
mongodb+srv://<username>:<password>@<cluster>.<hash>.mongodb.net/<database>?retryWrites=true&w=majority

# OBS.: "<username>", "<cluster>" e "<hash>" serão gerados pelo próprio MongoDB.
# Adicione o nome do banco de dados no lugar de "<database>".
```

8. Você vai trocar _username_ e _password_ pelos dados que foram informados no ponto **4** desse guia.

9. Pronto! Agora é só usar a URL na aplicação ;)
