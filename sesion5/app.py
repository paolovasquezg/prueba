#imports
import sys
from crypt import methods
from flask import (
    Flask,
    abort,
    jsonify, 
    render_template, 
    request,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/todoapp10'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#models
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable = False, default = False)

    def __repr__(self):
        return f'Todo: id={self.id}, description={self.description}'

#db.create_all()

#controller
@app.route('/', methods=['GET'])
def index():
    return render_template('index2.html', data=Todo.query.all())

@app.route('/todos/create_post', methods=['POST'])
def create_todo():
    error = False
    response = {}
    try:
        description = request.get_json()['description']
        id = request.get_json()['id']
        todo = Todo(id=id,description=description)
        db.session.add(todo)
        db.session.commit()
        response['id'] = id
        response['description'] = description
    except Exception as e:
        error = True
        print(e)
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify(response)

@app.route('/todos/create_get', methods=['GET'])
def create_todo_get():
    try:
        description = request.args.get('description', '')
        todo = Todo(description2=description)
        db.session.add(todo)
        db.session.commit()
    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


#run
if __name__ == '__main__':
    app.run(debug=True, port=5001)