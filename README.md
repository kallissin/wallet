<h1 align='center'>
    Wallet - API
</h1>

<p>
Esta api tem por base gerenciar produtos que foram adquiridos pelos clientes de uma determinada empresa, e gerar cashback para as orders dos clientes.
</P>

O cashback é gerado da seguinte forma:

> Cada produto tem a sua categoria que é criado pelo admin do sistema, e a categoria por sua vez tem um campo _discount_ que é o percentual em decimal. Então é calculado o desconto do produto com base na quantidade de um determinado produto que o cliente adquiriu, então é somando todos os descontos e calculado o cashback.

<p>
A fim de evitar inconsistnências, como dados duplicados ou redundantes, apliquei a normalização de dados, montando relações mais estruturadas e performática, assim como melhorar a integridade da base de dados.
</p>

<h2>Indice:</h2>
<ol>
    <li>
        <a href='#user'>User:</a> 
        <ul>
            <li>
                Para um usuário conseguir utilizar a aplicação ele precisa estar logado. Temos 2 tipos de usuários (user/admin), o admin consegue utilizar todos os end points da API, com alguns diferenciais, ele é o unico que consegue:
                <ul>
                    <li>criar/atualizar/deletar uma categoria e definir o desconto para o mesmo.</li>
                    <li>visualizar/deletar usuários</li>
                </ul>
            </li>
            <li>
              <a href='#cadastrando-um-usuario'>Cadastrando um usuário</a>
            </li>
            <li>
              <a href='#login-de-usuario'>Login de usuário</a>
            </li>
            <li>
              <a href='#listando-todos-os-usuarios'>Listando todos os usuários</a>
            </li>
            <li>
              <a href='#listando-um-usuario-especifico'>Listando um usuário específico</a>
            </li>
            <li>
              <a href='#atualizando-um-usuario'>Atualizando um usuário</a>
            </li>
            <li>
              <a href='#deletando-um-usuario'>Deletando um usuário</a>
            </li>
              </ul>
          </li>
    <li>
        <a href='#customer'>Customer:</a>
        <ul>
            <li>
                É cadastrado no sistema por um usuário. O objetivo de ter um cliente é para associar as orders de compra a ele. Sendo assim, é possível visualizar todas as orders de um cliente específico
            </li>
            <li>
              <a href='#cadastrando-um-cliente'>Cadastrando um cliente</a>
            </li>
            <li>
              <a href='#listando-todos-os-clientes'>Listando todos os clientes</a>
            </li>
            <li>
              <a href='#listando-um-cliente-especifico'>Listando um cliente específico</a>
            </li>
            <li>
              <a href='#atualizando-um-cliente'>Atualizando um cliente</a>
            </li>
        </ul>
    </li>
    <li>
        <a href='#category'>Category:</a>
        <ul>
            <li>
                É utilizada para associar um produto a ela. Com base na categoria que é calculado o desconto do produto.
            </li>
        </ul>
    </li>
    <li>
        <a href='#produto'>Produto:</a>
        <ul>
            <li>
                O produto é cadastrado pelo usuário, foi criado uma tabela para o mesmo para evitar redundancia de produtos no banco de dados e melhor associar ao cliente que o adquiriu.
            </li>
        </ul>
    </li>
    <li>
        <a href='#itens'>Itens:</a>
        <ul>
            <li>
                Os itens fazem parte de uma order, neste item esta presente uma lista de itens contendo produtos, quantidade e valores.
            </li>
            <li>
                Achei melhor colocar a quantidade e valores associado a um item e não a um produto, tendo em vista que um produto pode alterar o seu valor constantemente, isso iria gerar mais trabalho para o usuário que atua em uma empresa de grande porte.
            </li>
        </ul>
    </li>
    <li>
        <a href='#cashback'>Cashback:</a>
        <ul>
            <li>
                O cashback é gerado para os clientes com base no disconto total adquirido em sua compra.
            </li>
        </ul>
    </li>
</ol>

<br>

## User:

### **Cadastrando um usuario**

---

<p>Rota responsável pelo cadastro do "usuário". Retorna um json com algumas informações do usuário</p>

| **url** | **method** |    **status**     |
| :-----: | :--------: | :---------------: |
| `/user` |   `POST`   | `201 - 400 - 409` |

**BODY**

```json
{
  "name": "kelvin cantarino",
  "email": "kelvin123@email.com",
  "username": "kelvinc",
  "password": "123456"
}
```

**RESPONSE**

```json
{
  "user_id": 1,
  "name": "kelvin cantarino",
  "email": "kelvin123@email.com",
  "username": "kelvinc",
  "role": "user"
}
```

### **Possíveis erros**

---

<p>
    Caso você tenha esquecido de passar algum campo, será retornado um erro com os campos que não foram enviados, exemplo:
</p>

```json
{
  "status": "error",
  "message": [
    "email is required",
    "username is required",
    "password is required"
  ]
}
```

<p>
    Caso você tenha enviado algum campo que não existe, será retornado um erro com os campos errados:
