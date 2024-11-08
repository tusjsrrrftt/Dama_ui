import aiohttp
import asyncio
from .logging_config import get_logger
from .usage_tracking import update_usage
from config.model_limits import get_model_limit

logger = get_logger(__name__)

GROQ_API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

async def process_request(api_key, model, messages):
    """
    Process a request to the Groq API.

    :param api_key: The API key for authentication
    :param model: The model to use for the request
    :param messages: The conversation history
    :return: The AI's response
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    model_limits = get_model_limit(model)
    if not model_limits:
        raise ValueError(f"Unsupported model: {model}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(GROQ_API_ENDPOINT, json=data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    ai_response = result['choices'][0]['message']['content']
                    
                    # Update usage statistics
                    tokens_used = result['usage']['total_tokens']
                    update_usage(model, tokens_used)
                    
                    logger.info(f"Request processed successfully. Model: {model}, Tokens used: {tokens_used}")
                    return ai_response
                else:
                    error_message = await response.text()
                    logger.error(f"API request failed. Status: {response.status}, Error: {error_message}")
                    raise Exception(f"API request failed: {error_message}")

    except aiohttp.ClientError as e:
        logger.error(f"Network error occurred: {str(e)}")
        raise Exception(f"Network error: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise Exception(f"Unexpected error: {str(e)}")

async def test_process_request():
    """
    Test function for process_request.
    """
    from config.api_keys import GROQ_API_KEY
    
    test_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
    
    try:
        response = await process_request(GROQ_API_KEY, "gemma-7b-it", test_messages)
        print("AI Response:", response)
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_process_request())