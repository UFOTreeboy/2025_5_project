from flask import Blueprint, render_template, jsonify, request
from api.database.database import MyMongoDB
from uuid import uuid4
from flask_wtf.csrf import CSRFProtect
from bson import ObjectId

main = Blueprint('main', __name__)
csrf = CSRFProtect()

@main.route("/main", methods=['GET'])
def render_main_html():
    return render_template('main.html')

@main.route("/user", methods=['GET', 'POST', 'PUT', 'DELETE'])
@csrf.exempt
def user_handler():
    mongo = MyMongoDB()
    collection = mongo.connect_to_collection("customer_list")


    try:
        if request.method == 'POST':
            content = request.get_json()
            if not content:
                return jsonify({"message": "Invalid input"}), 400
            content["_id"] = uuid4().hex
            collection.insert_one(content)
            return jsonify({"message": "User added", "id": content["_id"]}), 201


        elif request.method == 'GET':
            users = collection.find({}, {'_id': 1, 'Contact Person': 1, 'Email': 1, 'Phone': 1, 'Address': 1})
            result = []
            for user in users:
                user['_id'] = str(user['_id'])
                user['Contact Person'] = user.get('Contact Person')
                user['Email'] = user.get('Email')
                user['Phone'] = user.get('Phone')
                user['Address'] = user.get('Address')

                result.append(user)
            return jsonify({"data": result}), 200
        

        elif request.method == 'PUT':
            content = request.get_json()
            user_id = content.get("_id")
            if not user_id:
                return jsonify({"message": "Missing '_id'"}), 400
            try:
                user_id = ObjectId(user_id)
            except Exception:
                return jsonify({"message": "Invalid '_id' format"}), 400
            update_data = {k: v for k, v in content.items() if k != "_id"}
            if not update_data:
                return jsonify({"message": "No fields to update"}), 400
            result = collection.update_one({"_id": user_id}, {"$set": update_data})
            if result.matched_count == 0:
                return jsonify({"message": "User not found"}), 404
            return jsonify({"message": "User updated"}), 200
        

        elif request.method == 'DELETE':
            content = request.get_json()
            user_id = content.get("_id")
            if not user_id:
                return jsonify({"message": "Missing '_id'"}), 400
            try:
                user_id = ObjectId(user_id)
            except Exception:
                return jsonify({"message": "Invalid '_id' format"}), 400
            result = collection.delete_one({"_id": user_id})
            if result.deleted_count == 0:
                return jsonify({"message": "User not found"}), 404
            return jsonify({"message": "User deleted"}), 200
        

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500