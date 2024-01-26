from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel

class Job(Model):
    id = fields.IntField(pk=True) 
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    
    def __str__(self):
        return self.name


class create_job(BaseModel):
    name: str
    description: str