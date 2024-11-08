import json
import os
from datetime import datetime
from .logging_config import get_logger

logger = get_logger(__name__)

USAGE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'usage_stats.json')

def load_usage_data():
    """
    Load usage data from the JSON file.
    """
    if os.path.exists(USAGE_FILE):
        try:
            with open(USAGE_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from {USAGE_FILE}. Starting with empty usage data.")
    return {}

def save_usage_data(data):
    """
    Save usage data to the JSON file.
    """
    os.makedirs(os.path.dirname(USAGE_FILE), exist_ok=True)
    with open(USAGE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def update_usage(model, tokens_used):
    """
    Update the usage statistics for a given model.

    :param model: The name of the model used.
    :param tokens_used: The number of tokens used in this request.
    """
    usage_data = load_usage_data()
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    if model not in usage_data:
        usage_data[model] = {}
    
    if today not in usage_data[model]:
        usage_data[model][today] = 0
    
    usage_data[model][today] += tokens_used
    
    save_usage_data(usage_data)
    logger.info(f"Updated usage for {model}: {tokens_used} tokens on {today}")

def get_usage(model=None, date=None):
    """
    Get usage statistics.

    :param model: Optional. If provided, return usage for this specific model.
    :param date: Optional. If provided, return usage for this specific date (format: 'YYYY-MM-DD').
    :return: A dictionary of usage statistics.
    """
    usage_data = load_usage_data()
    
    if model:
        if model not in usage_data:
            return {model: {}}
        if date:
            return {model: {date: usage_data[model].get(date, 0)}}
        return {model: usage_data[model]}
    
    if date:
        return {m: {date: data.get(date, 0)} for m, data in usage_data.items()}
    
    return usage_data

def get_total_usage(model=None):
    """
    Get total usage across all dates.

    :param model: Optional. If provided, return total usage for this specific model.
    :return: Total token usage.
    """
    usage_data = load_usage_data()
    
    if model:
        if model not in usage_data:
            return 0
        return sum(usage_data[model].values())
    
    return sum(sum(data.values()) for data in usage_data.values())

# Example usage and testing
if __name__ == "__main__":
    # Example usage
    update_usage("gemma-7b-it", 100)
    update_usage("gemma-7b-it", 150)
    update_usage("gemma-2b", 75)
    
    print("Usage for gemma-7b-it:", get_usage("gemma-7b-it"))
    print("Usage for today:", get_usage(date=datetime.now().strftime('%Y-%m-%d')))
    print("Total usage:", get_total_usage())
    print("Total usage for gemma-7b-it:", get_total_usage("gemma-7b-it"))