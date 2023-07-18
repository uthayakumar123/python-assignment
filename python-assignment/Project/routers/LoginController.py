from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from ..schemas import LoginSchema
from flask_jwt_extended import create_access_token
import datetime
from ..services import mongo_db


blp_login = Blueprint('login', __name__, description="Login")

@blp_login.route("/Login")
class Login(MethodView):
    @blp_login.arguments(LoginSchema)
    def post(self,input_body):
        '''Authenticate user with username and password  If authentication is successful, return JWT token'''
        try:
            login_flag = False
            collection_data = mongo_db.MongoService(database="pythonTest", collection="Login").get_data(single=False)
            print(collection_data)
            jwtToken = create_access_token(identity = input_body["email"], fresh = True,expires_delta = datetime.timedelta(minutes=600))
            for i in collection_data:
                if input_body["email"] == i["email"]:
                    if input_body["password"] == i["password"]:
                        login_flag = True
                        return ({"message":"Login Successful","jwt_token":"Bearer"+" "+jwtToken},200)
            if not login_flag:
                return({"message":"invalid credentials"},212)
        except Exception as ex :
            print("Error_in_Login ",ex)
            return({"message" : f"Something went wrong. Please contact Administrator {ex}"}, 500)