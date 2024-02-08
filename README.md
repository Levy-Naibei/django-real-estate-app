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

| Endpoint                                                      | FUNCTIONALITY                            |
| ------------------------------------------------------------- | :--------------------------------------- |
| POST &emsp;&emsp; api/v1/auth/users/                          | This will register user                  |
| POST &emsp;&emsp; ap1/v1/auth/jwt/create/                     | This will authenticate user              |
| POST &emsp;&emsp; api/v1/auth/users/activation/               | This will will activate user account     |
| POST &emsp;&emsp; api/v1/auth/users/reset_password/           | This will send password reset            |
| POST &emsp;&emsp; api/v1/auth/users/reset_password_confirm/   | Sends reset password confirm email alert |
| GET &emsp;&emsp;  api/v1/                                     |                                          |
| GET &emsp;&emsp;  api/v1/                                     |                                          |
| POST &emsp;&emsp; api/v1/enquiries/mail/                      | This will send enquiry email             |

### Registration

`POST api/v1/auth/users/`

Example request body:

```application/json
  {
    "email":"jane.doe@gmail.com",
    "username": "janedoe",
    "first_name": "jane",
    "last_name": "doe",
    "password": "pass1234",
    "re_password": "pass1234"
  }
```

No authentication required, returns a User

Required fields: `first_name`, `last_name`, `username`, `email(unique)`, `password`, `re_password`

### Login

`POST api/v1/auth/jwt/create/`

Example request body:

```application/json
  {
    "email":"jane.doe@gmail.com",
    "password": "pass1234",
  }
```

Returns Access and Refresh jwt tokens

Required fields: `email`, `password`

### Account Activation

`POST api/v1/auth/users/activation/`

Example request body:

```application/json
  {
    "uid": "Ng",
    "token": "c101o9-f5fd4e18e998e54f7b324500a0f563ca"
  }
```

Returns/sends activation link to email alert

### Reset password request

`POST api/v1/auth/users/reset_password/`

Example request body:

```application/json
  {
    "email":"jane.doe@gmail.com",
  }
```

Returns/sends reset password link to email alert

Required fields: `email`

### Reset password confirm request

`POST api/v1/auth/users/reset_password_confirm/`

Example request body:

```application/json
  {
    "uid": "Mw",
    "token": "c0yvo4-fbf3d1d6fe592499b91a002c42df062b",
    "new_password": "pass1234",
    "re_new_password":"pass1234"
}
```

Returns reset password confirm email alert

Required fields: `uid`, `token`, `new_password`, `re_new_password`

