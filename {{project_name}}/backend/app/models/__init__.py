# Import models here
{% if cookiecutter.use_sqlmodel == "y" %}
from sqlmodel import SQLModel
from app.models.base import Base
{% endif %} 