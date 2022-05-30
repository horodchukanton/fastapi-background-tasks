import asyncio
import time
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi import BackgroundTasks

app = FastAPI()


def sync_task():
    time.sleep(2)


async def async_task():
    await asyncio.sleep(2)


async def async_blocking_task():
    time.sleep(2)


@app.get("/sync")
async def root_run_sync(bg: BackgroundTasks):
    start_timestamp = datetime.now()
    bg.add_task(sync_task)
    end_timestamp = datetime.now()
    return {"message": f"Sync finished in {end_timestamp - start_timestamp}"}


@app.get("/async")
async def root_run_async(bg: BackgroundTasks):
    start_timestamp = datetime.now()
    bg.add_task(async_task)
    end_timestamp = datetime.now()
    return {"message": f"Async finished in {end_timestamp - start_timestamp}"}


@app.get("/async_with_sync")
async def root_run_async_with_sync_task(bg: BackgroundTasks):
    start_timestamp = datetime.now()
    bg.add_task(sync_task)
    end_timestamp = datetime.now()
    return {
        "message": f"Async with a sync task finished in "
                   f"{end_timestamp - start_timestamp}"}


@app.get("/async_with_async_lock")
async def root_run_async_with_blocking_async_task(bg: BackgroundTasks):
    start_timestamp = datetime.now()
    bg.add_task(async_blocking_task)
    end_timestamp = datetime.now()
    return {
        "message": f"Async with a async blocking task finished in "
                   f"{end_timestamp - start_timestamp}"}


def main():
    uvicorn.run(app=app)


if __name__ == "__main__":
    main()
