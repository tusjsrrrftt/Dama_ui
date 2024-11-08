import tiktoken
from .logging_config import get_logger

logger = get_logger(__name__)

def count_tokens(text, model="gemma-7b-it"):
    """
    Count the number of tokens in the given text for the specified model.

    :param text: The input text to count tokens for.
    :param model: The model to use for tokenization (default: "gemma-7b-it").
    :return: The number of tokens in the text.
    """
    try:
        # For gemma models, we'll use the cl100k_base encoding
        # This is an approximation, as the exact tokenizer for Gemma might differ
        encoding = tiktoken.get_encoding("cl100k_base")
        
        # Encode the text and count the tokens
        token_count = len(encoding.encode(text))
        
        logger.debug(f"Token count for '{text[:20]}...': {token_count}")
        return token_count
    
    except Exception as e:
        logger.error(f"Error counting tokens: {str(e)}")
        # Return a default value or raise the exception
        return 0  # or you could re-raise the exception: raise

def estimate_tokens_from_messages(messages):
    """
    Estimate the total number of tokens in a list of messages.

    :param messages: A list of message dictionaries, each containing 'role' and 'content'.
    :return: The estimated total number of tokens.
    """
    total_tokens = 0
    for message in messages:
        # Count tokens in the content
        content_tokens = count_tokens(message['content'])
        
        # Add tokens for role (approximation)
        role_tokens = 1  # Assuming 1 token for the role
        
        total_tokens += content_tokens + role_tokens
    
    logger.info(f"Estimated total tokens for messages: {total_tokens}")
    return total_tokens

# Example usage and testing
if __name__ == "__main__":
    test_text = "Hello, world! This is a test message to count tokens."
    token_count = count_tokens(test_text)
    print(f"Token count for '{test_text}': {token_count}")

    test_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."},
        {"role": "user", "content": "Can you tell me more about Paris?"}
    ]
    estimated_tokens = estimate_tokens_from_messages(test_messages)
    print(f"Estimated tokens for test messages: {estimated_tokens}")