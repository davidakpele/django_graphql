# 🔐 Django GraphQL Authentication Manager

This project provides a modular and secure **JWT-based authentication system** using **Django**, **GraphQL**, **OAuth2**, and **Apollo Federation-ready practices**. It serves as a core authentication service in a microservices architecture and is designed to be migrated to **Go (Golang)** using GraphQL Federation and Apollo Router.

---

## ✅ Features

- **JWT Authentication** with access token validation
- **OAuth2 Integration** via `django-oauth-toolkit`
- **GraphQL API** built with `graphene-django`
- **Custom Authentication Middleware**
- **Federated Identity Support** (for future Go migration)
- Structured **error handling and responses**
- Environment-based configuration using `.env`
- Minimal external dependencies — ready for migration

---

## ⚙️ Tech Stack

| Layer         | Tech                          |
|---------------|-------------------------------|
| Backend       | Django, Django REST Framework |
| Auth & Token  | OAuth2, JWT                   |
| GraphQL       | Graphene-Django               |
| Environment   | Python `environ`              |
| DB            | PostgreSQL (default)          |

---

## 🗂 Project Structure

🧪 GraphQL Integration
- Uses graphene and graphene-django
- All GraphQL views are protected with @login_required
- User context available via info.context.user


🔄 Environment Setup
1. ## Clone the repository
```
git clone https://github.com/davidakpele/django_graphql.git
cd django_graphql
```
2. ## Create virtual environment
```
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```
3. ## Install dependencies
```
pip install -r requirements.txt
```
4. ## Configure .env
```
cp .env.example .env
```
> Update your secret keys, DB credentials, and OAuth settings.
5. ## Run migrations
```
python manage.py migrate
```
6. ## Run the server
```
python manage.py runserver
```
🚀 ## APIs Available
| Type    | Path               | Description           |
| ------- | ------------------ | --------------------- |
| REST    | `/register/`       | create user           |
| REST    | `/login`           | Login user/ get token |
| GraphQL | `/graphql/`        | Main API endpoint     |
| REST    | `/o/token/`        | OAuth2 token issuer   |
| REST    | `/o/revoke_token/` | Revoke token endpoint |

🛠 ## Ready for Migration to Go
-This Django service is designed to simplify migration to Go:
  - Stateless JWT-based flow
  -Context-aware auth middleware
  - GraphQL structure aligned with gqlgen
  - Error handling designed for Apollo Federation


## 🧑‍💻 Contributing
Fork the repo
- Create a new branch
- Add your feature
- Open a PR

## 📜 License
MIT License 
