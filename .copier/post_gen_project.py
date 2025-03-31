import os
import shutil
import subprocess
import sys


def run_command(cmd, cwd=None):
    """Run a shell command and handle errors"""
    try:
        subprocess.run(cmd, check=True, shell=True, cwd=cwd)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        # Exit with error code when a command fails
        sys.exit(1)
        return False


def post_generation(answers: dict):
    """Post-generation function for Copier"""
    print("🚀 Running post-generation tasks...")

    # Setup frontend
    frontend_dir = os.path.join(os.path.realpath(os.path.curdir), "frontend")

    # Remove default frontend placeholder if anything exists
    if os.path.exists(frontend_dir):
        for item in os.listdir(frontend_dir):
            item_path = os.path.join(frontend_dir, item)
            if not item.startswith("."):  # Preserve dot files
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
    else:
        os.makedirs(frontend_dir, exist_ok=True)

    # Set up frontend with modern stack
    print("📦 Setting up frontend with React + Vite + TypeScript stack...")

    # Create frontend with Vite
    run_command("pnpm create vite . --template react-ts", cwd=frontend_dir)

    # Install core dependencies
    print("📚 Installing frontend dependencies...")
    run_command("pnpm install", cwd=frontend_dir)

    # Add Tailwind CSS and other dependencies
    print("🎨 Adding UI and state management libraries...")
    run_command(
        "pnpm add tailwindcss @tailwindcss/vite postcss autoprefixer @tailwindcss/forms @tailwindcss/typography @tailwindcss/container-queries",
        cwd=frontend_dir,
    )

    # Add other modern frontend dependencies
    run_command(
        "pnpm add @tanstack/react-query @tanstack/react-query-devtools axios zustand @hookform/resolvers zod react-hook-form @radix-ui/react-icons clsx tailwind-merge class-variance-authority",
        cwd=frontend_dir,
    )

    # Add development dependencies
    print("🛠️ Adding development tools...")
    run_command(
        "pnpm add -D @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint eslint-config-prettier eslint-plugin-react-hooks eslint-plugin-react-refresh prettier @types/node",
        cwd=frontend_dir,
    )

    # Update index.css for Tailwind
    index_css_content = """@import "tailwindcss";"""

    with open(os.path.join(frontend_dir, "src", "index.css"), "w") as f:
        f.write(index_css_content)

    # Create tsconfig.json
    tsconfig_content = """{
  "files": [],
  "references": [
    {
      "path": "./tsconfig.app.json"
    },
    {
      "path": "./tsconfig.node.json"
    }
  ],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}"""

    with open(os.path.join(frontend_dir, "tsconfig.json"), "w") as f:
        f.write(tsconfig_content)

    # Update tsconfig.app.json
    tsconfig_app_content = """{
  "extends": "@tsconfig/vite-react/tsconfig.json",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"]
}"""

    with open(os.path.join(frontend_dir, "tsconfig.app.json"), "w") as f:
        f.write(tsconfig_app_content)

    # Create vite.config.ts
    vite_config_content = """import path from "path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})"""

    with open(os.path.join(frontend_dir, "vite.config.ts"), "w") as f:
        f.write(vite_config_content)

    # Initialize shadcn-ui
    print("🎨 Setting up shadcn/ui...")
    run_command("pnpm dlx shadcn@latest init --yes", cwd=frontend_dir)

    # Add all shadcn components
    print("📦 Adding all shadcn/ui components...")
    run_command("pnpm dlx shadcn@latest add", cwd=frontend_dir)
    # Create modular frontend structure
    os.makedirs(os.path.join(frontend_dir, "src", "lib"), exist_ok=True)
    os.makedirs(os.path.join(frontend_dir, "src", "components", "ui"), exist_ok=True)
    os.makedirs(
        os.path.join(frontend_dir, "src", "components", "common"), exist_ok=True
    )
    os.makedirs(os.path.join(frontend_dir, "src", "features"), exist_ok=True)
    os.makedirs(os.path.join(frontend_dir, "src", "hooks"), exist_ok=True)
    os.makedirs(os.path.join(frontend_dir, "src", "services"), exist_ok=True)
    os.makedirs(os.path.join(frontend_dir, "src", "utils"), exist_ok=True)
    os.makedirs(os.path.join(frontend_dir, "src", "types"), exist_ok=True)
    os.makedirs(os.path.join(frontend_dir, "src", "store"), exist_ok=True)

    # Create API service
    api_service_content = """import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if exists
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('token')
    }
    return Promise.reject(error)
  }
)"""

    with open(os.path.join(frontend_dir, "src", "services", "api.ts"), "w") as f:
        f.write(api_service_content)

    # Create store setup
    store_content = """import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  token: string | null
  setToken: (token: string | null) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      setToken: (token) => set({ token }),
    }),
    {
      name: 'auth-storage',
    }
  )
)"""

    with open(os.path.join(frontend_dir, "src", "store", "auth.ts"), "w") as f:
        f.write(store_content)

    # Create custom hooks
    hooks_content = """import { useQuery, useMutation } from '@tanstack/react-query'
import { api } from '@/services/api'

export const useAuth = () => {
  const login = useMutation({
    mutationFn: async (credentials: { email: string; password: string }) => {
      const { data } = await api.post('/auth/login', credentials)
      return data
    },
  })

  const logout = () => {
    // Implement logout logic
  }

  return { login, logout }
}

export const useUser = () => {
  return useQuery({
    queryKey: ['user'],
    queryFn: async () => {
      const { data } = await api.get('/users/me')
      return data
    },
  })
}"""

    with open(os.path.join(frontend_dir, "src", "hooks", "auth.ts"), "w") as f:
        f.write(hooks_content)

    # Create utils
    utils_content = """export const formatDate = (date: string) => {
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(date))
}

export const classNames = (...classes: (string | boolean | undefined)[]) => {
  return classes.filter(Boolean).join(' ')
}"""

    with open(os.path.join(frontend_dir, "src", "utils", "helpers.ts"), "w") as f:
        f.write(utils_content)

    # Create modern App.tsx with modular structure
    app_tsx_content = """import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useAuth } from '@/hooks/auth'
import { api } from '@/services/api'
import { useAuthStore } from '@/store/auth'
import { useState } from 'react'

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 1000,
      retry: 1,
    },
  },
})

function App() {
  const [message] = useState('Welcome to FastAPI + React!')
  const { login } = useAuth()
  const setToken = useAuthStore((state) => state.setToken)

  const handleLogin = async () => {
    try {
      const result = await login.mutateAsync({
        email: 'test@example.com',
        password: 'password',
      })
      setToken(result.token)
    } catch (error) {
      console.error('Login failed:', error)
    }
  }

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-background p-8">
        <div className="container mx-auto">
          <Card className="w-full max-w-2xl mx-auto">
            <CardHeader>
              <CardTitle className="text-4xl font-bold tracking-tight">{message}</CardTitle>
              <CardDescription className="text-lg">
                Start building your full-stack application with FastAPI and React
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex justify-center gap-4">
                <Button size="lg" onClick={handleLogin}>
                  {login.isPending ? 'Logging in...' : 'Get Started'}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}

export default App"""

    with open(os.path.join(frontend_dir, "src", "App.tsx"), "w") as f:
        f.write(app_tsx_content)

    # Create .env file for frontend
    frontend_env = """VITE_API_URL=http://localhost:8000/api/v1"""

    with open(os.path.join(frontend_dir, ".env"), "w") as f:
        f.write(frontend_env)

    print("✅ Post-generation tasks completed!")
    print("\n🎉 Your project is ready! Next steps:")
    print(f"  cd {os.path.basename(os.path.realpath(os.path.curdir))}")
    print("\n🚀 To start development:")
    print("  1. Start the backend:")
    print("     cd backend && uvicorn app.main:app --reload")
    print("  2. Start the frontend:")
    print("     cd frontend && pnpm dev")
    print("\n📋 Setup summary:")
    print("  ✅ Frontend: React + Vite + TypeScript")
    print("  ✅ UI: shadcn/ui (all components)")
    print("  ✅ State: TanStack Query + Zustand")
    print("  ✅ Forms: React Hook Form + Zod")
    print("  ✅ Development: ESLint + Prettier")
    print("  ✅ Structure: Modular with services, hooks, and utils")
    print("\n🌐 Access your application at:")
    print("  Frontend: http://localhost:5173")
    print("  Backend API: http://localhost:8000/api/v1")
    print("  API Docs: http://localhost:8000/docs")


# Call the post_generation function when the script is executed
if __name__ == "__main__":
    post_generation({})
