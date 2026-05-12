import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy.orm import Session
from database.database import sessionlocal
from models.tables.config_details import ConfigDetails
from models.responses.config_details_response import ConfigDetailsRequest
from typing import Union


async def get_all_triggered_records(db: Session) :
    result = db.query(ConfigDetails).all()
    if not result:
        return None
    return [item for item in result]

async def get_triggered_record_by_id(db: Session, record_id: int) -> Union[ConfigDetails, None]:
    return db.query(ConfigDetails).filter(ConfigDetails.id == record_id).first()

import asyncio

if __name__ == "__main__":
    db = sessionlocal()
    result = asyncio.run(get_all_triggered_records(db=db))
    print(result)