# PC2I API
> Todas as rotas de acesso à API

### Usuários
- [**`POST /users`**](#post-users) - Cadastro de usuário
- [**`POST /users/login`**](#post-userslogin) - Autenticação de usuário

### Zonas de Irrigação
- [**`POST /irrigation-zones`**](#post-irrigation-zones) - Cadastro de zona de irrigação
- [**`GET /irrigation-zones/user/{user-id}`**](#get-irrigation-zonesuseruser-id) - Listagem de zonas de irrigação por usuário

### Culturas
- [**`POST /cultures`**](#post-cultures) - Cadastro de culturas

---

## `POST` /users
> Cadastro de um novo usuário

### Requisição
```jsonc
{
  "name": "string",
  "email": "string",
  "password": "string"
}
```

### Exemplos de Resposta
```jsonc
// 201 CREATED

{
  "message": "Operação realizada com sucesso",
  "data": {
    "_id": "string",
    "email": "string",
    "name": "string",
    "date_added": "string"
  }
}
```

```jsonc
// 400 BAD REQUEST

{
  "message": "Não foi possível realizar a operação com os dados informados"
}
```

---

## `POST` /users/login
> Autenticação de um usuário existente

### Requisição
```jsonc
{
  "email": "string",
  "password": "string"
}
```

### Exemplos de Resposta
```jsonc
// 200 OK (SUCCESS)

{
  "message": "Operação realizada com sucesso",
  "data": {
    "_id": "string",
    "email": "string",
    "name": "string",
    "date_added": "string"
  }
}
```

```jsonc
// 400 BAD REQUEST

{
  "message": "Não foi possível realizar a operação com os dados informados"
}
```

---

## `POST` /irrigation-zones
> Cadastro de uma nova zona de irrigação por um usuário autenticado

### Requisição
```jsonc
{
  "user_id": "string",
  "name": "string",
  "description": "string",
  "size": "number"
}
```

### Exemplos de Resposta
```jsonc
// 201 CREATED

{
  "message": "Operação realizada com sucesso",
  "data": {
    "_id": "string",
    "user_id": "string",
    "name": "string",
    "description": "string",
    "size": "number"
  }
}
```

```jsonc
// 400 BAD REQUEST

{
  "message": "Não foi possível realizar a operação com os dados informados"
}
```

---

## `GET` /irrigation-zones/user/{user-id}
> Listagem de zonas de irrigação salvas por um determinado usuário

### Exemplos de Resposta
```jsonc
// 200 OK (SUCCESS)

{
  "message": "Operação realizada com sucesso",
  "data": [
    {
      "_id": "string",
      "user_id": "string",
      "name": "string",
      "description": "string",
      "size": "number"
    },
    {
      /* ... */
    }
  ]
}
```

```jsonc
// 400 BAD REQUEST

{
  "message": "Não foi possível realizar a operação com os dados informados"
}
```

---

## `POST` /cultures
> Cadastro de uma nova cultura

### Requisição
```jsonc
{
  "irrigation_zone_id": "string",
  "name": "string",
  "type": "string",
  "planting_date": "date",
  "harvest_date": "date", // opcional
  "phase": "string",
  "geographic_coordinates": "array[2]",
  "image": "file" // opcional
}
```

### Exemplos de Resposta
```jsonc
// 201 CREATED

{
  "message": "Operação realizada com sucesso",
  "data": {
    "_id": "string",
    "irrigation_zone_id": "string",
    "name": "string",
    "type": "string",
    "planting_date": "string",
    "harvest_date": "string", // opcional
    "phase": "string",
    "geographic_coordinates": "array[2]",
    "image": "string" // opcional
  }
}
```

```jsonc
// 400 BAD REQUEST

{
  "message": "Não foi possível realizar a operação com os dados informados"
}
```
