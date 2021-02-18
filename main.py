from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

Notes = {
    'MyNote1': {'MyNote1': 'Do this'},
    'MyNote2': {'MyNote2': 'Do that'},
    'MyNote3': {'MyNote3': 'Do all'},
}


def abort_if_note_doesnt_exist(note_id):
    if note_id not in Notes:
        abort(404, message="Note {} doesn't exist".format(note_id))



parser = reqparse.RequestParser()
parser.add_argument('title')


class Note(Resource):
    def get(self, note_id):
        abort_if_note_doesnt_exist(note_id)
        return Notes[note_id]

    def delete(self, note_id):
        abort_if_note_doesnt_exist(note_id)
        del Notes[note_id]
        return '', 204

    def put(self, note_id):
        args = parser.parse_args()
        task = {note_id: args['title']}
        Notes[note_id] = task
        return task, 201


class NoteList(Resource):
    def get(self):
        return Notes

    def post(self):
        args = parser.parse_args()
        # note_id = int(max(Notes.keys()).lstrip('note')) + 1
        note_id = len(Notes) + 1
        note_id = 'note%i' % note_id
        Notes[note_id] = {note_id: args['title']}
        return note_id, 201


api.add_resource(NoteList, '/notes')
api.add_resource(Note, '/notes/<note_id>')


if __name__ == '__main__':
    app.run(debug=True)
