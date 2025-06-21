import openai
from ..config import settings

def generate_response(input_text: str, model: str = None) -> str:
    """
    Generate a response using the specified LLM model.
    
    Args:
        input_text: The input text to process
        model: The model to use (defaults to settings.DEFAULT_MODEL if None)
        
    Returns:
        The generated response text
    """
    if not model:
        model = settings.DEFAULT_MODEL
    
    # Set OpenAI API key
    openai.api_key = settings.OPENAI_API_KEY
    
    # Call the OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are Evolve, a helpful AI assistant."},
                {"role": "user", "content": input_text}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        # Extract and return the response text
        return response.choices[0].message.content
    except Exception as e:
        # Log the error and re-raise
        print(f"Error calling OpenAI API: {str(e)}")
        raise
