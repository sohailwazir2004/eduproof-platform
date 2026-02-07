# Homework API

## List Homework

`GET /homework`

Query Parameters:
- `class_id`: Filter by class
- `subject_id`: Filter by subject
- `status`: pending | past_due | completed
- `page`: Page number
- `limit`: Items per page

## Get Homework

`GET /homework/{id}`

## Create Homework (Teacher)

`POST /homework`

Request:
```json
{
  "title": "Chapter 5 Exercises",
  "description": "Complete questions 1-10",
  "class_id": "uuid",
  "subject_id": "uuid",
  "textbook_id": "uuid",
  "page_numbers": "45-47",
  "due_date": "2024-01-20T23:59:59Z"
}
```

## Update Homework (Teacher)

`PUT /homework/{id}`

## Delete Homework (Teacher)

`DELETE /homework/{id}`
