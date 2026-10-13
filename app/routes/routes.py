from flask import Blueprint, jsonify, request

new_routes = Blueprint("new_routes",__name__)


@new_routes.route("/new",methods=["GET"])
def get():
  id = request.args.get("id")
  user_list = [{
    "id":1,
    "name":"Hirdesh",
    "role":"admin",
  },
  {
    "id":2,
    "name":"Sneha",
    "role":"emp",
  },
  {
    "id":3,
    "name":"Ashwini",
    "role":"admin",
  }

  ]

  users_list= user_list

  if id:
    id=int(id)
    users_list = [u for u in user_list if u["id"] == id]
  return jsonify({"users":users_list})


@new_routes.route("/zip",methods=["POST"])
def zip_user():
  users = ["Hirdesh","Rahul","Amit"]
  scores = [84,74,69]
  result = []
  for user, score in zip(users,scores):
   result.append([user,score])

  return jsonify({"status":"success","userArr":result})


@new_routes.route("/list",methods=["POST"])
def list_comp():
  numbers = [1,2,3,4,5]
  return [str(number) for number in numbers]
  