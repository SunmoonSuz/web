from ..models import UserMan
from .model_operation import take_object

def access(hash: str, user_id: int):
    try:
        curr_user = take_object(UserMan, user_id, None)
    except Exception as e:
        raise e
    password = curr_user.password
    if hash == password[-16::]:
        return None
    else:
        raise ValueError("hash is not correct")