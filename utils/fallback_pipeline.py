import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from utils.logger import get_logger
from tools.yaml_tools.base import CI_Builder, CD_Builder, TF_Builder
from tools.tf_tools.base import TF_Module_builder
from utils.crud_ops import get_triggered_record_by_id
from sqlalchemy.orm import Session


logger = get_logger(__name__)

async def fallback_pipeline(db: Session, id: int) :
    record = await get_triggered_record_by_id(db, id)
    if not record:
        logger.warning(f"No record found for ID: {id}")
        return (f"No record found for ID: {id}")
    repo_name = record.repo
    language = record.techstack.get("language", "unknown")
    tool_name = record.techstack.get("tool", "github_actions")
    branch_name = record.branch

    logger.info("[yaml_agent] Called with prompt.")
    print("[yaml_agent] Called with prompt.")
    response = await CI_Builder(repo_name=repo_name, techstack=language, tool=tool_name, branch_name=branch_name)
    logger.info("[terraform_agent] Called with prompt.")
    print("[terraform_agent] Called with prompt.")
    tf_repo_name =


    print(response)

import asyncio
if __name__ == "__main__":
    # Example usage
    from database.database import sessionlocal
    db = sessionlocal()
    asyncio.run(fallback_pipeline(db, 8))

    


