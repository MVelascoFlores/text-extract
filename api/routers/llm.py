from fastapi import (
    APIRouter,
    UploadFile,
    HTTPException,
    Depends,
)

from services.llm import (
    load_file,
    ask,
)
from services.storage import (
    create_file,
    is_file_from_user,
)
from services.auth import (
    oauth2_scheme,
    get_current_user,
)

from sql_app import schemas

from resources.llm import llm_ask


router = APIRouter()


@router.post('/upload-file/',
             dependencies=[
                 Depends(oauth2_scheme),
             ])
async def upload_file(file: UploadFile, 
                      user=Depends(get_current_user)):
    """
        Upload the file to extract information
    """
    try:
        path, file_name = await load_file(file)
        file_object: schemas.File  = create_file(
            file_name, path, user.id
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    return {
        'message':'File readed and stored',
        'data':{
            'id':file_object.id
        }
    }

@router.post('/file/{id}/',
             status_code=200,
             dependencies=[
                 Depends(oauth2_scheme),
             ])
async def ask_file(data: llm_ask, id:int, user=Depends(get_current_user)):
    """
        ask information about a file
    """
    file = is_file_from_user(user.id, id)
    if file is None:
        raise HTTPException(
            status_code=400,
            detail='The file it\'s from another user',
        )
    response = ask(file.index_path, data.question)
    # create history from file
    return {
        'data':{
            'message': response
        }
    }
    