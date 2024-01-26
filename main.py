from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import DoesNotExist
from database.connection import db_conn, db_close
from contextlib import asynccontextmanager
from app.models import Job, create_job
from fastapi import HTTPException

job_pydantic = pydantic_model_creator(Job)

asynccontextmanager
async def life_span(app: FastAPI):
    await db_conn()
    yield
    await db_close()

app = FastAPI(lifespan=life_span)

@app.get("/")
async def read():
    return {"Username": "AmirPyDev"}



@app.post("/add_job")
async def add_job(add_title: create_job): 
    job = await Job.create(**add_title.model_dump())
    return {"Job title": job.name}



@app.get("/get_jobs")
async def collect_jobs():
    result = await Job.all()
    # result = await Job.id(), Job.name(), Job.description()
    jobs = [{"id": job.id, "name": job.name, "description": job.description} for job in result]
    return jobs

@app.put("/update_job/{job_id}")
async def update_job(job_id: int, update_title: create_job):
    try:
        job = await Job.get(id=job_id)
        
        job.name = update_title.name
        job.description = update_title.description
        await job.save()
        return {"message": "Job updated successfully", "job_id": job.id}
    except DoesNotExist:
        N_avail = {"Error": "Job does not exist."}
        return HTTPException(status_code=404, detail=N_avail)


@app.delete("/delete/{job_id}")
async def delete_job(job_id: int):
    job = await Job.get_or_none(id=job_id)

    job_name = job.name
    await job.delete()

    return {"Message": f"Job '{job_name}' with ID {job_id} deleted successfully"}


register_tortoise(
    app,
    db_url='postgres://amir:passcode@localhost:5432/lamp',
    modules= {'models': ['app.models']},
    generate_schemas=True,
    add_exception_handlers=True
)