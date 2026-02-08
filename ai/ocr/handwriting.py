# handwriting.py - Handwriting Recognition
#
# Specialized handwriting OCR using vision models.

"""
Handwriting Recognizer

Uses specialized models for handwritten text extraction from images.

Methods:
- recognize(image) -> str
- detect_language(image) -> str
- confidence_score(image) -> float
- extract_from_url(url) -> dict
"""

import base64
import logging
from typing import Optional, Tuple
from pathlib import Path

# OpenAI for GPT-4 Vision
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Anthropic for Claude Vision
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# Tesseract OCR as fallback
try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

from ai.config import settings

logger = logging.getLogger(__name__)


class HandwritingRecognizer:
    """
    Recognizes handwritten text from images using multiple backends.
    Primary: GPT-4 Vision or Claude Vision
    Fallback: Tesseract OCR
    """

    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None

        if OPENAI_AVAILABLE and settings.openai_api_key:
            self.openai_client = OpenAI(api_key=settings.openai_api_key)
            logger.info("OpenAI client initialized")

        if ANTHROPIC_AVAILABLE and settings.anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=settings.anthropic_api_key)
            logger.info("Anthropic client initialized")

    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64."""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def _get_mime_type(self, image_path: str) -> str:
        """Get MIME type from file extension."""
        ext = Path(image_path).suffix.lower()
        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }
        return mime_types.get(ext, "image/jpeg")

    async def recognize(self, image_path: str) -> str:
        """
        Recognize handwritten text from an image.

        Args:
            image_path: Path to image file

        Returns:
            Extracted text
        """
        # Try OpenAI GPT-4 Vision first
        if self.openai_client:
            try:
                return await self._recognize_with_openai(image_path)
            except Exception as e:
                logger.warning(f"OpenAI OCR failed: {e}")

        # Try Anthropic Claude Vision
        if self.anthropic_client:
            try:
                return await self._recognize_with_anthropic(image_path)
            except Exception as e:
                logger.warning(f"Anthropic OCR failed: {e}")

        # Fallback to Tesseract
        if TESSERACT_AVAILABLE:
            try:
                return await self._recognize_with_tesseract(image_path)
            except Exception as e:
                logger.error(f"Tesseract OCR failed: {e}")

        return ""

    async def _recognize_with_openai(self, image_path: str) -> str:
        """Use GPT-4 Vision for handwriting recognition."""
        base64_image = self._encode_image(image_path)
        mime_type = self._get_mime_type(image_path)

        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please extract and transcribe all handwritten text from this image. Return only the extracted text, preserving line breaks where appropriate."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000
        )

        return response.choices[0].message.content

    async def _recognize_with_anthropic(self, image_path: str) -> str:
        """Use Claude Vision for handwriting recognition."""
        base64_image = self._encode_image(image_path)
        mime_type = self._get_mime_type(image_path)

        response = self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime_type,
                                "data": base64_image
                            }
                        },
                        {
                            "type": "text",
                            "text": "Please extract and transcribe all handwritten text from this image. Return only the extracted text, preserving line breaks where appropriate."
                        }
                    ]
                }
            ]
        )

        return response.content[0].text

    async def _recognize_with_tesseract(self, image_path: str) -> str:
        """Use Tesseract OCR as fallback."""
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()

    async def recognize_with_confidence(
        self,
        image_path: str
    ) -> Tuple[str, float]:
        """
        Recognize text and return confidence score.

        Args:
            image_path: Path to image file

        Returns:
            Tuple of (extracted text, confidence score 0-1)
        """
        text = await self.recognize(image_path)

        # Calculate simple confidence based on text quality
        if not text:
            return "", 0.0

        # Basic heuristics for confidence
        word_count = len(text.split())
        avg_word_length = sum(len(w) for w in text.split()) / max(word_count, 1)

        # Higher confidence for reasonable text patterns
        confidence = 0.5
        if word_count > 3:
            confidence += 0.2
        if 3 < avg_word_length < 10:
            confidence += 0.2
        if text.count(" ") > 0:
            confidence += 0.1

        return text, min(confidence, 1.0)

    async def extract_from_url(self, image_url: str) -> dict:
        """
        Extract text from an image URL.

        Args:
            image_url: URL of the image

        Returns:
            Dict with extracted_text, confidence, and metadata
        """
        import httpx
        import tempfile

        # Download image
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url)
            response.raise_for_status()

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(response.content)
            temp_path = f.name

        try:
            text, confidence = await self.recognize_with_confidence(temp_path)
            return {
                "extracted_text": text,
                "confidence": confidence,
                "source_url": image_url,
                "word_count": len(text.split()) if text else 0
            }
        finally:
            Path(temp_path).unlink(missing_ok=True)
