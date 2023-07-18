from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from ..schemas import TempalateSchema
from ..services.mongo_db import MongoService
from flask import request

blp_template = Blueprint('Template', __name__, description="Tempaltes Operation")

@blp_template.route("/template")
class TemplateController(MethodView):
    @jwt_required()
    @blp_template.arguments(TempalateSchema)
    def put(self, input_body):
        try:
            result = MongoService(database="pythonTest", collection="Template").insert_data(input_body)
            return({"message":"New Template has been inserted Successfully", "Your Template Id is":str(result.inserted_id)},200)
        except Exception as ex :
            return({"message" : "Error_in_Inserting New Template"}, 500)
    @jwt_required()
    def get(self):
        try:
            result = MongoService(database="pythonTest", collection="Template").get_data(single=False)
            return({"Templates":result},200)
        except Exception as ex :
            return({"message" : "Error_in_Get All Template"}, 500)

@blp_template.route("/template/<string:template_id>")
class TemplateManipulationController(MethodView):
    @jwt_required()
    def put(self,template_id):
        try:
            result = MongoService(database="pythonTest", collection="Template").update_data(template_id, request.json)   
            return {"Message":"Template Updated Successfully"}
        except Exception as ex :
            return({"message" : "Error_in_Update Single Template"}, 500)
    
    @jwt_required()
    def get(self,template_id):
        try:
            result = MongoService(database="pythonTest", collection="Template").get_data(single=True, template_id=template_id)   
            return (result, 200)
        except Exception as ex :
            return({"message" : "Error_in_Update Single Template"}, 500)

    @jwt_required()
    def delete(self,template_id):
        try:
            result = MongoService(database="pythonTest", collection="Template").delete_template_by_id(document_id=template_id)   
            return ({"Message": "The Tempalte has been deleted successfully"}, 200)
        except Exception as ex :
            return({"message" : "Error_in_DELETE Single Template"}, 500)