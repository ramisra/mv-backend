import uuid
from typing import Optional

from black import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlmodel import Session
from starlette.responses import JSONResponse

from core.crud.job import JobCrud
from core.crud.user import UserCrud
from core.database import get_db_session
from core.models.job import JobRead
from core.models.user import User, UserCreate, UserRead, UserUpdate
from core.services.auth import AuthService

router = APIRouter()


@router.get("/users/{user_id}", response_model=UserRead, dependencies=[Depends(AuthService().is_user_logged_in)])
def get_single_user(user_id: uuid.UUID, db: Session = Depends(get_db_session)):
    user = UserCrud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users", response_model=Page[UserRead],  dependencies=[Depends(AuthService().is_user_logged_in)])
def get_all_users(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db_session)
):
    return paginate(UserCrud.get_users(db, skip=skip, limit=limit))


@router.post("/users", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db_session)):
    try:
        created_user = UserCrud.create_user(db, user)
        user_token = AuthService().generate_token(claims={'email': created_user.email, 'id': str(created_user.id), 'name': created_user.name})
        updated = UserCrud.update_user(db, created_user, UserUpdate(user_token=user_token))
        return updated
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "msg": f"Failed to create users: {str(e)}",
            },
            status_code=500,
        )


@router.put("/users/{user_id}", response_model=User,  dependencies=[Depends(AuthService().is_user_logged_in)])
def update_existing_user(
    user_id: uuid.UUID, updated_user: UserUpdate, db: Session = Depends(get_db_session)
):
    user = UserCrud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        updated = UserCrud.update_user(db, user, updated_user)
        return updated
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "msg": f"Failed to update users: {str(e)}",
            },
            status_code=500,
        )


@router.delete("/users/{user_id}", response_model=User,  dependencies=[Depends(AuthService().is_user_logged_in)])
def delete_existing_user(user_id: uuid.UUID, db: Session = Depends(get_db_session)):
    user = UserCrud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        deleted = UserCrud.delete_user(db, user_id)
        return deleted
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "msg": f"Failed to delete users: {str(e)}",
            },
            status_code=500,
        )


# @router.post("/users/{user_id}/jobs", response_model=JobRead)
# def create_job_for_authenticated_user(
#     job_create_instance: JobCreate,
#     db: Session = Depends(get_db_session),
# ):
#     try:
#         return JobCrud.create_job(db, job_create_instance)
#     except Exception as e:
#         return JSONResponse(
#             content={
#                 "status": "error",
#                 "msg": f"Failed to submit job: {str(e)}",
#             },
#             status_code=500,
#         )
#
#
@router.get(
    "/users/{user_id}/videos", response_model=List[JobRead]
)
def get_user_job(
        db: Session = Depends(get_db_session),
        current_user: Optional[User] = Depends(AuthService().get_current_user),
):
    try:
        job = JobCrud.get_user_jobs(db, current_user)
        return job
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "msg": f"Failed to create users: {str(e)}",
            },
            status_code=500,
        )
