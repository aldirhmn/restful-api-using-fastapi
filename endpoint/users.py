from fastapi import APIRouter
from models.request import UsersRequest, UsersUpdateRequest
from models.response import Response
from models.models import users
from db.database import Database
from sqlalchemy import and_, desc

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404:{"description": "Not Found"}}
)

database = Database()
engine = database.get_db_connection()

@router.post("/create", response_description="New Users added into the Database")
async def add_users(users_req: UsersRequest):
    new_users = users()
    new_users.username = users_req.username
    new_users.firstName = users_req.firstName
    new_users.lastName = users_req.lastName
    new_users.email = users_req.email
    new_users.password = users_req.password
    new_users.phoneNumber = users_req.phoneNumber
    new_users.address = users_req.address
    new_users.id = None
    session = database.get_db_session(engine)
    session.add(new_users)
    session.flush()
    #GET ID OF THE INSERTED PRODUCT
    session.refresh(new_users, attribute_names=['id'])
    data = {"users_id": new_users.id}
    session.commit()
    session.close()
    return Response(data, 200, "New User Added Successfully", False)

@router.put("/update")
async def update_users(users_update_req : UsersUpdateRequest):
    users_id = users_update_req.users_id
    session = database.get_db_session(engine)
    try:
        is_users_updated = session.query(users).filter(users.id == users_id).update({
            users.username: users_update_req.username,
            users.firstName: users_update_req.firstName,
            users.lastName: users_update_req.lastName,
            users.email: users_update_req.email,
            users.password: users_update_req.password,
            users.phoneNumber: users_update_req.phoneNumber,
            users.address: users_update_req.address
        }, synchronize_session = False)
        session.flush()
        session.commit()
        response_msg = "Users Updated Successfully"
        response_code = 200
        error = False
        if is_users_updated == 1:
            data = session.query(users).filter(
                users.id == users_id).one()
        elif is_users_updated == 0:
            response_msg = "Users Not Updated. No Users Found With this ID :" + \
                str(users_id)
            error = True
            data = None
        return Response(data, response_code,response_msg, error)
    except Exception as e:
        print("Error : ", e)

@router.delete("/{users_id}/delete")
async def delete_users(users_id: str):
    session = database.get_db_session(engine)
    try:
        is_users_updated = session.query(users).filter(and_(users.id == users_id, users.deleted == False)).update({
            users.deleted: True}, synchronize_session = False)
        session.flush()
        session.commit()
        response_msg = "User Deleted Successfully"
        response_code = 200
        error = False
        data = {"users_id": users_id}
        if is_users_updated == 0:
            response_msg = "User Not Deleted. No Users Found with this ID : " + \
                str(users_id)
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as e:
        print("Error : ", e)

@router.get("/{users_id}")
async def read_users(users_id: str):
    session = database.get_db_session(engine)
    response_message = "Users Retrived Successfully"
    data = None
    try:
        data = session.query(users).filter(and_(users.id == users_id, users.deleted == False)).one()
    except Exception as ex :
        print("Error : ", ex)
        response_message = "Users Not Found"
    error = False
    return Response(data, 200, response_message, error)

@router.get("/")
async def read_all_users(username: str, page_size: int, page: int):
    session = database.get_db_session(engine)
    data = session.query(users).filter(and_(users.username == username, users.deleted == False)).order_by(
        desc(users.username)).limit(page_size).offset((page-1)*page_size).all()
    return Response(data, 200, "Users Retrived Successfully", False)