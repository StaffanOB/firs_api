import requests, os
from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)

from db import db
from models import UserModel
from schemas import UserSchema, UserRegisterSchema
from blocklist import BLOCKLIST
from tasks import send_user_registration_email


blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    """
    Register new users
    """
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        """
        Regiser a new user and add it to the database

        Parameters:
            user_data (dict): Username and password

        Returns:
            user (UserModel): username and a hashed password


        # TODO: <20-10-23, sob> #
                * Change password hash to bcrypt hash
        """
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == user_data["email"]
                )).first():
            abort(410, message=f"A user with that username ({user_data['username']}) already exists.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        # Send register email
        current_app.queue.enqueue(send_user_registration_email, user.email, user.username)

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    """
    User login class for handeling user logins
    """
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """
        Check users credentials

        Parameters:
            user_data (dict): Username and password

        Returns:
            access_token (str): Generated access token from pbkdf2_sha256
            function.
        """

        # Check if user exists in database
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        # Check if users password maches with the stored hash
        # if it maches return a access token
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)

        # Make it clear that when to add the refresh token to the blocklist
        # will depend on the app designe
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    User route
    """
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """
        Get user by route ID

        Parameters:
            user_id (int): User database id

        Returns:
            user: User Object (json)
        """
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"message": "User was deleted"}


# TODO: Remove all users that dont start with test
@blp.route("/users")
class ListUsers(MethodView):
    """ Lists all test user on the system """
    @blp.response(200, UserSchema(many=True))
    def get(self):
        test_user_list = [test_user for test_user in UserModel.query.all() if str(test_user.username).startswith("test_") ]
        #test_user_list = [test_user for test_user in UserModel.query.all() if str(test_user.username).startswith("") ]
        return test_user_list

    #@jwt_required(fresh=True)
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)

    def post(self, user_data):
        user = UserSchema(**user_data)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting in to users")

        return user
