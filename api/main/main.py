from flask import Blueprint, render_template, jsonify, request,redirect
from api.database.database import MyMongoDB
from uuid import uuid4
from flask_wtf.csrf import CSRFProtect
from bson import ObjectId

main = Blueprint('main', __name__,
                 template_folder= 'templates',)

csrf = CSRFProtect()

@main.route("/main", methods=['GET', 'POST', 'PUT', 'DELETE'])
@csrf.exempt
def user_handler():
    mongo = MyMongoDB()
    collection = mongo.connect_to_collection("customer_list")

    try:
        if request.method == 'POST':

            if request.form:
                content = request.form.to_dict()
            else:
                content = request.get_json()

            if not content:
                return jsonify({"message": "Invalid input"}), 400
            content["_id"] = uuid4().hex
            collection.insert_one(content)

            if request.form:
                return redirect("/main")

            return jsonify({"message": "User added", "id": content["_id"]}), 201

        elif request.method == 'GET':
            users = collection.find({}, {'_id': 1, 'Contact Person': 1, 'Email': 1, 'Phone': 1, 'Address': 1})
            result = []
            for user in users:
                user['_id'] = str(user['_id'])
                user['Contact Person'] = user.get('Contact Person','None')
                user['Email'] = user.get('Email','None')
                user['Phone'] = user.get('Phone','None')
                user['Address'] = user.get('Address','None')

                result.append(user)
            return render_template('main.html', users=result)
        

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
            
            return redirect("/main")
        

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
            
            return redirect("/main")
        

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500