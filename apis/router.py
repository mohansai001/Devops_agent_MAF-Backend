from fastapi import APIRouter #type: ignore
from .routes.sql import router as sql_router
from .routes.log_manager import router as log_router
from .routes.agent_routes import router as agent_router
from .routes.llm import router as llm_router

router = APIRouter()

router.include_router(sql_router,tags=["SQL"],prefix="/sql")
router.include_router(log_router,tags=["Logs"],prefix="/logs")
router.include_router(agent_router,tags=["Agents"],prefix="/agents")
router.include_router(llm_router, tags=["LLM"], prefix="/llm")
