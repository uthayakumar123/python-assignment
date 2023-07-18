from flask_smorest import Blueprint
from flask.views import MethodView
from ..schemas import RegisterSchema
from flask_jwt_extended import jwt_required
from ..services import mongo_db

blp_register = Blueprint('Register', __name__, description="user register")

@blp_register.route("/register")
class Login(MethodView):
    @blp_register.arguments(RegisterSchema)
    def post(self,input_body):
        try:
            result = mongo_db.MongoService(database="pythonTest", collection="Login").insert_data(input_body)
            return({"message":"User has been Registered Successfully"},200)
        except Exception as ex :
            return({"message" : "Error in Registering User"}, 500)