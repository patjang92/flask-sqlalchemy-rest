from flask import Flask, make_response, jsonify, request
import dataset

app = Flask(__name__)
db = dataset.connect('sqlite:///api.db')

'''
Examples:
GET request to /api/books returns the details of all books
POST request to /api/books creates a book with the ID 3 (As per request body)

Sample request body -
{
        "id": "1",
        "name": "A Game of Thrones",
        "author": "George R. R. Martin"
}

GET request to /api/books/3 returns the details of book 3
PUT request to /api/books/3 to update fields of book 3
DELETE request to /api/books/3 deletes book 3

'''

# table = db['books']

def _get_table(db):
  return db.create_table('books', primary_id='id', primary_type=db.types.integer)

# def fetch_db(id):  # Each book scnerio
#     return table.find_one(id=id)

def get_each_book_response(id, success_response_code=200, failure_response_code=404):
  book_obj = _get_table(db).find_one(id = id)
  
  if book_obj:
    return make_response(jsonify(book_obj), success_response_code)
  else:
    return make_response(jsonify(book_obj), failure_response_code)


def fetch_db_all():
  books = []
  for book in _get_table(db):
    books.append(book)
  return books


@app.route('/api/db_populate', methods=['POST'])
def db_populate():
  table = db['books']

  data = {
    "id": "1",
    "name": "A Game of Thrones.",
    "author": "George R. R. Martin"
  }
  
  table.insert_ignore(data, ['id'])

  data = {
    "id": "2",
    "name": "Lord of the Rings",
    "author": "J. R. R. Tolkien"
  }
  
  table.insert_ignore(data, ['id'])

  return make_response("", 201)


@app.route('/api/books', methods=['GET', 'POST'])
def api_books():
  if request.method == "GET":
    return make_response(jsonify(fetch_db_all()), 200)
  elif request.method == 'POST':
    content = request.json
    id = content['id']
    _get_table(db).insert(content)
    return get_each_book_response(id, success_response_code=201)  # 201 = Created


@app.route('/api/books/<id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_book(id):
  if request.method == "GET":
    return get_each_book_response(id)
  elif request.method == "PUT":  # Updates the book
    content = request.json
    _get_table(db).update(content, ['id'])
    return make_response("", 204)
  elif request.method == "DELETE":
    _get_table(db).delete(id=id)
    return make_response("", 204)


if __name__ == '__main__':
  app.run(debug=True)