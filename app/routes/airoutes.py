import asyncio
from flask import Blueprint,request,jsonify
from app.services.aiservice import GeminiServices
from app.database.mongodb import db


ai_routes = Blueprint("ai_routes",__name__)

prompt_collection = db["prompt"]
history_collection = db["history"]
gemini_service = GeminiServices()

DEFAULT_PROMPT = {
  "_id":"Education_Prompt",
  "template":"You are an expert in education domain. Answer the following: {{userInput}}" 
}

@ai_routes.route("/ask",methods=["POST"])
def ask():
  data = request.json
  user_input = data.get('userinput') 
  if not user_input:
    return jsonify({"error":"userinput field is required"}),400

  prompt_doc = prompt_collection.find_one_and_update(
    {"_id":"Education_Prompt"},
    {"$setOnInsert":DEFAULT_PROMPT},
    upsert=True,
    return_document=True,
  )

  final_prompt = prompt_doc["template"].replace("{{userInput}}",user_input)

  try:
    ai_response = gemini_service.generate_text(final_prompt)
  except RuntimeError as e:
      return jsonify({"status":"error","error":str(e)}),502


  history_doc = {
    "userInput":user_input,
    "response":ai_response,
  }

  result = history_collection.insert_one(history_doc)

  return jsonify({
    "status":"success",
    "response":ai_response,
    "log_id":str(result.inserted_id)
  }),200
  


  


@ai_routes.route("/ask-bulk",methods=["POST"])
def ask_bulk():
  data = request.json
  user_inputs = data.get("userinputs")
  if not user_inputs:
    return jsonify({"error":"userinputs field is required"}),400

  prompt_doc = prompt_collection.find_one_and_update(
    {"_id":"Education_Prompt"},
    {"$setOnInsert":DEFAULT_PROMPT},
    upsert=True,
    return_document=True,
  )

  template = prompt_doc["template"]

  async def process_all():
    tasks = [gemini_service.genearate_text_async(template.replace("{{userInput}}",ui)) for ui in user_inputs
    ]
    return await asyncio.gather(*tasks,return_exceptions=True)

  ai_response = asyncio.run(process_all())

  history_docs = []
  result = []

  for ui, resp in zip(user_inputs,ai_response):
    if isinstance(resp,Exception):
      result.append({"userInput":ui,"status":"error","error":str(resp)})
    else:
      history_docs.append({"userI nput":ui,"response":resp})
      result.append({"userInput":ui,"status":"success","response":resp}) if history_docs else None

  results = history_collection.insert_many(history_docs)

  return jsonify({
    "status":"success",
    "response":ai_response,
    "log_id":[str(_id) for _id in results.inserted_ids] if result else []
  }),200


@ai_routes.route("/get_all",methods=["GET"])
def get_all():
  histories = list(history_collection.find())
  for history in histories:
    history["_id"] = str(history["_id"])

  return jsonify({
    "histories":histories
  }),200