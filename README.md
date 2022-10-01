<h1 align='center'>
    Wallet - API
</h1>


Esta api tem por base gerenciar produtos que foram adquiridos pelos clientes de uma determinada empresa, e gerar cashback para os pedidos dos clientes.


O cashback é gerado da seguinte forma:

> Cada produto tem a sua categoria que é criado pelo admin do sistema, e a categoria por sua vez tem um campo _discount_ que é o percentual em decimal. Então é calculado o desconto do produto com base na quantidade de um determinado produto que o cliente adquiriu, então é somando todos os descontos e calculado o cashback.


A fim de evitar inconsistnências, como dados duplicados ou redundantes, apliquei a normalização de dados, montando relações mais estruturadas e performática, assim como melhorar a integridade da base de dados.


## Instruções:

1 - Adicione as variáveis de ambiente em seu arquivo **.env** conforme o arquivo **.env.example**

2 - Buildar o projeto

```bash
make build
```

3 - Criar um ambiente virtual
```bash
python -m venv venv
```

4 - Ativando o ambiente

```bash
source venv/bin/activate
```

5 - Instalando as libs

```bash
pip install -r requirements.txt
```

6 - Gerando as tabelas no banco de dados

```bash
make run-revisions
```

7 - Rodando os Tests

```bash
make bash
```

```bash
pytest -s
```

8 - Rodando a aplicação

```bash
make run
```
Para criar um usuário admin **local**

`flask admin create name email username password`

**Exemplo:**

`flask admin create kelvin kelvin@email.com kelvin42 123456`


## Aplicação no Heroku

