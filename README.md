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
        </ul>
    </li>
    <li>
        <a href='#customer'>Customer:</a>
        <ul>
            <li>
                É cadastrado no sistema por um usuário. O objetivo de ter um cliente é para associar as orders de compra a ele. Sendo assim, é possível visualizar todas as orders de um cliente específico
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

## User:

### **Cadastrando um Usuário**

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

### **Login de Usuário**

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

<br>

### Listando todos os usuários

<p>Rota responsável por listar todos os usuários cadastrados</p>

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
