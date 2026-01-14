from fastapi import APIRouter, HTTPException, Depends, status
from app.user.user_schema import User, UserLogin, UserUpdate, UserDeleteRequest
from app.user.user_service import UserService
from app.dependencies import get_user_service
from app.responses.base_response import BaseResponse

user = APIRouter(prefix="/api/user")


@user.post("/login", response_model=BaseResponse[User], status_code=status.HTTP_200_OK)
def login_user(user_login: UserLogin, service: UserService = Depends(get_user_service)) -> BaseResponse[User]:
    try:
        user = service.login(user_login)
        return BaseResponse(status="success", data=user, message="Login Success.") 
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user.post("/register", response_model=BaseResponse[User], status_code=status.HTTP_201_CREATED)
def register_user(user: User, service: UserService = Depends(get_user_service)) -> BaseResponse[User]:
    """
    Register a new user.

    This endpoint creates a new user with the given information.
    If a user with the same email already exists, an error is raised.
    
    :param user: User information for registration.
    :type user: User
    :param service: User service dependency.
    :type service: UserService
    :return: A response containing the registered user information.
    :rtype: Any
    """
    ## TODO
    try:
        new_user = service.register_user(user)
        return BaseResponse(status="success", data=new_user, message="User registration success.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user.delete("/delete", response_model=BaseResponse[User], status_code=status.HTTP_200_OK)
def delete_user(user_delete_request: UserDeleteRequest, service: UserService = Depends(get_user_service)) -> BaseResponse[User]:
    """
    Delete an existing user.

    This endpoint deletes a user identified by the given email address.
    If the user does not exist, an error is raised.
    
    :param user_delete_request: Request body containing the user's email.
    :type user_delete_request: UserDeleteRequest
    :param service: User service dependency.
    :type service: UserService
    :return: A response containing the deleted user information.
    :rtype: Any
    """
    ## TODO
    try:
        user = service.delete_user(user_delete_request.email)
        return BaseResponse(status="success", data=user, message="User Deletion Success.")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@user.put("/update-password", response_model=BaseResponse[User], status_code=status.HTTP_200_OK)
def update_user_password(user_update: UserUpdate, service: UserService = Depends(get_user_service)) -> BaseResponse[User]:
    """
    Update a user's password.

    This endpoint updates the password of an existing user identified by email.
    If the user does not exist, an error is raised.
    
    :param user_update: Request body containing the user's email and new password.
    :type user_update: UserUpdate
    :param service: User service dependency.
    :type service: UserService
    :return: A response containing the updated user information.
    :rtype: Any
    """
    ## TODO
    try:
        user = service.update_user_pwd(user_update)
        return BaseResponse(status="success", data=user, message="User password update success.")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))