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


def setup_frontend_dir(frontend_dir):
    """Setup the frontend directory"""
    print("🚀 Setting up frontend directory...")

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


def install_frontend_dependencies(frontend_dir):
    """Install frontend dependencies"""
    # Create frontend with Vite
    print("📦 Setting up frontend with React + Vite + TypeScript stack...")
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


def setup_shadcn_ui(frontend_dir):
    """Setup shadcn UI components"""
    print("🎨 Setting up shadcn/ui...")
    run_command("pnpm dlx shadcn@latest init --yes", cwd=frontend_dir)

    # Add all shadcn components
    print("📦 Adding all shadcn/ui components...")
    run_command("pnpm dlx shadcn@latest add", cwd=frontend_dir)


def print_summary():
    """Print setup summary"""
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


def post_generation(answers: dict):
    """Post-generation function for Copier"""
    print("🚀 Running post-generation tasks...")

    # Setup frontend
    frontend_dir = os.path.join(os.path.realpath(os.path.curdir), "frontend")

    # Setup frontend directory
    setup_frontend_dir(frontend_dir)

    # Install dependencies
    install_frontend_dependencies(frontend_dir)

    # Setup shadcn UI
    setup_shadcn_ui(frontend_dir)

    # Print summary
    print_summary()


# Call the post_generation function when the script is executed
if __name__ == "__main__":
    post_generation({})
