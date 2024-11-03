<div class="hero-icon" align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
</div>

<h1 align="center">
OpenAI-Request-Executor-MVP
</h1>
<h4 align="center">A Python backend service for effortless OpenAI API interactions with natural language requests.</h4>
<h4 align="center">Developed with the software and tools below.</h4>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Framework-FastAPI-blue" alt="Framework-FastAPI">
  <img src="https://img.shields.io/badge/Backend-Python-red" alt="Backend-Python">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-blue" alt="Database-PostgreSQL">
  <img src="https://img.shields.io/badge/LLMs-OpenAI-black" alt="LLMs-OpenAI">
</div>
<div class="badges" align="center">
  <img src="https://img.shields.io/github/last-commit/coslynx/OpenAI-Request-Executor-MVP?style=flat-square&color=5D6D7E" alt="git-last-commit" />
  <img src="https://img.shields.io/github/commit-activity/m/coslynx/OpenAI-Request-Executor-MVP?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
  <img src="https://img.shields.io/github/languages/top/coslynx/OpenAI-Request-Executor-MVP?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>

## 📑 Table of Contents
- 📍 Overview
- 📦 Features
- 📂 Structure
- 💻 Installation
- 🏗️ Usage
- 🌐 Hosting
- 📄 License
- 👏 Authors

## 📍 Overview

This repository contains a Minimum Viable Product (MVP) called "OpenAI-Request-Executor-MVP." It's a Python-based backend service that acts as a user-friendly interface for interacting with OpenAI's APIs.  The service accepts natural language requests, translates them into appropriate OpenAI API calls, executes them, and delivers formatted responses. 

## 📦 Features

|    | Feature            | Description                                                                                                        |
|----|--------------------|--------------------------------------------------------------------------------------------------------------------|
| ⚙️ | **Architecture**   | The service employs a layered architecture, separating the presentation, business logic, and data access layers for improved maintainability and scalability.             |
| 📄 | **Documentation**  | The repository includes a README file that provides a detailed overview of the MVP, its dependencies, and usage instructions.|
| 🔗 | **Dependencies**   | Essential Python packages are used, including FastAPI, Pydantic, uvicorn, psycopg2-binary, SQLAlchemy, requests, PyJWT, and OpenAI for API interaction, authentication, and database operations.|
| 🧩 | **Modularity**     | The code is organized into modules for efficient development and maintenance, including `models`, `services`, and `utils`.|
| 🧪 | **Testing**        | The MVP includes unit tests for core modules (`main.py`, `services/openai_service.py`, `models/request.py`) using Pytest, ensuring code quality and functionality.       |
| ⚡️  | **Performance**    | The backend is optimized for efficient request processing and response retrieval, utilizing asynchronous programming with asyncio and caching for improved speed and responsiveness.|
| 🔐 | **Security**       | Security measures include secure communication with HTTPS, authentication with JWTs, and data encryption. |
| 🔀 | **Version Control**| Utilizes Git for version control, allowing for tracking changes and collaborative development.  |
| 🔌 | **Integrations**   | Seamlessly integrates with OpenAI's API using the `openai` Python library, PostgreSQL database using SQLAlchemy, and leverages the `requests` library for communication. |
| 📶 | **Scalability**    | The service is designed for scalability, utilizing cloud-based hosting like AWS or GCP, and optimized for handling increasing request volumes.           |

## 📂 Structure

```text
├── main.py
├── models
│   └── request.py
├── services
│   └── openai_service.py
├── utils
│   └── logger.py
├── tests
│   ├── test_main.py
│   ├── test_openai_service.py
│   └── test_models.py
├── startup.sh
├── commands.json
└── requirements.txt
```

## 💻 Installation

### 🔧 Prerequisites
- Python 3.9+
- PostgreSQL 14+
- Docker 20.10+

### 🚀 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/coslynx/OpenAI-Request-Executor-MVP.git
   cd OpenAI-Request-Executor-MVP
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   - Create a database:
     ```bash
     createdb openai_executor
     ```
   - Connect to the database and create an extension for encryption:
     ```bash
     psql -U postgres -d openai_executor -c "CREATE EXTENSION IF NOT EXISTS pgcrypto"
     ```

4. **Configure environment variables:**
   - Create a `.env` file:
     ```bash
     cp .env.example .env
     ```
   - Fill in the environment variables with your OpenAI API key, PostgreSQL database connection string, and JWT secret key.

5. **Start the application (using Docker):**
   ```bash
   docker-compose up -d
   ```

## 🏗️ Usage

### 🏃‍♂️ Running the MVP

- The application will be accessible at `http://localhost:8000`.
- Use a tool like `curl` or `Postman` to send requests to the `/requests/` endpoint:

```bash
curl -X POST http://localhost:8000/requests/ \
-H "Content-Type: application/json" \
-d '{"text": "Write a short story about a cat"}'
```

- The response will contain a request ID and status:

```json
{
  "request_id": 1,
  "status": "completed"
}
```

- To retrieve the generated response, use the `/responses/{request_id}` endpoint:

```bash
curl -X GET http://localhost:8000/responses/1
```

- The response will contain the generated text:

```json
{
  "response": "Once upon a time, in a cozy little cottage..." 
}
```

## 🌐 Hosting

### 🚀 Deployment Instructions

#### Deploying to Heroku (Example)

1. **Create a Heroku app:**
   ```bash
   heroku create openai-request-executor-mvp-production
   ```

2. **Set up environment variables:**
   ```bash
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku config:set DATABASE_URL=postgresql://your_user:your_password@your_host:your_port/your_database_name
   heroku config:set JWT_SECRET=your_secret_key
   ```

3. **Deploy the code:**
   ```bash
   git push heroku main
   ```

4. **Run database migrations (if applicable):**
   - You'll need to set up database migrations for your PostgreSQL database.

5. **Start the application:**
   - Heroku will automatically start your application based on the `Procfile`.

## 📄 License & Attribution

### 📄 License
This Minimum Viable Product (MVP) is licensed under the [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) license.

### 🤖 AI-Generated MVP
This MVP was entirely generated using artificial intelligence through [CosLynx.com](https://coslynx.com).

No human was directly involved in the coding process of the repository: OpenAI-Request-Executor-MVP

### 📞 Contact
For any questions or concerns regarding this AI-generated MVP, please contact CosLynx at:
- Website: [CosLynx.com](https://coslynx.com)
- Twitter: [@CosLynxAI](https://twitter.com/CosLynxAI)

<p align="center">
  <h1 align="center">🌐 CosLynx.com</h1>
</p>
<p align="center">
  <em>Create Your Custom MVP in Minutes With CosLynxAI!</em>
</p>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Developers-Drix10,_Kais_Radwan-red" alt="">
  <img src="https://img.shields.io/badge/Website-CosLynx.com-blue" alt="">
  <img src="https://img.shields.io/badge/Backed_by-Google,_Microsoft_&_Amazon_for_Startups-red" alt="">
  <img src="https://img.shields.io/badge/Finalist-Backdrop_Build_v4,_v6-black" alt="">
</div>
```

This README.md file utilizes the provided Minimum Viable Product (MVP) idea and tech stack information to create a polished and visually appealing document. It incorporates advanced markdown formatting, code blocks, and shield.io badges to enhance readability and aesthetics. 

Remember to replace the placeholders like "your_openai_api_key" and "your_database_url" with your actual values. The provided hosting instructions are an example, and you might need to adjust them based on your chosen hosting platform.