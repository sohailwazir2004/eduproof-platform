# notification_service.py - Notification Service
#
# Business logic for push and email notifications.

"""
Notification Service

Methods:
- send_push_notification(user_id, title, body) -> None
- send_email(email, subject, body) -> None
- notify_homework_assigned(homework) -> None
- notify_submission_received(submission) -> None
- notify_grade_posted(submission) -> None
- notify_deadline_reminder(homework) -> None
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

# Firebase Admin SDK
try:
    import firebase_admin
    from firebase_admin import credentials, messaging
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

# Email via SendGrid
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False

from app.core.config import settings

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service for sending push notifications and emails.
    Supports Firebase Cloud Messaging and SendGrid.
    """

    def __init__(self):
        self._init_firebase()
        self._init_sendgrid()

    def _init_firebase(self):
        """Initialize Firebase Admin SDK."""
        self.firebase_enabled = False

        if not FIREBASE_AVAILABLE:
            logger.warning("Firebase Admin SDK not installed")
            return

        if not settings.firebase_credentials_path:
            logger.warning("Firebase credentials not configured")
            return

        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(settings.firebase_credentials_path)
                firebase_admin.initialize_app(cred)
            self.firebase_enabled = True
            logger.info("Firebase initialized successfully")
        except Exception as e:
            logger.error(f"Firebase initialization failed: {e}")

    def _init_sendgrid(self):
        """Initialize SendGrid client."""
        self.sendgrid_enabled = False

        if not SENDGRID_AVAILABLE:
            logger.warning("SendGrid SDK not installed")
            return

        if not settings.sendgrid_api_key:
            logger.warning("SendGrid API key not configured")
            return

        try:
            self.sendgrid_client = SendGridAPIClient(settings.sendgrid_api_key)
            self.sendgrid_enabled = True
            logger.info("SendGrid initialized successfully")
        except Exception as e:
            logger.error(f"SendGrid initialization failed: {e}")

    async def send_push_notification(
        self,
        device_token: str,
        title: str,
        body: str,
        data: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        Send push notification to a device.

        Args:
            device_token: FCM device token
            title: Notification title
            body: Notification body
            data: Optional additional data

        Returns:
            True if sent successfully
        """
        if not self.firebase_enabled:
            logger.warning("Push notification skipped: Firebase not enabled")
            return False

        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                token=device_token
            )

            response = messaging.send(message)
            logger.info(f"Push notification sent: {response}")
            return True
        except Exception as e:
            logger.error(f"Push notification failed: {e}")
            return False

    async def send_push_to_multiple(
        self,
        device_tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict[str, str]] = None
    ) -> int:
        """
        Send push notification to multiple devices.

        Args:
            device_tokens: List of FCM device tokens
            title: Notification title
            body: Notification body
            data: Optional additional data

        Returns:
            Number of successful sends
        """
        if not self.firebase_enabled:
            return 0

        try:
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                tokens=device_tokens
            )

            response = messaging.send_multicast(message)
            logger.info(f"Multicast sent: {response.success_count} success")
            return response.success_count
        except Exception as e:
            logger.error(f"Multicast push failed: {e}")
            return 0

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        from_email: Optional[str] = None
    ) -> bool:
        """
        Send email via SendGrid.

        Args:
            to_email: Recipient email
            subject: Email subject
            html_content: HTML content
            from_email: Sender email (defaults to settings)

        Returns:
            True if sent successfully
        """
        if not self.sendgrid_enabled:
            logger.warning("Email skipped: SendGrid not enabled")
            return False

        try:
            message = Mail(
                from_email=from_email or settings.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content
            )

            response = self.sendgrid_client.send(message)
            logger.info(f"Email sent: {response.status_code}")
            return response.status_code in [200, 201, 202]
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return False

    # Notification templates

    async def notify_homework_assigned(
        self,
        student_tokens: List[str],
        homework_title: str,
        due_date: datetime,
        teacher_name: str
    ) -> int:
        """
        Notify students about new homework.

        Args:
            student_tokens: Device tokens of students
            homework_title: Title of homework
            due_date: Due date
            teacher_name: Teacher's name

        Returns:
            Number of notifications sent
        """
        title = "New Homework Assigned"
        body = f"{teacher_name} assigned: {homework_title}. Due: {due_date.strftime('%b %d, %Y')}"
        data = {
            "type": "homework_assigned",
            "title": homework_title,
            "due_date": due_date.isoformat()
        }

        return await self.send_push_to_multiple(student_tokens, title, body, data)

    async def notify_submission_received(
        self,
        teacher_token: str,
        student_name: str,
        homework_title: str
    ) -> bool:
        """
        Notify teacher about new submission.

        Args:
            teacher_token: Teacher's device token
            student_name: Student's name
            homework_title: Homework title

        Returns:
            True if notification sent
        """
        title = "New Submission"
        body = f"{student_name} submitted: {homework_title}"
        data = {
            "type": "submission_received",
            "student": student_name
        }

        return await self.send_push_notification(teacher_token, title, body, data)

    async def notify_grade_posted(
        self,
        student_token: str,
        homework_title: str,
        grade: float,
        feedback: Optional[str] = None
    ) -> bool:
        """
        Notify student about grade.

        Args:
            student_token: Student's device token
            homework_title: Homework title
            grade: Grade received
            feedback: Optional teacher feedback

        Returns:
            True if notification sent
        """
        title = "Grade Posted"
        body = f"You received {grade}% on: {homework_title}"
        if feedback:
            body += f" - {feedback[:50]}..."

        data = {
            "type": "grade_posted",
            "grade": str(grade)
        }

        return await self.send_push_notification(student_token, title, body, data)

    async def notify_deadline_reminder(
        self,
        student_token: str,
        homework_title: str,
        hours_remaining: int
    ) -> bool:
        """
        Send deadline reminder to student.

        Args:
            student_token: Student's device token
            homework_title: Homework title
            hours_remaining: Hours until deadline

        Returns:
            True if notification sent
        """
        title = "Deadline Reminder"
        body = f"{homework_title} is due in {hours_remaining} hours!"
        data = {
            "type": "deadline_reminder",
            "hours": str(hours_remaining)
        }

        return await self.send_push_notification(student_token, title, body, data)

    async def send_parent_report_email(
        self,
        parent_email: str,
        student_name: str,
        report_html: str
    ) -> bool:
        """
        Send weekly progress report to parent.

        Args:
            parent_email: Parent's email
            student_name: Student's name
            report_html: HTML report content

        Returns:
            True if email sent
        """
        subject = f"Weekly Progress Report - {student_name}"
        return await self.send_email(parent_email, subject, report_html)

    async def send_welcome_email(
        self,
        email: str,
        name: str,
        role: str
    ) -> bool:
        """
        Send welcome email to new user.

        Args:
            email: User's email
            name: User's name
            role: User's role

        Returns:
            True if email sent
        """
        subject = "Welcome to EduProof!"
        html_content = f"""
        <html>
        <body>
            <h1>Welcome to EduProof, {name}!</h1>
            <p>Your account has been created as a <strong>{role}</strong>.</p>
            <p>You can now log in and start using the platform.</p>
            <br>
            <p>Best regards,<br>The EduProof Team</p>
        </body>
        </html>
        """

        return await self.send_email(email, subject, html_content)
