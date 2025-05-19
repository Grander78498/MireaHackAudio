from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from dependencies import get_current_user
from models import User


router = APIRouter(prefix='auth')


@router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    pass


@router.get('/me')
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user