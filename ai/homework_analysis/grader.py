# grader.py - AI Grading Assistant
#
# Suggest grades based on content analysis using LLMs.

"""
AI Grader

Methods:
- suggest_grade(submission_text, rubric) -> GradeSuggestion
- analyze_completeness(submission_text, requirements) -> float
- identify_errors(submission_text) -> List[Error]

GradeSuggestion:
- suggested_grade: float
- confidence: float
- reasoning: str
- improvements: List[str]
"""

import json
import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

# OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Anthropic
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from ai.config import settings

logger = logging.getLogger(__name__)


@dataclass
class GradeSuggestion:
    """Grade suggestion result."""
    suggested_grade: float
    confidence: float
    reasoning: str
    improvements: List[str]
    errors_found: List[str]


@dataclass
class CompletenessResult:
    """Completeness analysis result."""
    score: float
    covered_topics: List[str]
    missing_topics: List[str]
    feedback: str


class AIGrader:
    """
    AI-powered homework grading assistant.
    Uses LLMs to analyze submissions and suggest grades.
    """

    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None

        if OPENAI_AVAILABLE and settings.openai_api_key:
            self.openai_client = OpenAI(api_key=settings.openai_api_key)
            logger.info("OpenAI grader initialized")

        if ANTHROPIC_AVAILABLE and settings.anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=settings.anthropic_api_key)
            logger.info("Anthropic grader initialized")

    async def suggest_grade(
        self,
        submission_text: str,
        homework_description: str,
        rubric: Optional[Dict[str, Any]] = None,
        max_points: float = 100
    ) -> GradeSuggestion:
        """
        Suggest a grade for a homework submission.

        Args:
            submission_text: The student's submission text
            homework_description: Description of the homework assignment
            rubric: Optional grading rubric
            max_points: Maximum possible points

        Returns:
            GradeSuggestion with grade, confidence, and feedback
        """
        prompt = self._build_grading_prompt(
            submission_text,
            homework_description,
            rubric,
            max_points
        )

        try:
            if self.openai_client:
                result = await self._grade_with_openai(prompt)
            elif self.anthropic_client:
                result = await self._grade_with_anthropic(prompt)
            else:
                return self._default_grade_suggestion()

            return self._parse_grading_response(result, max_points)
        except Exception as e:
            logger.error(f"Grading failed: {e}")
            return self._default_grade_suggestion()

    def _build_grading_prompt(
        self,
        submission_text: str,
        homework_description: str,
        rubric: Optional[Dict[str, Any]],
        max_points: float
    ) -> str:
        """Build the grading prompt."""
        rubric_text = ""
        if rubric:
            rubric_text = f"\n\nGrading Rubric:\n{json.dumps(rubric, indent=2)}"

        return f"""You are an educational grading assistant. Analyze the following homework submission and provide a grade suggestion.

Assignment Description:
{homework_description}
{rubric_text}

Student Submission:
{submission_text}

Please evaluate this submission and respond in the following JSON format:
{{
    "suggested_grade": <number between 0 and {max_points}>,
    "confidence": <number between 0 and 1>,
    "reasoning": "<brief explanation of the grade>",
    "improvements": ["<suggestion 1>", "<suggestion 2>"],
    "errors_found": ["<error 1>", "<error 2>"]
}}

Be fair but thorough in your assessment. Focus on:
1. Correctness of the content
2. Completeness of the response
3. Quality of explanation or work shown
4. Adherence to assignment requirements"""

    async def _grade_with_openai(self, prompt: str) -> str:
        """Grade using OpenAI."""
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an educational grading assistant. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content

    async def _grade_with_anthropic(self, prompt: str) -> str:
        """Grade using Anthropic Claude."""
        response = self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt + "\n\nRespond ONLY with valid JSON, no other text."}
            ]
        )
        return response.content[0].text

    def _parse_grading_response(
        self,
        response: str,
        max_points: float
    ) -> GradeSuggestion:
        """Parse LLM response into GradeSuggestion."""
        try:
            # Clean up response if needed
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]

            data = json.loads(response)

            return GradeSuggestion(
                suggested_grade=min(max(float(data.get("suggested_grade", 0)), 0), max_points),
                confidence=min(max(float(data.get("confidence", 0.5)), 0), 1),
                reasoning=str(data.get("reasoning", "Unable to provide reasoning")),
                improvements=list(data.get("improvements", [])),
                errors_found=list(data.get("errors_found", []))
            )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse grading response: {e}")
            return self._default_grade_suggestion()

    def _default_grade_suggestion(self) -> GradeSuggestion:
        """Return a default grade suggestion when AI fails."""
        return GradeSuggestion(
            suggested_grade=0,
            confidence=0,
            reasoning="Unable to analyze submission. Manual review required.",
            improvements=["Manual review recommended"],
            errors_found=[]
        )

    async def analyze_completeness(
        self,
        submission_text: str,
        requirements: List[str]
    ) -> CompletenessResult:
        """
        Analyze how complete a submission is.

        Args:
            submission_text: The student's submission
            requirements: List of required topics/items

        Returns:
            CompletenessResult with score and details
        """
        prompt = f"""Analyze this homework submission for completeness.

Required topics/items:
{json.dumps(requirements, indent=2)}

Student Submission:
{submission_text}

Respond in JSON format:
{{
    "score": <0-100 completeness percentage>,
    "covered_topics": ["<topic that was addressed>", ...],
    "missing_topics": ["<topic that was missed>", ...],
    "feedback": "<brief feedback on completeness>"
}}"""

        try:
            if self.openai_client:
                response = await self._grade_with_openai(prompt)
            elif self.anthropic_client:
                response = await self._grade_with_anthropic(prompt)
            else:
                return CompletenessResult(0, [], requirements, "AI analysis unavailable")

            data = json.loads(response.strip())
            return CompletenessResult(
                score=float(data.get("score", 0)),
                covered_topics=list(data.get("covered_topics", [])),
                missing_topics=list(data.get("missing_topics", [])),
                feedback=str(data.get("feedback", ""))
            )
        except Exception as e:
            logger.error(f"Completeness analysis failed: {e}")
            return CompletenessResult(0, [], requirements, "Analysis failed")

    async def identify_errors(
        self,
        submission_text: str,
        subject: str = "general"
    ) -> List[Dict[str, str]]:
        """
        Identify errors in a submission.

        Args:
            submission_text: The student's submission
            subject: Subject area (math, science, english, etc.)

        Returns:
            List of errors with descriptions
        """
        prompt = f"""Analyze this {subject} homework submission and identify any errors or mistakes.

Student Submission:
{submission_text}

Respond in JSON format:
{{
    "errors": [
        {{
            "type": "<error type: factual, calculation, grammar, logic, etc.>",
            "description": "<what the error is>",
            "location": "<where in the text>",
            "correction": "<suggested correction>"
        }}
    ]
}}

If no errors are found, return {{"errors": []}}"""

        try:
            if self.openai_client:
                response = await self._grade_with_openai(prompt)
            elif self.anthropic_client:
                response = await self._grade_with_anthropic(prompt)
            else:
                return []

            data = json.loads(response.strip())
            return list(data.get("errors", []))
        except Exception as e:
            logger.error(f"Error identification failed: {e}")
            return []

    async def generate_feedback(
        self,
        submission_text: str,
        homework_description: str,
        grade: float
    ) -> str:
        """
        Generate constructive feedback for a submission.

        Args:
            submission_text: The student's submission
            homework_description: Assignment description
            grade: The grade given

        Returns:
            Constructive feedback text
        """
        prompt = f"""Generate constructive feedback for this homework submission.

Assignment: {homework_description}
Grade: {grade}/100

Student Submission:
{submission_text}

Provide encouraging but helpful feedback that:
1. Acknowledges what was done well
2. Points out areas for improvement
3. Gives specific suggestions
4. Maintains a supportive tone

Keep the feedback concise (2-3 paragraphs max)."""

        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a supportive teacher providing feedback."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500
                )
                return response.choices[0].message.content
            elif self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            else:
                return "AI feedback generation unavailable."
        except Exception as e:
            logger.error(f"Feedback generation failed: {e}")
            return "Unable to generate feedback. Please review manually."
