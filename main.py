import json
from fastapi import FastAPI, status
from fastapi.responses import Response
from schema import Contact


app = FastAPI()


@app.post('/post', status_code=status.HTTP_200_OK)
def add_contact(contact: Contact, response: Response):
    try:
        with open('addressbook.json') as file:
            db_contacts = json.load(file)
        if contact.book_name in db_contacts:
            book = db_contacts.get(contact.book_name)
            if book.get(contact.first_name):
                raise Exception('Contact Already Exists!!')
            book.update({contact.first_name: contact.model_dump()})
            db_contacts.update({contact.book_name: book})
        else:
            db_contacts.update({contact.book_name: {contact.first_name: contact.model_dump()}})
        with open('addressbook.json', 'w') as file:
            json.dump(db_contacts, file, indent=2)
        return {'message': "Contacts Added", 'status': 201, 'data': contact.model_dump()}
    except FileNotFoundError:
        return {'message': 'File Not Found!!', 'status': 500}
    except Exception as ex:
        response.status_code = 400
        return {'message': str(ex), 'status': 400}


@app.get('/get', status_code=status.HTTP_200_OK)
def retrieve_all_contact(response: Response):
    try:
        with open('addressbook.json') as file:
            data = json.load(file)
        return {'message': 'data retrieved', 'status': 200, 'data': data}
    except FileNotFoundError:
        response.status_code = 400
    except Exception as ex:
        response.status_code = 400
        return {'message': str(ex), 'status': 400}


@app.delete('/delete', status_code=status.HTTP_200_OK)
def delete_contact(contact: Contact, response: Response):
    try:
        with open('addressbook.json') as file:
            db_contacts = json.load(file)

        if contact.book_name in db_contacts:
            book = db_contacts.get(contact.book_name)
            if book.get(contact.first_name):
                del book[contact.first_name]
                db_contacts.update({contact.book_name: book})
            else:
                raise Exception('Contact Not Found')
        else:
            raise Exception('Book Not Found')

        with open('addressbook.json', 'w') as file:
            json.dump(db_contacts, file, indent=2)

        return {'message': "Contact Deleted", 'status': 200}

    except FileNotFoundError:
        return {'message': 'File Not Found!!', 'status': 500}
    except Exception as ex:
        response.status_code = 400
        return {'message': str(ex), 'status': 400}


@app.put('/update', status_code=status.HTTP_200_OK)
def update_contact(contact: Contact, response: Response):
    try:
        with open('addressbook.json') as file:
            db_contact = json.load(file)

        if contact.book_name in db_contact:
            book = db_contact.get(contact.book_name)
            if book.get(contact.first_name):
                db_contact.update({contact.book_name: {contact.first_name: contact.model_dump()}})

            else:
                raise Exception('Contact Not Found')
        else:
            print('Book Not Found')

        with open('addressbook.json', 'w') as file:
            json.dump(db_contact, file, indent=2)

        return {'message': "Contact Updated", 'status': 200}

    except FileNotFoundError:
        return {'message': 'File Not Found!!', 'status': 500}
    except Exception as ex:
        response.status_code = 400
        return {'message': str(ex), 'status': 400}
