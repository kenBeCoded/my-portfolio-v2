You are an expert backend developer. I need you to build the backend for my portfolio system using FastAPI and SQL (using SQLAlchemy and Pydantic).

Here is the exact database schema you should use, written in DBML. Note that the `users` table handles admin credentials.

```dbml
Table users {
  id int [pk]
  username varchar
  password varchar
  fullname varchar
  role varchar
  updated_at timestamp
  created_at timestamp
}

Table projects {
  id int [pk]
  title varchar
  description varchar
  repo_url varchar
  live_url varchar
  status varchar [note: 'in-progress, completed, archived']
  sort_order int
  featured boolean
  is_deleted boolean
  updated_at timestamp
  created_at timestamp
}

Table techstack {
  id int [pk]
  name varchar
  category varchar [note: 'e.g. language, framework, database, devops, etc...']
  sort_order int
  updated_at timestamp
  created_at timestamp
}

Table project_techstacks {
  id int [pk]
  project_id int [ref: > projects.id]
  techstack_id int [ref: > techstack.id]
}
```

Please implement the following FastAPI endpoints. Use FastAPI's `Depends()` with a JWT dependency to protect the private routes cleanly. Passwords in the `users` table must be stored as bcrypt hashes.

**Auth**

- `POST /auth/login` — verify credentials, return a JWT token
- `POST /auth/logout` — invalidate token (if using token blocklist)
- `GET /auth/me` — validate current session

**Projects** (private routes require JWT)

- `GET /projects` — list all (public: only non-archived; private: all)
- `POST /projects` — create project
- `PUT /projects/{id}` — update project
- `DELETE /projects/{id}` — delete project
- `PATCH /projects/{id}/techstacks` — assign/remove techstacks from a project

**Techstacks**

- `GET /techstacks` — list all (public)
- `POST /techstacks` — create
- `PUT /techstacks/{id}` — update
- `DELETE /techstacks/{id}` — delete

**Users (Accounts)** (private only)

- `GET /users` — list accounts
- `POST /users` — create account
- `PUT /users/{id}` — update username or password
- `DELETE /users/{id}` — delete account

Please provide the code in a structured format:

1. Database configuration & setup
2. SQLAlchemy Models
3. Pydantic Schemas
4. Auth / Security utilities (JWT, password hashing)
5. FastAPI Routers for each module (Auth, Projects, Techstacks, Users)
6. Main application entry point (`main.py`)
