"""
Configuration settings for the Dama UI application.
This package includes API keys and model limits.
"""

from .api_keys import GROQ_API_KEY
from .model_limits import MODEL_LIMITS

__all__ = ['GROQ_API_KEY', 'MODEL_LIMITS']