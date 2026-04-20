Minha segunda API de autenticação com JWT feita em Python + Flask

O que essa API faz?

- Cadastro de usuários
- Login com geração de token JWT
- Rota protegida que só funciona com token válido
- Senhas criptografadas com bcrypt
- Banco de dados SQLite

Tecnologias usadas:

- Python
- Flask
- JWT
- bcrypt
- SQLite

Como rodar o projeto:

1. Clone o repositório
2. Instale as dependências:
   pip install -r requirements.txt
3. Crie um arquivo .env com:
   SECRET_KEY=sua_chave_secreta_aqui
4. Rode:
   python app.py

Rotas

| Método | Rota       | Descrição                        |
|--------|------------|----------------------------------|
| POST   | /register  | Cadastra um novo usuário         |
| POST   | /login     | Faz login e retorna token JWT    |
| GET    | /perfil    | Rota protegida (precisa do token)|