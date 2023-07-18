from flask import Flask, jsonify
from flask_smorest import Api
from Project.routers import LoginBluePrint, RegisterBlueprint, TemplateBluePrint
from flask_jwt_extended import JWTManager
import os


app = Flask(__name__)
app.config['API_TITLE'] = 'Python Test'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.2'
api = Api(app)
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )
@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401,
    )

# Which will be called at the time of token creation
# we can call the db and set the roles or other information if needed
@jwt.additional_claims_loader  
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
)

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )
api.register_blueprint(LoginBluePrint)
api.register_blueprint(RegisterBlueprint)
api.register_blueprint(TemplateBluePrint)
    # return app

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")