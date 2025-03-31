#!/usr/bin/env python
"""
Post-generation script for cookiecutter-fastapi-vite
"""
import os
import shutil
import subprocess

# Get the project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def run_command(cmd, cwd=None):
    """Run a shell command and handle errors"""
    try:
        subprocess.run(cmd, check=True, shell=True, cwd=cwd)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return False


def main():
    """Main post-generation function"""
    print("🚀 Running post-generation tasks...")

    # Setup initial git repo
    subprocess.run(["git", "init"], cwd=PROJECT_DIRECTORY, check=False)

    # Setup backend directories
    os.makedirs(
        os.path.join(PROJECT_DIRECTORY, "backend", "app", "api", "routes"),
        exist_ok=True,
    )
    os.makedirs(
        os.path.join(PROJECT_DIRECTORY, "backend", "app", "core"), exist_ok=True
    )
    os.makedirs(
        os.path.join(PROJECT_DIRECTORY, "backend", "app", "models"), exist_ok=True
    )
    os.makedirs(
        os.path.join(PROJECT_DIRECTORY, "backend", "app", "services"), exist_ok=True
    )

    # Create __init__.py files
    python_dirs = [
        "backend/app",
        "backend/app/api",
        "backend/app/api/routes",
        "backend/app/core",
        "backend/app/models",
        "backend/app/services",
    ]

    for dir_path in python_dirs:
        init_file = os.path.join(PROJECT_DIRECTORY, dir_path, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write("# Auto-generated file\n")

    # Create FastAPI routes
    routes_init_content = """from fastapi import APIRouter
from app.api.routes import hello

api_router = APIRouter()
api_router.include_router(hello.router, prefix="/hello", tags=["hello"])
"""

    with open(
        os.path.join(
            PROJECT_DIRECTORY, "backend", "app", "api", "routes", "__init__.py"
        ),
        "w",
    ) as f:
        f.write(routes_init_content)

    hello_route_content = """from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def hello():
    return {"message": "Hello from FastAPI!"}
"""

    with open(
        os.path.join(PROJECT_DIRECTORY, "backend", "app", "api", "routes", "hello.py"),
        "w",
    ) as f:
        f.write(hello_route_content)

    # Create main.py
    main_content = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
"""

    with open(os.path.join(PROJECT_DIRECTORY, "backend", "app", "main.py"), "w") as f:
        f.write(main_content)

    # Create config.py
    config_content = """from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI React Boilerplate"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///app.db")
    
    class Config:
        case_sensitive = True
        
settings = Settings()
"""

    with open(
        os.path.join(PROJECT_DIRECTORY, "backend", "app", "core", "config.py"), "w"
    ) as f:
        f.write(config_content)

    # Create requirements.txt with latest versions
    requirements_content = """fastapi>=0.110.0
uvicorn>=0.27.0
pydantic>=2.6.0
pydantic-settings>=2.2.1
python-dotenv>=1.0.0
sqlmodel>=0.0.14
alembic>=1.13.1
pytest>=8.0.0
httpx>=0.27.0
"""

    with open(os.path.join(PROJECT_DIRECTORY, "backend", "requirements.txt"), "w") as f:
        f.write(requirements_content)

    # Create .dockerignore files
    docker_ignore_backend = """
.git
.env
venv
.venv
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
.coverage
htmlcov/
.pytest_cache/
.tox/
.vscode/
.idea/
*.db
"""

    with open(os.path.join(PROJECT_DIRECTORY, "backend", ".dockerignore"), "w") as f:
        f.write(docker_ignore_backend)

    docker_ignore_frontend = """
