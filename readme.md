### Automatic data abstration tool

A simple llm-base tool to fastrack specific information extraction
from PDF documents. 
The provided tool offers users the possibility to build their
questoinnaires in natural language to drive the information
extraction process based on llama2-7b.

Python version : 11

Alembic:
add versions dir: backend/alembic/versions/
generate migrations: alembic revision --autogenerate -m "db initialization"
run migrations : alembic upgrade head
