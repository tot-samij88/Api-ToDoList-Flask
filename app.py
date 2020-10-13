from flask import Flask
from flask_restful import Resource, Api, reqparse
from datetime import datetime


app = Flask(__name__)
api = Api(app)


TODOLIST = {
    '1': {'date_create': str(datetime.utcnow()), 'text': 'ABra', 'date_modificated': str(datetime.utcnow()), 'done': False},
    '2': {'date_create': str(datetime.utcnow()), 'text': 'Kadab', 'date_modificated': str(datetime.utcnow()), 'done': False},
    '3': {'date_create': str(datetime.utcnow()), 'text': 'Rabarf', 'date_modificated': str(datetime.utcnow()), 'done': False},
    '4': {'date_create': str(datetime.utcnow()), 'text': 'vendoring', 'date_modificated': str(datetime.utcnow()), 'done': False},
    '5': {'date_create': str(datetime.utcnow()), 'text': 'pirsing', 'date_modificated': str(datetime.utcnow()), 'done': False},
}


parser = reqparse.RequestParser()


class ToDoList(Resource):
    def get(self):
        return TODOLIST

    def post(self):
        parser.add_argument("date_create", str(datetime.utcnow()))
        parser.add_argument("text")
        parser.add_argument("date_modificated", str(datetime.utcnow()))
        parser.add_argument("done", type=bool, default=False)
        args = parser.parse_args()
        todo_id = int(max(TODOLIST.keys()))+1
        todo_id = '%i' % todo_id
        TODOLIST[todo_id] = {
            "date_create": args["date_create"],
            "text": args["text"],
            "date_modificated": args["date_modificated"],
            "done": args["done"]
        }
        return TODOLIST[todo_id], 201


class ToDo(Resource):
    def get(self, todo_id):
        if todo_id not in TODOLIST:
            return "Not Found", 404
        else:
            return TODOLIST[todo_id]

    def put(self, todo_id):
        parser.add_argument("text")
        parser.add_argument("date_modificated", str(datetime.utcnow()))
        parser.add_argument("done", type=bool)
        args = parser.parse_args()
        if todo_id not in TODOLIST:
            return "Record not found", 404
        else:
            todo_list = TODOLIST[todo_id]
            todo_list["text"] = args["text"] if args["text"] is not None else todo_list["text"]
            todo_list["date_modificated"] = args["date_modificated"] if args["date_modificated"] is not None else todo_list["date_modificated"]
            todo_list["done"] = args["done"] if args["done"] is not None else todo_list["done"]
            return todo_list, 200

    def delete(self, todo_id):
        if todo_id not in TODOLIST:
            return "Not Found", 404
        else:
            del TODOLIST[todo_id]
            return '', 204


api.add_resource(ToDoList, '/todolist/')
api.add_resource(ToDo, '/todolist/<todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
