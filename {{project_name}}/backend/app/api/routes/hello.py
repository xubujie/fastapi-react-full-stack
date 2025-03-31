from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def hello():
    return {"message": "Hello from {{ cookiecutter.project_name }} API!"} 