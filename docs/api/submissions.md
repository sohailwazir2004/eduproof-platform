# Submissions API

## Submit Homework (Student)

`POST /submissions`

Request (multipart/form-data):
- `homework_id`: UUID
- `file`: Image or PDF file

Response:
```json
{
  "id": "uuid",
  "homework_id": "uuid",
  "file_url": "https://...",
  "status": "pending",
  "submitted_at": "2024-01-19T10:30:00Z"
}
```

## Get Submission

`GET /submissions/{id}`

## Grade Submission (Teacher)

`PUT /submissions/{id}/grade`

Request:
```json
{
  "grade": "A",
  "feedback": "Great work!"
}
```

## Get AI Analysis

`GET /submissions/{id}/ai-analysis`

Response:
```json
{
  "relevance_score": 0.95,
  "suggested_grade": "A",
  "feedback_suggestions": ["..."],
  "ocr_text": "..."
}
```