</p>

```json
{
  "status": "error",
  "message": ["key surname invalid"]
}
```

<p>
    Caso você tenha enviado algum valor no formato errado, será retornado um erro:
</p>

```json
{
  "status": "error",
  "message": ["key password must be type str"]
}
```

<p>
    Caso o username ja tenha sido cadastrado:
</p>

```json
{
  "message": "username already exists"
}
```

<p>
    Caso o email ja tenha sido cadastrado:
</p>

```json
{
  "message": "email already exists"
}
```

<br>

### **Login de usuario**

---

<p>Rota responsável pelo login do "usuário". Retorna um token de acesso, para que o usuário consiga utilizar os end points</p>

|    **url**    | **method** |       **status**        |
| :-----------: | :--------: | :---------------------: |
| `/user/login` |   `POST`   | `201 - 400 - 401 - 404` |

**BODY**

```json
{
  "username": "kelvinc",
  "password": "123456"
}
```

**RESPONSE**

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6MTY0MTE0Nzc5NS4wMzAwMTQsImlhdCI6MTY0MTE0NzY3NSwianRpIjoiOTliMDA3ZmItY2UyOC00NmU4LThmZWYtNzBlNTJkMGQ2NGM2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VyX2lkIjo0MiwibmFtZSI6IktlbHZpbiIsImVtYWlsIjoia2VsdmluMkBlbWFpbC5jb20iLCJ1c2VybmFtZSI6ImthbGxpc3NpbiIsInJvbGUiOiJhZG1pbiJ9LCJuYmYiOjE2NDExNDc2NzUsImV4cCI6MTY0MTE0ODU3NX0.HiyThkNcdxksX9MXDS9jovYhhFpRZQFxRiU7duT9NOs"
}
```

### **Possíveis erros**

---

<p>
    caso enviar o valor com o tipo diferente
</p>

```json
{
  "status": "error",
  "message": ["key password must be type str"]
}
```

<p>
    caso enviar um campo que não existe
</p>

```json
{
  "status": "error",
  "message": ["key teste invalid"]
}
```

<p>
   se enviar a senha errada 
<p>

```json
{
  "message": "password incorrect"
}
```

<p>
    se enviar o username que não existe no banco de dados
</p>

```json
{
  "message": "user not found"
}
```

<br>

### **Listando todos os usuarios**

---

<p>Rota responsável por listar todos os usuários cadastrados. Obs: precisa ser um usuário com role "admin" para fazer essa requisição</p>

> Authorization: Bearer {token}

| **url** | **method** | **status** |
| :-----: | :--------: | :--------: |
| `/user` |   `GET`    |   `200`    |

**RESPONSE**

```json
[
  {
    "user_id": 1,
    "name": "kelvin cantarino",
    "email": "kelvin123@email.com",
    "username": "kelvinc",
    "role": "user"
  },
  {
    "user_id": 2,
    "name": "maria",
    "email": "maria@email.com",
    "username": "maria",
    "role": "admin"
  }
]
```

<br>

### **Listando um usuario especifico**

---

<p>Rota responsável por listar um usuário específico. Obs: precisa ser um usuário com role "admin" para fazer essa requisição</p>

> Authorization: Bearer {token}

|     **url**     | **method** |    **status**     |
| :-------------: | :--------: | :---------------: |
| `/user/user_id` |   `GET`    | `200 - 403 - 404` |

**RESPONSE**

```json
{
  "user_id": 1,
  "name": "kelvin cantarino",
  "email": "kelvin123@email.com",
  "username": "kelvinc",
  "role": "user"
}
```

### **Possíveis erros**

---

<p>
    caso não encotre o usuário especificado
</p>

```json
{
  "message": "user not found"
}
```

<p>
    se não for um usuário admin
</p>

```json
{
  "msg": "Unauthorized for this user scope"
}
```

<br>

### **Atualizando um usuario**

---

<p>
    Nesta rota é possível atualizar os dados de um usuário, porem, só pode atualizar as informações se for admin ou se for o perfil do usuário que fez a requisição. Não é possível atualizar as informações de outros usuários.
</p>

> Authorization: Bearer {token}

|     **url**     | **method** |          **status**           |
| :-------------: | :--------: | :---------------------------: |
| `/user/user_id` |   `PTCH`   | `200 - 400 - 401 - 404 - 409` |

**RESPONSE**

```json
{
  "user_id": 1,
  "name": "kelvin cantarino",
  "email": "kelvin123@email.com",
  "username": "kelvinc",
  "role": "user"
}
```

### **Possíveis erros**

---

<p>
    caso tente alterar o campo "role" para admin
</p>

```json
{
  "message": "Unauthorized to update role"
}
```

<p>
    caso tente atualizar o email e este dado já pertencer a algum usuário
</p>

```json
{
  "message": "email already exists"
}
```

<p>
    caso tente atualizar o username e este dado já pertencer a algum usuário
</p>

```json
{
  "message": "username already exists"
}
```

<br>

### **Deletando um usuario**

---

<p>
    Esta rota é para deletar um usuário da aplicação. Obs: para deletar é necessário ser "admin". 
</p>

> Authorization: Bearer {token}

|     **url**     | **method** |    **status**     |
| :-------------: | :--------: | :---------------: |
| `/user/user_id` |  `DELETE`  | `204 - 403 - 404` |

**RESPONSE**

> No content

### **Possíveis erros**

---

<p>
  caso o usuário não seja um admin
</p>

```json
{
  "msg": "Unauthorized for this user scope"
}
```

<p>
  se o usuário não for encontrado
</p>

```json
{
  "message": "user not found"
}
```

<br>

## Customer

### **Cadastrando um cliente**

---

<p>
  Esta rota é responsável por cadastrar um cliente
</p>

> Authorization: Bearer {token}

|   **url**   | **method** |    **status**     |
| :---------: | :--------: | :---------------: |
| `/customer` |   `POST`   | `201 - 400 - 409` |

**BODY**

```json
{
  "name": "Flavio Reis",
  "cpf": "25579585063"
}
```

**RESPONSE**

```json
{
  "customer_id": 3,
  "cpf": "25579585063",
  "name": "flavio reis"
}
```

<br>

### **Possíveis erros**

---

<p>
  cpf precisa estar no formato xxxxxxxxxxx, se caso enviar o cpf em outro formato, receberá o seguinte erro
</p>

```json
{
  "message": "cpf must be in format xxxxxxxxxxx"
}
```

<p> 
  se adicionar um cpf que já esta sendo utilizado por outro usuário, receberá o seguinte erro
</p>

```json
{
  "message": "cpf already exists"
}
```

<p>
  se digitar um cpf que não é válido, exemplo: 11111111111. Receberá o seguinte erro
<p>

```json
{
  "message": "cpf is not valid"
}
```

<p>
  se digitar algum valor em outro formato, receberá o seguinte erro
<p>

```json
{
  "status": "error",
  "message": ["key cpf must be type str"]
}
```

<p>
  se caso não enviar os campos necessário para cadastrar um cliente voce receberá um erro, com o campo requerido
</p>

```json
{
  "status": "error",
  "message": ["cpf is required"]
}
```

<br>

### **Listando todos os clientes**

---

<p>
  Essa rota é responsável por listar todos os clientes que foram cadastrados
</p>

> Authorization: Bearer {token}

|   **url**   | **method** | **status** |
| :---------: | :--------: | :--------: |
| `/customer` |   `GET`    |   `200`    |

**RESPONSE**

```json
[
  {
    "customer_id": 1,
    "cpf": "70208421009",
    "name": "eduardo oliveira carrijo"
  },
  {
    "customer_id": 2,
    "cpf": "24041985051",
    "name": "silvana oliveira"
  },
  {
    "customer_id": 3,
    "cpf": "25579585063",
    "name": "flavio reis"
  }
]
```

<br>

### **Listando um cliente especifico**

---

<p>
  Essa rota é responsável por listar um cliente específico que foi cadastrado
</p>

> Authorization: Bearer {token}

|         **url**         | **method** |    **status**     |
| :---------------------: | :--------: | :---------------: |
| `/customer/customer_id` |   `GET`    | `200 - 403 - 404` |

**RESPONSE**

```json
{
  "customer_id": 3,
  "cpf": "25579585063",
  "name": "flavio reis"
}
```

### **Possíveis erros**

---

<p>
    caso não encotre o cliente especificado
</p>

```json
{
  "message": "customer not found"
}
```

<br>

### **Atualizando um cliente**

---

<p> 
  Essa rota é responsável por atualizar um cliente
</p>

> Authorization: Bearer {token}

|     **url**     | **method** |       **status**        |
| :-------------: | :--------: | :---------------------: |
| `/user/user_id` |   `PTCH`   | `200 - 400 - 404 - 409` |

**BODY**

```json
{
  "name": "flavio reis moreira",
  "cpf": "25579585063"
}
```

**RESPONSE**

```json
{
  "customer_id": 3,
  "cpf": "25579585063",
  "name": "flavio reis moreira"
}
```

### **Possíveis erros**

---

<p>
  cpf precisa estar no formato xxxxxxxxxxx, se caso enviar o cpf em outro formato, receberá o seguinte erro
</p>

```json
{
  "message": "cpf must be in format xxxxxxxxxxx"
}
```

<p> 
  se adicionar um cpf que já esta sendo utilizado por outro usuário, receberá o seguinte erro
</p>

```json
{
  "message": "cpf already exists"
}
```

<p>
  se digitar um cpf que não é válido, exemplo: 11111111111. Receberá o seguinte erro
<p>

```json
{
  "message": "cpf is not valid"
}
```

<p>
  se digitar algum valor em outro formato, receberá o seguinte erro
<p>

```json
{
  "status": "error",
  "message": ["key cpf must be type str"]
}
```
