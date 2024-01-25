# REAL ESTATE APP API

- This is the API service that powers real estate web app

## Getting Started(Non-Docker Environment)

- Clone the repo: `git clone https://github.com/Levy-Naibei/django-real-estate-app.git`
- `cd django-real-estate-app`
- `pip install -r requirements.txt`
- `python3 manage.py makemigrations`
- `python3 manage.py migrate`
- `python3 manage.py runserver`

## API Endpoints


|       Endpoint                                        |               FUNCTIONALITY                             |
| ------------------------------------------------------|:-------------------------------------------------------
| POST &emsp;&emsp;/api/v1/auth/user/                    | This will register user                                 |
| POST &emsp;&emsp;/ap1/v1/auth/jwt/create/                       | This will login user                                    |
| POST &emsp;&emsp;/auth/v1/request/                    | This will send password reset                           |
| POST &emsp;&emsp;/api/v1/farmer/product/              | This will create Product                                |
| POST &emsp;&emsp;/api/v1/retailer/order/              | This will create order                                  |
| GET  &emsp;&emsp;/api/v1/farmer/product/list/         | This will return all products                           |
| GET  &emsp;&emsp;/api/v1/retailer/order/list          | This will return all placed order                       |
| POST &emsp;&emsp;/api/v1/enquiries/mail/                     | This will post a contact info                           |

### Registration

`POST /auth/v1/register`

Example request body:

```source-multipart/form-data
{
  "user":{
    "firstName": "John",
    "username": "Doe",
    "email":     "jd@gmail.com",
    "password": "pass12",
  }
}
```

No authentication required, returns a User

Required fields: `firstName`, `surname`, `email(unique)`, `password`,
