from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict
from tortoise import connections
import psutil
import time

router = APIRouter(prefix="/utils", tags=["utils"])


async def check_database():
    try:
        start_time = time.time()
        conn = connections.get("default")
        await conn.execute_query("SELECT 1")

        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)

        return {
            "status": "healthy",
            "latency_ms": latency,
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@router.get("/health", response_model=Dict)
async def health_check():
    try:
        start_time = time.time()

        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()

        db_status = await check_database()

        if db_status.get("status") == "unhealthy":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Database unhealthy: {db_status.get('error')}",
            )

        response = {
            "status": "healthy",
            "timestamp": start_time,
            "system": {"cpu_usage": cpu_usage, "memory_used_percent": memory.percent},
            "dependencies": {"database": db_status},
        }

        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unhealthy: {str(e)}",
        )
