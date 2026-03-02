from pydantic import BaseModel


class MessageDTO(BaseModel):
    user_id: int
    matching_user_id: int
    message: str
