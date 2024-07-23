import flask_bcrypt
import pydantic
from flask import Flask, Response, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from models import Session, User, Adv
from schema import CreateUser, Schema_user, UpdateUser, CreateAdv, UpdateAdv, Schema_adv, RelAdv, RelUser

app = Flask("app")
# bcrypt = flask_bcrypt.Bcrypt(app)


# def hash_password(password: str) -> str:
#     password = password.encode()
#     password = bcrypt.generate_password_hash(password)
#     password = password.decode()
#     return password
#
#
# def check_password(hashed_password: str, password: str) -> bool:
#     hashed_password = hashed_password.encode()
#     password = password.encode()
#     return bcrypt.check_password_hash(hashed_password, password)


class HttpError(Exception):

    def __init__(self, status_code: int, error_message: str | dict):
        self.status_code = status_code
        self.error_message = error_message


def validate(schema_cls: Schema_user | Schema_adv, json_data: dict):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as err:
        error = err.errors()[0]
        error.pop("ctx", None)
        raise HttpError(409, error)


@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    json_response = jsonify({"error": err.error_message})
    json_response.status_code = err.status_code
    return json_response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: Response):
    request.session.close()
    return response


def get_user(user_id):
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user

def get_adv(adv_id):
    adv = request.session.get(Adv, adv_id)
    if adv is None:
        raise HttpError(404, "advertisement not found")
    return adv

def add_user(user: User):
    request.session.add(user)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(400, "user already exists")
    return user

def add_adv(adv: Adv):
    request.session.add(adv)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(400, "advertisement already exists")
    return adv

class UserView(MethodView):

    @property
    def session(self) -> Session:
        return request.session

    def get(self, user_id):
        user = get_user(user_id)
        return jsonify(user.json)

    def post(self):
        json_data = validate(CreateUser, request.json)
        # json_data["password"] = hash_password(json_data["password"])
        user = add_user(User(**json_data))
        return jsonify(user.json)

    def patch(self, user_id):
        json_data = validate(UpdateUser, request.json)
        # if "password" in json_data:
        #     json_data["password"] = hash_password(json_data["password"])
        user = get_user(user_id)
        for field, value in json_data.items():
            setattr(user, field, value)
        user = add_user(user)
        return jsonify(user.json)

    def delete(self, user_id):
        user = get_user(user_id)
        self.session.delete(user)
        self.session.commit()
        return jsonify({"status": "deleted"})

class AdvView(MethodView):
    @property
    def session(self) -> Session:
        return request.session

    def get(self, adv_id):
        adv = get_adv(adv_id)
        return jsonify(adv.json)

    def post(self):
        json_data = validate(CreateAdv, request.json)
        adv = Adv(**json_data)
        return jsonify(adv.json)

    def patch(self, adv_id):
        json_data = validate(UpdateAdv, request.json)
        adv = get_adv(adv_id)
        for field, value in json_data.items():
            setattr(adv, field, value)
        adv = add_adv(adv)
        return jsonify(adv.json)

    def delete(self, adv_id):
        adv = get_adv(adv_id)
        self.session.delete(adv)
        self.session.commit()
        return jsonify({"status": "deleted"})

user_view = UserView.as_view("user")
adv_view = AdvView.as_view("adv")

app.add_url_rule("/user/", view_func=user_view, methods=["POST"])
app.add_url_rule(
    "/user/<int:user_id>/", view_func=user_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule("/adv/", view_func=adv_view, methods=["POST"])
app.add_url_rule(
    "/adv/<int:adv_id>/", view_func=adv_view, methods=["GET", "PATCH", "DELETE"]
)
app.run()