.git
node_modules
dist
.DS_Store
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.vscode/
.idea/
"""

    with open(os.path.join(PROJECT_DIRECTORY, "frontend", ".dockerignore"), "w") as f:
        f.write(docker_ignore_frontend)

    # Setup frontend using appropriate Vite template
    frontend_dir = os.path.join(PROJECT_DIRECTORY, "frontend")

    # Remove default frontend placeholder if anything exists
    if os.path.exists(frontend_dir):
        for item in os.listdir(frontend_dir):
            item_path = os.path.join(frontend_dir, item)
            if item != ".dockerignore" and item != ".gitignore":
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
    else:
        os.makedirs(frontend_dir, exist_ok=True)

    # Set up frontend with shadcn/ui template by default
    print("Setting up frontend with shadcn/ui template...")
    run_command(
        "pnpm create vite --template vite-react-ts-shadcn-starter .", cwd=frontend_dir
    )

    # Install dependencies
    print("Installing frontend dependencies...")
    run_command("pnpm install", cwd=frontend_dir)

    # Add additional dependencies by default
    print("Adding additional dependencies...")
    run_command("pnpm add zustand @tanstack/react-query axios", cwd=frontend_dir)

    # Create App.tsx with FastAPI connection
    app_tsx_content = """import { useState, useEffect } from 'react'
    import axios from 'axios'
    import './App.css'

    const api = axios.create({
        baseURL: 'http://localhost:8000/api/v1'
    })

    function App() {
        const [message, setMessage] = useState('Loading...')
        const [isLoading, setIsLoading] = useState(true)
        const [error, setError] = useState<string | null>(null)

        useEffect(() => {
            const fetchData = async () => {
                try {
                    const { data } = await api.get('/hello')
                    setMessage(data.message)
                    setIsLoading(false)
                } catch (err) {
                    setError(err instanceof Error ? err.message : 'An error occurred')
                    setIsLoading(false)
                }
            }

            fetchData()
        }, [])

        return (
            <div className="min-h-screen flex flex-col items-center justify-center bg-background">
                <div className="container flex flex-col items-center gap-4 px-4 py-8 md:px-6">
                    <h1 className="text-4xl font-bold tracking-tighter">FastAPI + React App</h1>
                    {isLoading ? (
                        <div className="flex items-center gap-2">
                            <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
                            <p>Loading data from API...</p>
                        </div>
                    ) : error ? (
                        <div className="p-4 bg-destructive/10 text-destructive rounded-lg">
                            <p>Error: {error}</p>
                        </div>
                    ) : (
                        <div className="text-center space-y-2">
                            <p className="text-lg">Message from backend:</p>
                            <p className="text-2xl font-semibold text-primary">{message}</p>
                        </div>
                    )}
                </div>
            </div>
        )
    }

    export default App"""

    with open(os.path.join(frontend_dir, "src", "App.tsx"), "w") as f:
        f.write(app_tsx_content)

    # Create a Dockerfile for the frontend
    dockerfile_frontend = """FROM node:20-alpine

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy package files
COPY package.json pnpm-lock.yaml* ./

# Install dependencies
RUN pnpm install

# Copy project files
COPY . .

# Expose port
EXPOSE ${FRONTEND_PORT:-5173}

# Start development server
CMD ["pnpm", "dev", "--", "--host", "0.0.0.0"]
"""

    with open(os.path.join(frontend_dir, "Dockerfile"), "w") as f:
        f.write(dockerfile_frontend)

    # Create docker-compose.yml
    docker_compose_content = """version: '3.8'

services:
    backend:
        build:
            context: ./backend
            dockerfile: Dockerfile
        ports:
            - "8000:8000"
        volumes:
            - ./backend:/app
        environment:
            - DEBUG=True
            - DATABASE_URL=sqlite:///app.db
        command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

    frontend:
        build:
            context: ./frontend
            dockerfile: Dockerfile
        ports:
            - "5173:5173"
        volumes:
            - ./frontend:/app
            - /app/node_modules
        environment:
            - VITE_API_URL=http://localhost:8000/api/v1
        depends_on:
            - backend
"""

    with open(os.path.join(PROJECT_DIRECTORY, "docker-compose.yml"), "w") as f:
        f.write(docker_compose_content)

    # Create .env file
    env_content = """DEBUG=True
DATABASE_URL=sqlite:///app.db
"""

    with open(os.path.join(PROJECT_DIRECTORY, ".env"), "w") as f:
        f.write(env_content)

    # Setup SQLModel and Alembic by default
    os.makedirs(os.path.join(PROJECT_DIRECTORY, "backend", "alembic"), exist_ok=True)
    os.makedirs(
        os.path.join(PROJECT_DIRECTORY, "backend", "alembic", "versions"), exist_ok=True
    )

    # Create base model
    base_model_content = """from sqlmodel import SQLModel as _SQLModel

class SQLModel(_SQLModel):
    class Config:
        arbitrary_types_allowed = True
"""

    with open(
        os.path.join(PROJECT_DIRECTORY, "backend", "app", "models", "base.py"), "w"
    ) as f:
        f.write(base_model_content)

    print("✅ Post-generation tasks completed!")
    print("\n🎉 Your project is ready! Next steps:")
    print(f"  cd {os.path.basename(PROJECT_DIRECTORY)}")
    print("\n🐳 To use Docker:")
    print("  docker-compose up")
    print("\n📋 Setup summary:")
    print("  ✅ Backend: FastAPI with SQLModel and Alembic")
    print("  ✅ Frontend: React with Vite, shadcn/ui, Zustand, and React Query")
    print("  ✅ Docker: Containerized development environment")
    print("\n🌐 Access your application at:")
    print("  Frontend: http://localhost:5173")
    print("  Backend API: http://localhost:8000/api/v1/hello")
    print("  API Docs: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
