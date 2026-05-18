from fastapi import APIRouter #type: ignore
from utils.llm import get_azure_response

router = APIRouter()

@router.get("/llm/test")
async def test_llm():
    return get_azure_response("hi")
