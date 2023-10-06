from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from fastapi.security import (
    OAuth2PasswordRequestForm,
)

from services.storage import (
    login as login_service,
    get_files,
)
from services.auth import (
    create_access_token, 
    oauth2_scheme,
    get_current_user,
)

from sql_app.schemas import FileBase

router = APIRouter()

@router.post('/token/', status_code=200)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        user = login_service(
            form_data.username,
            form_data.password
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    token = create_access_token(
        data=dict(
            email=user.email,
        )
    )
    return dict(
        access_token=token,
        token_type="bearer"
    )

@router.get('/files/', status_code=200,
            response_model=list[FileBase],
            dependencies=[
                Depends(oauth2_scheme),
            ])
async def see_user_files(user = Depends(get_current_user)):
    """
        get the files from the current user
    """
    return get_files(user.id)
