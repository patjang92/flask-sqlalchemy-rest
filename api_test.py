import unittest
import requests 

def addTwoNumbers(a,b):
  return a + b

class AddTest(unittest.TestCase):
  def test1(self):
    c = addTwoNumbers(5, 10)
    self.assertEqual(c, 15)
    
  def test2(self):
    c = addTwoNumbers(5, 10)
    self.assertNotEqual(c, 10)
    
    
class ApiTest(unittest.TestCase):
  API_URL = "http://127.0.0.1:5000/api"
  BOOKS_URL = "{}/books".format(API_URL)
  BOOK_OBJ = {
    "id": 3,
    "name": "Harry Potter and Philosopher Stone",
    "author": "J. K. Rowling"
  }
  NEW_BOOK_OBJ = {
    "id": 3,
    "name": "The Alchemist",
    "author": "Paulo Coelho"    
  }
  
  def _get_each_book_url(self, id):
    return "{}/{}".format(ApiTest.BOOKS_URL, id)
  
  # Get request to /api/books returns the details of all books
  @unittest.skip("skip this")
  def test_1_get_all_books(self):
    r = requests.get(ApiTest.BOOKS_URL)
    self.assertEqual(r.status_code, 200)
    self.assertEqual(len(r.json()), 2)
  
  def test_2_add_new_books(self):
    r = requests.post(ApiTest.BOOKS_URL, json=ApiTest.BOOK_OBJ)
    self.assertEqual(r.status_code, 201)
    
  def test_3_get_new_book(self):
    id = 3
    r = requests.get("{}/{}".format(ApiTest.BOOKS_URL, id))
    self.assertEqual(r.status_code, 200)
    self.assertDictEqual(r.json(), ApiTest.BOOK_OBJ)
    
  def test_4_update_existing_book(self):
    id = 3
    r = requests.put("{}/{}".format(ApiTest.BOOKS_URL, id), json=ApiTest.NEW_BOOK_OBJ)
    self.assertEqual(r.status_code, 204)
    
  def test_5_get_new_book_after_update(self):
    id = 3
    r = requests.put(self._get_each_book_url(id))
    self.assertEqual(r.status_code, 200)    
    self.assertDictEqual(r.json(), ApiTest.NEW_BOOK_OBJ)
    
  def test_6_delete_book(self):
    id = 3
    r = requests.delete(self._get_each_book_url(id))
    self.assertEqual(r.status_code, 204)
    
  @unittest.expectedFailure  
  def test_7_get_new_book_after_delete(self):
    id = 3
    r = requests.get(self._get_each_book_url(id))
    self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
  unittest.main()