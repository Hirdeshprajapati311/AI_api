from flask import Blueprint,request,jsonify
from app.database.mongodb import db


ai_new_routes = Blueprint("ai_new_routes",__name__)

prompt_collection = db["prompt"]



@ai_new_routes.route("/prompt",methods=["GET"])
def get_prompt():
  prompt_id = request.args.get("id")
  if not prompt_id:
    return jsonify({"error":"cannot find the declared ID"}),400

  prompt = prompt_collection.find_one_and_update({"_id":prompt_id})

  if not prompt:
    return jsonify({"error":"Prompt not found"}),400

  return jsonify(prompt),200


@ai_new_routes.route("/prompt",methods=["PUT"])
def upsert_prompt():
  prompt_id = request.args.get("id")
  if not prompt_id:
    return jsonify({"error":"cannot find the id"}),400

  prompt = prompt_collection.find_one_and_update

  

  
