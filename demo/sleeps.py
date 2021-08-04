from typing import Dict, Optional, Union

import asyncio
from fastapi import APIRouter, HTTPException, Request
from fastapi.logger import logger

router = APIRouter(
    prefix="/sleeps",
    tags=["sleeps"],
    responses={404: {"description": "Not found"}},
)


async def client_disconnected(request: Request) -> bool:
    disconnected = False
    while not disconnected:
        disconnected = await request.is_disconnected()
    return True


async def cpu_heavy() -> bool:
    try:
        await asyncio.sleep(3)
        logger.info("cpu_heavy success")
        return True
    except asyncio.CancelledError as e:
        logger.error("Canceled")
        return False


@router.get("/no-context")
async def get_sleep(request: Request) -> Union[Optional[Dict], HTTPException]:
    yes = await cpu_heavy()
    return {"msg": "Slept beautifully", "success": yes}


@router.get("/with-context")
async def get_sleep_with_cancel(request: Request) -> Union[Optional[Dict], HTTPException]:
    t1 = asyncio.create_task(client_disconnected(request))
    t2 = asyncio.create_task(cpu_heavy())
    done, pending = await asyncio.wait([t1, t2], return_when=asyncio.FIRST_COMPLETED)
    for t in done:
        logger.info(f"Number of done elements: {len(done)}")
        if t == t1:
            try:
                c = t2.cancel()
                logger.info(f"Task 2 {c} cancelled = {t2.cancelled()}")
            except asyncio.CancelledError as e:
                logger.info("Cancelled was raised again in inner coroutine")
            raise HTTPException(status_code=503, detail={"msg": "Disconnected so you won't see this"})
        else:
            return {"msg": "Slept beautifully without Cancel", "success": t2.result()}