[Link](https://wallet-backend-flask.herokuapp.com/api)


baixe a collection no seu insomnia para utilizar os endpoints

[![Run in Insomnia}](https://insomnia.rest/images/run.svg)](https://insomnia.rest/run/?label=wallet&uri=https%3A%2F%2Fraw.githubusercontent.com%2Fkallissin%2Finsomnia-wallet%2Fmaster%2Fexport.json%3Ftoken%3DGHSAT0AAAAAABPDN7HAYOAV7ZHSSWOQ3LFWYO4GMQQ)

Para criar um usuário admin **heroku**

`heroku run --app wallet-backend-flask flask admin create name email username password`

**Exemplo:**

`heroku run --app wallet-backend-flask flask admin create kelvin kelvin@email.com kelvin123 123456`

## Indice:
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
            <li>
              <a href='#criando-um-produto'>Criando um produto</a>
            </li>
            <li>
              <a href='#listando-todos-os-produtos'>Listando todos os produtos</a>
            </li>
            <li>
              <a href='#listando-um-produto-especifico'>Listando um produto específico</a>
            </li>
            <li>
              <a href='#atualizando-um-produto'>Atualizando um produto</a>
            </li>
            <li>
              <a href='#deletando-um-produto'>Deletando um produto</a>
            </li>
        </ul>
    </li>
    <li>
      <a href='#order'>Order:</a>
      <ul>
        <li>
          Representa uma solicitação de compra do cliente, ou seja, o cliente pode ter várias solicitações contendo vários itens que é representado por produtos, quantidade e valores. Dessa forma fica mais fácil identificar o que o cliente comprou e visualizar o cashback gerado para aquela solicitação.
        </li>
        <li>
          <a href='#criando-um-pedido'>Criando um pedido</a>
        </li>
        <li>
          <a href='#listando-todos-os-pedidos'>Listando todos os pedidos</a>
        </li>
        <li>
          <a href='#listando-um-pedido-especifico'>Listando um pedido específico</a>
        </li>
        <li>
          <a href='#deletando-um-pedido'>Deletando um pedido</a>
        </li>
      </ul>
    </li>
    <li>
        <a href='#item'>Item:</a>
        <ul>
            <li>
                Os itens fazem parte de uma order, neste item esta presente uma lista de itens contendo produtos, quantidade e valores.
            </li>
            <li>
                Achei melhor colocar a quantidade e valores associado a um item e não a um produto, tendo em vista que um produto pode alterar o seu valor constantemente, isso iria gerar mais trabalho para o usuário que atua em uma empresa de grande porte.
            </li>
            <li>
              <a href='#adicionando-item-a-um-pedido'>Adicionando item a um pedido</a>
            </li>
            <li>
              <a href='#listando-todos-os-itens'>Listando todos os itens</a>
            </li>
            <li>
              <a href='#listando-um-item-especifico'>Listando um item especifico</a>
            </li>
            <li>
              <a href='#listando-todos-os-itens-de-um-pedido'>Listando todos os itens de um pedido</a>
            </li>
            <li>
              <a href='#atualizando-um-item'>Atualizando um item</a>
            </li>
            <li>
              <a href='#deletando-um-item'>Deletando um item</a>
            </li>
        </ul>
    </li>
    <li>
        <a href='#cashback'>Cashback:</a>
        <ul>
            <li>
                O cashback é gerado para os clientes com base no disconto total adquirido em sua compra.
            </li>
             <li>
              <a href='#gerando-um-cashback'>Gerando um cashback</a>
            </li>
            <li>
              <a href='#listando-um-cashback-especifico'>Listando um cashback específico</a>
            </li>
        </ul>
    </li>
</ol>

<br>

## **USER**:

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

## **CUSTOMER**

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
  se o cpf não tiver 11 digitos, receberá uma mensagem de erro
</p>

```json
{
  "message": "cpf must be 11 digits"
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

<br>

## **CATEGORY**:

### **Criando uma categoria**

---

<p>
  Rota responsável por criar uma categoria, o valor do campo discount tem que ser em decimal para representar o disconto. Exemplo: 5% seria 5 / 100 o que resultaria em 0,05, logo o valor de discount seria 0.05 . Obs: Somente usuário "admin" consegue criar uma categoria.
</p>

> Authorization: Bearer {token}

|   **url**   | **method** |       **status**        |
| :---------: | :--------: | :---------------------: |
| `/category` |   `POST`   | `201 - 400 - 403 - 409` |

**BODY**

```json
{
  "name": "alimentos",
  "discount": 0.05
}
```

**RESPONSE**

```json
{
  "category_id": 2,
  "name": "alimentos",
  "discount": 0.05
}
```

### **Possíveis erros**

---

<p>
  Se caso digitar um valor do tipo inteiro no campo discount, voce receberá o seguinte erro informando que o valor precisa ser do tipo flutuante
</p>

```json
{
  "status": "error",
  "message": ["key discount must be type float"]
}
```

<p>
  Se caso esquecer de digitar algum campo, receberá a seguinte mensagem de erro
</p>

```json
{
  "status": "error",
  "message": ["discount is required"]
}
```

<p>
  Se digitar um campo que não existe, receberá a seguinte mensagem de erro
</p>

```json
{
  "status": "error",
  "message": ["key teste invalid"]
}
```

<p>
  Se caso existir o nome para a categoria, receberá a seguinte mensagem de erro
</p>

```json
{
  "message": "name already exists"
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

### **Listando todas as categorias**

---

<p>
  Essa rota é responsável por renderizar todas as categorias que foram cadastradas pelo usuário admin
</p>

> Authorization: Bearer {token}

|   **url**   | **method** | **status** |
| :---------: | :--------: | :--------: |
| `/category` |   `GET`    |   `200`    |

**RESPONSE**

```json
[
  {
    "category_id": 1,
    "name": "bebidas",
    "discount": 0.07
  },
  {
    "category_id": 2,
    "name": "alimentos",
    "discount": 0.05
  }
]
```

<br>

### **Listando uma categoria especifica**

---

<p>
  Essa rota é responsável por renderizar uma categoria especifica
</p>

> Authorization: Bearer {token}

|         **url**         | **method** | **status**  |
| :---------------------: | :--------: | :---------: |
| `/category/category_id` |   `GET`    | `200 - 404` |

**RESPONSE**

```json
{
  "category_id": 2,
  "name": "alimentos",
  "discount": 0.05
}
```

### **Possíveis erros**

---

<p>
  Se não encontrar nenhuma categoria, receberá o seguinte erro
</p>

```json
{
  "message": "category not found"
}
```

<br>

### **Atualizando uma categoria**

<p>
  Rota responsável por atualizar uma categoria. Obs: somente usuário "admin" pode atualizar uma categoria
</p>

> Authorization: Bearer {token}

|         **url**         | **method** |          **status**           |
| :---------------------: | :--------: | :---------------------------: |
| `/category/category_id` |  `PATCH`   | `200 - 400 - 403 - 404 - 409` |

**BODY**

```json
{
  "discount": 0.1
}
```

**RESPONSE**

```json
{
  "category_id": 2,
  "name": "alimentos",
  "discount": 0.1
}
```

### **Possíveis erros**

---

<p>
  Se caso digitar um valor do tipo inteiro no campo discount, voce receberá o seguinte erro informando que o valor precisa ser do tipo flutuante
</p>

```json
{
  "status": "error",
  "message": ["key discount must be type float"]
}
```

<p>
  Se digitar um campo que não existe, receberá a seguinte mensagem de erro
</p>

```json
{
  "status": "error",
  "message": ["key teste invalid"]
}
```

<p>
  Se caso existir o nome para a categoria, receberá a seguinte mensagem de erro
</p>

```json
{
  "message": "name already exists"
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

### **Deletando uma categoria**

---

<p>
  Rota responsável por deletar uma categoria. Obs: Somente um usuário "admin" pode deletar uma categoria
</p>

> Authorization: Bearer {token}

|         **url**         | **method** |       **status**        |
| :---------------------: | :--------: | :---------------------: |
| `/category/category_id` |  `DELETE`  | `204 - 403 - 404 - 409` |

**RESPONSE**

> No content

### **Possíveis erros**

---

<p>
  Se não encontrar a categoria, receberá a seguinte mensagem de erro
</p>

```json
{
  "message": "category not found"
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

<p>
  se caso a categoria estiver sido relacionada a algum produto, então não poderá excluíla, e receberá a seguinte mensagem de erro
</P>

```json
{
  "message": "there are products registered with this category"
}
```

<br>

## **PRODUTO:**

### **Criando um produto**

---

<p>
  Rota responsável por criar um produto
</p>

> Authorization: Bearer {token}

|  **url**   | **method** |    **status**     |
| :--------: | :--------: | :---------------: |
| `/product` |   `POST`   | `201 - 400 - 409` |

**BODY**

```json
{
  "name": "cerveja",
  "category": "bebidas"
}
```

**RESPONSE**

```json
{
  "product_id": 2,
  "name": "cerveja",
  "category": {
    "category_id": 1,
    "name": "bebidas",
    "discount": 0.05
  }
}
```

### **Possíveis erros**

---

<p>
  se caso tentar cadastrar um produto que já existe, receberá a seguinte mensagem de erro
</p>

```json
{
  "message": "name already exists"
}
```

<p>
  se passar algum valor com o tipo diferente, receberá a seguinte mensagem de erro
</p>

```json
{
  "status": "error",
  "message": ["key category must be type str"]
}
```

<p>
  se caso tentar cadastrar um produto sem enviar algum campo, receberá a seguinte mensagem de erro
</p>

```json
{
  "status": "error",
  "message": ["category is required"]
}
```

<p>
  se tentar cadastrar um produto com algum campo que não existe, receberá a seguinte mensagem de erro
</p>

```json
{
  "status": "error",
  "message": ["key teste invalid"]
}
```

### **Listando todos os produtos**

---

<p>
  Rota responsável por renderizar todos os produtos cadastrados
</p>

> Authorization: Bearer {token}

|  **url**   | **method** | **status** |
| :--------: | :--------: | :--------: |
| `/product` |   `GET`    |   `200`    |

**RESPONSE**

```json
[
  {
    "product_id": 1,
    "name": "guarana",
    "category": {
      "category_id": 1,
      "name": "bebidas",
      "discount": 0.05
    }
  },
  {
    "product_id": 2,
    "name": "cerveja",
    "category": {
      "category_id": 1,
      "name": "bebidas",
      "discount": 0.05
    }
  }
]
```

<br>

### **Listando um produto especifico**

---

<p>
  Rota responsável por buscar um produto específico
</p>

> Authorization: Bearer {token}

|        **url**        | **method** | **status**  |
| :-------------------: | :--------: | :---------: |
| `/product/product_id` |   `GET`    | `200 - 404` |

**RESPONSE**

```json
{
  "product_id": 1,
  "name": "guarana",
  "category": {
    "category_id": 1,
    "name": "bebidas",
    "discount": 0.05
  }
}
```

### **Possíveis problemas**

---

<p>
  se caso não encontrar o produto específico, receberá a seguinte mensagem de erro
</p>

```json
{
  "message": "product not found"
}
```

<br>

### **Atualizando um produto**

---

<p>
  Rota responsável por atualizar um produto
</p>

> Authorization: Bearer {token}

|        **url**        | **method** |       **status**        |
| :-------------------: | :--------: | :---------------------: |
| `/product/product_id` |  `PATCH`   | `200 - 400 - 404 - 409` |

**BODY**

```json
{
  "category": "bebidas"
}
```

**RESPONSE**

```json
{
  "product_id": 1,
  "name": "guarana",
  "category": {
    "category_id": 1,
    "name": "bebidas",
    "discount": 0.05
  }
}
```

### **Possíveis erros**

---

<p>
  se caso não encontrar o produto, receberá a seguinte mensagem de erro
</p>

```json
{
  "message": "product not found"
}
```

<p>
  se caso tentar atualizar o nome do produto por um nome que ja existe, receberá a seguinte mensagem de erro
</p>

```json
{
  "message": "name already exists"
}
```

<p>
  se caso tentar atualizar a categoria de um produto e não for encontrado no banco de dados, receberá a seguinte mensagem de erro
</p>

```json
{
  "message": "category not found"
}
```

<p>
  se caso tentar atualizar um produto com um campo que não existe, receberá a seguinte mensagem de erro
</p>

```json
{
  "status": "error",
  "message": ["key name1 invalid"]
}
```

<br>

### **Deletando um produto**

---

<p>
  Rota responsável por deletar um produto
</p>

> Authorization: Bearer {token}

|        **url**        | **method** | **status**  |
| :-------------------: | :--------: | :---------: |
| `/product/product_id` |  `DELETE`  | `204 - 404` |

**RESPONSE**

> No content

### **Possíveis erros**

---

<p>
  se caso não encontrar o produto, reberá a seguinte mensagem de erro
</p>

```json
{
  "message": "product not found"
}
```

<br>

## **ORDER**

### **Criando um pedido**

---

<p>
  Rota responsável por criar um pedido de compra de um usuário, para isso é necessário enviar o cpf do cliente em que voce deseja efetuar o pedido. Obs: O valor do campo <i>sold_at</i> foi adicionado como datetime.utcnow() para que a data possa ser convertido e visualizado de acordo com o local da pessoa que esta visualizando a ordem.
</p>

> Authorization: Bearer {token}

| **url**  | **method** |    **status**     |
| :------: | :--------: | :---------------: |
| `/order` |   `POST`   | `201 - 400 - 404` |

**BODY**

```json
{
  "cpf": "25579585063"
}
```

**RESPONSE**

```json
{
  "order_id": 3,
  "sold_at": "Thu, 06 Jan 2022 11:40:49 GMT",
  "total": null,
  "customer": {
    "customer_id": 3,
    "cpf": "25579585063",
    "name": "flavio reis"
  },
  "cashback_id": null
}
```

### **Possíveis erros**

---

<p>
  se caso não tiver cadastrado o cliente, voce irá receber uma mensagem de erro
</p>

```json
{
  "message": "customer not found"
}
```

<p>
  se caso enviar o cpf com o tipo errado voce receberá a seguinte mensagem de erro
</p>

```json
{
  "status": "error",
  "message": ["key cpf must be type str"]
}
```

<p>
  se caso enviar o cpf no formato errado receberá a seguinte mensagem de erro
</p>

```json
{
  "message": "cpf must be in format xxxxxxxxxxx"
}
```

<p>
  se caso enviar um campo que não existe, receberá a seguinte mensagem de erro
</p>

```json
{
  "status": "error",
  "message": ["key cpf1 invalid"]
}
```

<br>

### **Listando todos os pedidos**

---

<p>
  essa rota é responsável por listar todos os pedidos de clientes
</p>

> Authorization: Bearer {token}

| **url**  | **method** | **status** |
| :------: | :--------: | :--------: |
| `/order` |   `GET`    |   `200`    |

**RESPONSE**

```json
[
  {
    "order_id": 1,
    "sold_at": "Thu, 06 Jan 2022 11:40:49 GMT",
    "customer": {
      "customer_id": 11,
      "cpf": "56975797056",
      "name": "maria fernanda"
    },
    "total": null,
    "itens": [],
    "cashback_id": null
  },
  {
    "order_id": 2,
    "sold_at": "Thu, 06 Jan 2022 12:31:18 GMT",
    "customer": {
      "customer_id": 3,
      "cpf": "25579585063",
      "name": "flavio reis"
    },
    "total": null,
    "itens": [],
    "cashback_id": null
  },
  {
    "order_id": 3,
    "sold_at": "Thu, 06 Jan 2022 12:31:18 GMT",
    "customer": {
      "customer_id": 3,
      "cpf": "25579585063",
      "name": "flavio reis"
    },
    "total": null,
    "itens": [],
    "cashback_id": null
  }
]
```

<br>

### **Listando um pedido especifico**

---

<p>
  Esta rota tem por objetivo listar um pedido específico
</p>

> Authorization: Bearer {token}

|      **url**      | **method** | **status**  |
| :---------------: | :--------: | :---------: |
| `/order/order_id` |   `GET`    | `200 - 404` |

**RESPONSE**

Exemplo de um pedido sem itens:

```json
{
  "order_id": 3,
  "sold_at": "Thu, 06 Jan 2022 12:31:18 GMT",
  "customer": {
    "customer_id": 3,
    "cpf": "25579585063",
    "name": "Flavio Reis"
  },
  "total": null,
  "itens": [],
  "cashback_id": null
}
```

Exemplo de um pedido com itens e com um cashback gerado:

```json
{
  "order_id": 3,
  "sold_at": "Thu, 06 Jan 2022 12:31:18 GMT",
  "customer": {
    "customer_id": 3,
    "cpf": "25579585063",
    "name": "Flavio Reis"
  },
  "total": 38.58,
  "itens": [
    {
      "register_id": 19,
      "product": "guarana",
      "value": 7.99,
      "qty": 2
    },
    {
      "register_id": 20,
      "product": "cerveja",
      "value": 2.35,
      "qty": 6
    },
    {
      "register_id": 21,
      "product": "coca-cola",
      "value": 8.5,
      "qty": 1
    }
  ],
  "cashback_id": 87
}
```

### **Possíveis erros**

---

<p>
  caso não encontrar o pedido, será retornado uma mensagem de erro
</p>

```json
{
  "message": "order not found"
}
```

<br>

### **Deletando um pedido**

---

> Authorization: Bearer {token}

|      **url**      | **method** | **status**  |
| :---------------: | :--------: | :---------: |
| `/order/order_id` |  `DELETE`  | `204 - 404` |

**RESPONSE**

> No content

### **Possíveis erros**

---

<p>
  se caso não encontrar o pedido, receberá a seguinte mensagem de erro
</p>

```json
{
  "message": "order not found"
}
```

<br>

## **ITEM:**

### **Adicionando item a um pedido**

---

<p>
  Esta rota tem por objetivo adicionar um item a um pedido. Este item é composto por três campos, sendo eles: "name" que se refere ao nome do produto, "value" que se refere ao valor unitário do produto, "qty" que se refere a quantidade de produto. Tudo isso resultando em um item que será cadastrado a um pedido de compra de um cliente. Se adicionar um novo item, será retornado uma lista com os itens atuais do pedido mais o novo item adicionado.
</p>

> Authorization: Bearer {token}

|        **url**         | **method** | **status**  |
| :--------------------: | :--------: | :---------: |
| `/order/order_id/item` |   `POST`   | `201 - 404` |

**BODY**

```json
{
  "name": "cerveja",
  "value": 2.35,
  "qty": 6
}
```

**RESPONSE**

```json
[
  {
    "item_id": 19,
    "product": {
      "product_id": 7,
      "name": "guarana",
      "category": "bebidas"
    },
    "value": 7.99,
    "qty": 2
  },
  {
    "item_id": 20,
    "product": {
      "product_id": 2,
      "name": "cerveja",
      "category": "bebidas"
    },
    "value": 2.35,
    "qty": 6
  }
]
```

### **Possíveis erros**

---

<p>
  se não passar todos os campos necessários, será retornado uma mensagem de erro
</p>

```json
{
  "status": "error",
  "message": ["qty is required"]
}
```

<p>
  se caso enviar algum valor com o tipo diferente, será retornado uma mensagem de erro
</p>

```json
{
  "status": "error",
  "message": ["key value must be type float"]
}
```

<p>
  se caso enviar alguma chave com o tipo diferente, será retornado uma mensagem de erro
</p>

```json
{
  "status": "error",
  "message": ["key teste invalid"]
}
```

<p>
  se caso enviar um produto que não existe, será retornado uma mensagem de erro
</p>

```json
{
  "message": "product not found"
}
```

<p>
se caso tentar um item com um produto que já existe no pedido, será retornado a seguinte mensagem de erro
</p>

```json
{
  "message": "Item already exists"
}
```

<br>

### **Listando todos os itens**

---

<p>
  essa rota tem por objetivo retornar uma lista com todos os itens
</p>

> Authorization: Bearer {token}

|    **url**    | **method** |  **status**  |
| :-----------: | :--------: | :----------: |
| `/order/item` |   `GET`    | ` 200 - 404` |

**RESPONSE**

```json
[
  {
    "item_id": 19,
    "product": {
      "product_id": 7,
      "name": "guarana",
      "category": "bebidas"
    },
    "value": 7.99,
    "qty": 2
  },
  {
    "item_id": 20,
    "product": {
      "product_id": 2,
      "name": "cerveja",
      "category": "bebidas"
    },
    "value": 2.35,
    "qty": 6
  }
]
```

### **Listando um item especifico**

---

<p>
  essa rota tem por objetivo retornar as informações de um item específico
</p>

> Authorization: Bearer {token}

|        **url**        | **method** |  **status**  |
| :-------------------: | :--------: | :----------: |
| `/order/item/item_id` |   `GET`    | ` 200 - 404` |

**RESPONSE**

```json
{
  "item_id": 19,
  "product": {
    "product_id": 7,
    "name": "guarana",
    "category": {
      "category_id": 1,
      "name": "bebidas"
    }
  },
  "value": 7.99,
  "qty": 2
}
```

### **Possíveis erros**

---

<p>
  se caso não encontrar o item, será retornado uma mensgem de erro
</p>

```json
{
  "message": "item not found"
}
```

<br>

### **Listando todos os itens de um pedido**

---

<p>
  Essa rota tem por objetivo retornar uma lista com todos os itens de um pedido de um cliente
</p>

> Authorization: Bearer {token}

|        **url**         | **method** |  **status**  |
| :--------------------: | :--------: | :----------: |
| `/order/order_id/item` |   `GET`    | ` 200 - 404` |

**RESPONSE**

```json
[
  {
    "item_id": 19,
    "product": {
      "product_id": 7,
      "name": "guarana",
      "category": "bebidas"
    },
    "value": 7.99,
    "qty": 2
  },
  {
    "item_id": 20,
    "product": {
      "product_id": 14,
      "name": "cerveja",
      "category": "bebidas"
    },
    "value": 2.35,
    "qty": 6
  },
  {
    "item_id": 21,
    "product": {
      "product_id": 6,
      "name": "coca-cola",
      "category": "Bebidas"
    },
    "value": 8.5,
    "qty": 1
  }
]
```

### **Possíveis erros**

---

<p>
  se caso não encontrar o pedido, será retornado uma mensagem de erro
</p>

```json
{
  "message": "order not found"
}
```

<br>

### **Atualizando um item**

---

<p>
  essa rota tem por objetivo atualizar um item. Obs: diferente das outras rotas, essa especificamente atualiza um item se for enviado todos os campos.
</p>

> Authorization: Bearer {token}

|        **url**        | **method** |     **status**     |
| :-------------------: | :--------: | :----------------: |
| `/order/item/item_id` |   `PUT`    | ` 200 - 400 - 404` |

**BODY**

```json
{
  "name": "guarana",
  "value": 10.0,
  "qty": 3
}
```

**RESPONSE**

```json
{
  "item_id": 20,
  "product": {
    "product_id": 7,
    "name": "guarana",
    "category": {
      "category_id": 3,
      "name": "bebidas"
    }
  },
  "value": 10.0,
  "qty": 3
}
```

### **Possíveis erros**

---

<p>
  se caso não for enviado todos os campos necessários
<p>

```json
{
  "status": "error",
  "message": ["qty is required"]
}
```

<p>
  se caso enviar um valor com o tipo errado
</p>

```json
{
  "status": "error",
  "message": ["key qty must be type int"]
}
```

<p>
se enviar um campo que não existe
</p>

```json
{
  "status": "error",
  "message": ["key teste invalid"]
}
```

<p>
  se caso não encontrar o item
</p>

```json
{
  "message": "item not found"
}
```

<p>
  se caso não encontrar o produto
</p>

```json
{
  "message": "product not found"
}
```

<br>

### **Deletando um item**

---

<p>
  Essa rota tem por objetivo deletar um item
</p>

> Authorization: Bearer {token}

|        **url**        | **method** |  **status**  |
| :-------------------: | :--------: | :----------: |
| `/order/item/item_id` |  `DELETE`  | ` 204 - 404` |

**RESPONSE**

> No content

### **Possíveis erros**

---

<p>
  se caso não encontrar o item
</p>

```json
{
  "message": "item not found"
}
```

<br>

## **CASHBACK**

### **Gerando um cashback**

---

<p>
  Esta rota tem por objetivo gerar cashback para um pedido de compra de um cliente. Obs: se caso adicionar um novo item ao pedido, será necessário gerar um novo cashback para atualizar o valor de desconto para o cliente.
</p>

> Authorization: Bearer {token}

|   **url**   | **method** |  **status**  |
| :---------: | :--------: | :----------: |
| `/cashback` |   `POST`   | ` 201 - 404` |

**BODY**

```json
{
  "order_id": 17
}
```

**RESPONSE**

```json
{
  "order_id": 17,
  "sold_at": "Thu, 06 Jan 2022 12:31:18 GMT",
  "customer": {
    "customer_id": 3,
    "cpf": "25579585063",
    "name": "flavio reis"
  },
  "total": 54.48,
  "itens": [
    {
      "register_id": 19,
      "product": "guarana",
      "value": 7.99,
      "qty": 2
    },
    {
      "register_id": 21,
      "product": "coca-cola",
      "value": 8.5,
      "qty": 1
    },
    {
      "register_id": 20,
      "product": "cerveja",
      "value": 10.0,
      "qty": 3
    }
  ],
  "cashback": {
    "cashback_id": 87,
    "value": 2.73
  }
}
```

### **Possíveis erros**

---

<p>
  se caso não encontrar o pedido
</p>

```json
{
  "message": "order not found"
}
```

<br>

### **Listando um cashback especifico**

---

<p>
  Essa rota tem por objetivo, listar as informações do cashback específico que foi gerado para um cliente
</p>

> Authorization: Bearer {token}

|   **url**   | **method** |  **status**  |
| :---------: | :--------: | :----------: |
| `/cashback` |   `GET`    | ` 200 - 404` |

**RESPONSE**

```json
{
  "createdAt": "2022-01-06T05:03:49.840Z",
  "message": "Cashback criado com sucesso!",
  "id": "87",
  "cashback": "1.94",
  "document": "25579585063"
}
```

### **Possíveis erros**

---

```json
{
  "message": "cashback not found"
}
```
