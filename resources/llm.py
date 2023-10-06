from pydantic import BaseModel

class llm_ask(BaseModel):
    question: str
