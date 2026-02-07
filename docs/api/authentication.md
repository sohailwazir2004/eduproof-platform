# Authentication API

## Login

`POST /auth/login`

Request:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

## Register

`POST /auth/register`

Request:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "role": "student",
  "name": "John Doe"
}
```

## Refresh Token

`POST /auth/refresh`

## Password Reset

`POST /auth/forgot-password`
`POST /auth/reset-password`
