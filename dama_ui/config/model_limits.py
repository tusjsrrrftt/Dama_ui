"""
Model limits configuration for the Dama UI application.
This file defines the rate limits and token limits for different AI models.
"""

MODEL_LIMITS = {
    "gemma-7b-it": {
        "requests_per_minute": 30,
        "tokens_per_minute": float('inf')
    },
    "gemma2-9b-it": {
        "requests_per_minute": 30,
        "tokens_per_minute": float('inf')
    },
    "llama-3.1-70b-versatile": {
        "requests_per_minute": 100,
        "tokens_per_minute": 131072
    },
    "llama-3.1-8b-instant": {
        "requests_per_minute": 30,
        "tokens_per_minute": 131072
    },
    "llama-guard-3-8b": {
        "requests_per_minute": 30,
        "tokens_per_minute": float('inf')
    },
    "llama3-70b-8192": {
        "requests_per_minute": 30,
        "tokens_per_minute": 6000
    },
    "llama3-8b-8192": {
        "requests_per_minute": 30,
        "tokens_per_minute": 30000
    },
    "mixtral-8x7b-32768": {
        "requests_per_minute": 30,
        "tokens_per_minute": 5000
    }
}

# You can add helper functions here if needed, for example:

def get_model_limit(model_name):
    """
    Get the limits for a specific model.
    
    :param model_name: The name of the model
    :return: A dictionary with the model's limits, or None if the model is not found
    """
    return MODEL_LIMITS.get(model_name)

def is_model_supported(model_name):
    """
    Check if a model is supported.
    
    :param model_name: The name of the model to check
    :return: Boolean indicating whether the model is supported
    """
    return model_name in MODEL_LIMITS

# Add more helper functions as needed