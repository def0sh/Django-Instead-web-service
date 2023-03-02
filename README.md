# Instead - site where an employer can find a future employee and developers can post their projects.
### Profiles
<img width="945" alt="image_2023-01-13_20-59-08" src="https://user-images.githubusercontent.com/74783488/212376493-f4fc9461-983e-473a-bea3-7a2996be5e5b.png">

---
### Projects
<img width="945" alt="image_2023-01-13_21-03-46" src="https://user-images.githubusercontent.com/74783488/212377374-f13be548-57c9-4df1-b90f-f23095cd1ee3.png">

---
### Account
<img width="943" alt="image_2023-01-14_01-43-40" src="https://user-images.githubusercontent.com/74783488/212424870-2deba4db-2e26-46a1-92f2-6f8c4b12f5e2.png">

## :computer_mouse: Site functionality:

* Authorization and authentication system
* Profile and project cards
* Сomments and projects evaluation
* Messenger
* Search by projects and profiles
* Filtering projects by tags and profiles by skills
* Full CRUD operations for users from the frontend

### :hammer_and_wrench: Installation:

1. `$ pip install -r requirements.txt`
2. `python manage.py runserver`


## :atom: The service also has its own REST api with:

* Authorization and authentication by token
* Permissions
* CRUD operations

### Api v1 is still in development but there are some basic operations

## Api documentaton

### Response codes:
| Code | Status             |  
|:-----|:-------------------|
| 200  | Success            |
| 201  | Created success    |
| 400  | Bad request        |
| 401  | Unauthorized       |
| 404  | Cannot be found    |
| 405  | Method not allowed |
| 50X  | Server Error       |

### Example:

#### Request:

```http
GET http://127.0.0.1:8000/api/v1/
```


#### Response:

```json
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "projects": "http://127.0.0.1:8000/api/v1/projects/",
    "profiles": "http://127.0.0.1:8000/api/v1/profiles/"
}
```
#### In the example above you can request profiles or projects list

### Get Access Token

### 1. Register:

#### _Request with Body_

```http
POST http://127.0.0.1:8000/api/v1/auth/users/

{
    "username": "testuser",
    "password": "test123!",
    "email": "test@gmail.com"
}
```

#### _Response_:

```json
HTTP 201 Created
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
{
    "email": "test@gmail.com",
    "username": "testuser",
    "id": 40
}
```
***
### 2. Get token:

#### _Request with Body_

```http
POST http://127.0.0.1:8000/api/auth/token/login/

{
    "username": "testuser",
    "password": "test123!"
}
```

#### _Response_:

```json
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "auth_token": "04b5fbcbb5de9d7aef3be8e75eb02540bf10d441"
}
```

_For PUT or POST use your token in the  header request._

>You can make requests in readonly if you don't have a token.

#### Also you can:

```http
GET http://127.0.0.1:8000/api/v1/profiles/<username>
```
_Get information about one profile_

```http
GET http://127.0.0.1:8000/api/v1/projects/<title>
```
_information about one project_

### Will be updated ! :nerd_face:
/













