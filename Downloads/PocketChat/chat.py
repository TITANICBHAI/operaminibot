import os
import logging
from groq import Groq
import time

# Initialize Groq client
try:
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY", "")
    )
    logging.info("Groq client initialized successfully")
except Exception as e:
    logging.error(f"Failed to initialize Groq client: {e}")
    client = None

def get_ai_response(user_message, conversation_history=None, max_retries=2):
    """
    Get AI response from Groq API with retry logic and optimization for slow networks
    """
    if not client:
        logging.error("Groq client not initialized")
        return "Sorry, the AI service is not available."
    
    try:
        # Prepare conversation context (limited for feature phone memory)
        messages = []
        
        # Add system message for context
        messages.append({
            "role": "system",
            "content": "You are a helpful assistant. Keep responses short and clear for mobile users. Limit responses to 2-3 sentences maximum."
        })
        
        # Add recent conversation history (max 4 exchanges to save memory)
        if conversation_history:
            recent_history = conversation_history[-8:]  # Last 8 messages (4 exchanges)
            for msg in recent_history[:-1]:  # Exclude the current message
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"][:200]  # Truncate long messages
                })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message[:500]  # Limit input length
        })
        
        # Make API call with retry logic
        for attempt in range(max_retries + 1):
            try:
                logging.info(f"Attempting Groq API call (attempt {attempt + 1})")
                
                response = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.1-8b-instant",  # Fast model for feature phones
                    max_tokens=150,  # Short responses for slow networks
                    temperature=0.7,
                    timeout=15  # Short timeout for 2G networks
                )
                
                ai_message = response.choices[0].message.content
                if ai_message:
                    ai_message = ai_message.strip()
                else:
                    ai_message = "Sorry, I couldn't generate a response."
                
                # Additional response length check
                if len(ai_message) > 300:
                    ai_message = ai_message[:297] + "..."
                
                logging.info("Successfully received AI response")
                return ai_message
                
            except Exception as api_error:
                logging.error(f"API call failed (attempt {attempt + 1}): {api_error}")
                
                if attempt < max_retries:
                    time.sleep(1)  # Brief pause before retry
                    continue
                else:
                    # Return fallback message on final failure
                    if "timeout" in str(api_error).lower():
                        return "Network timeout. Please try again with a shorter message."
                    else:
                        return "Sorry, I'm having trouble connecting. Please try again."
                        
    except Exception as e:
        logging.error(f"Unexpected error in get_ai_response: {e}")
        return "Sorry, something went wrong. Please try again."

def format_conversation(conversation):
    """
    Format conversation for display on feature phones with minimal HTML
    """
    if not conversation:
        return []
    
    formatted = []
    for msg in conversation:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        
        # Truncate very long messages for display
        if len(content) > 500:
            content = content[:497] + "..."
        
        formatted.append({
            'role': role,
            'content': content,
            'is_user': role == 'user'
        })
    
    return formatted
