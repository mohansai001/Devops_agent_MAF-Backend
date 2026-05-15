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
    response ={}
    response = await CI_Builder(repo_name=repo_name, techstack=language, tool=tool_name, branch_name=branch_name)
    artifact_name = str(response.get("Artifact_name","insureflowwebappdrop")) #type: ignore
    workflow_name = str(response.get("Workflow_name","React CI Pipeline"))#type: ignore
    ci_filename = str(response.get("ci_filename","react-ci.yml")) #type: ignore
    logger.info("[terraform_agent] Called with prompt.")
    print("[terraform_agent] Called with prompt.")
    cloud_provider = "azure"
    deploy_target_name = str(record.config.get("DEPLOY_TARGET"))
    target_service_name = str(record.config.get("APP_NAME"))
    target_service_location = str(record.config.get("LOCATION"))
    target_service_sku = str(record.config.get("APP_SERVICE_SKU"))
    resource_group_name = str(record.config.get("RESOURCE_GROUP"))
    resource_group_location = str(record.config.get("LOCATION"))
    tf_repo_name = "Shashank-workflow"


    # response1 = await TF_Module_builder(
    #     repo_name="Shashank-workflow",
    #     cloud_provider=cloud_provider,
    #     deploy_target_name=deploy_target_name,
    #     target_service_name=target_service_name,
    #     target_service_location=target_service_location,
    #     target_service_sku=target_service_sku,
    #     resource_group_name=resource_group_name,
    #     resource_group_location=resource_group_location
    # )

    # response2 = TF_Builder()

    response3 =await CD_Builder(tool=tool_name,
                                repo_name=repo_name, 
                                artifact_name=artifact_name, #type: ignore
                                workflow_name= workflow_name, #type: ignore
                                branch=branch_name,
                                techstack=language,
                                target = deploy_target_name, 
                                ci_file_name=ci_filename, #type: ignore
                                deploy_target_name=target_service_name,
                                resource_group_name=resource_group_name ) #type: ignore


    

    print(response3)

import asyncio
if __name__ == "__main__": 
    # Example usage
    from database.database import sessionlocal
    db = sessionlocal()
    asyncio.run(fallback_pipeline(db, 8))

    


