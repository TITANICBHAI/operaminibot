import os
import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "ultra-lightweight-chat-secret")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Import chat functionality
from chat import get_ai_response, format_conversation

@app.after_request
def after_request(response):
    """Add caching headers for Opera Mini optimization"""
    # Cache static assets
    if request.endpoint == 'static':
        response.headers['Cache-Control'] = 'public, max-age=86400'
    else:
        response.headers['Cache-Control'] = 'no-cache'
    
    # Minimize headers for Opera Mini
    response.headers.pop('Server', None)
    response.headers.pop('Date', None)
    
    return response

@app.route('/')
def index():
    """Landing page with minimal design"""
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    """Main chat interface"""
    if 'conversation' not in session:
        session['conversation'] = []
    
    if request.method == 'POST':
        user_message = request.form.get('message', '').strip()
        
        if user_message:
            # Add user message to conversation
            session['conversation'].append({
                'role': 'user',
                'content': user_message
            })
            
            try:
                # Get AI response
                ai_response = get_ai_response(user_message, session['conversation'])
                
                if ai_response:
                    session['conversation'].append({
                        'role': 'assistant',
                        'content': ai_response
                    })
                else:
                    flash('Sorry, I could not get a response. Please try again.', 'error')
                    
            except Exception as e:
                logging.error(f"Error getting AI response: {e}")
                flash('Network error. Please check your connection and try again.', 'error')
        
        # Keep conversation history limited for memory efficiency
        if len(session['conversation']) > 20:
            session['conversation'] = session['conversation'][-16:]  # Keep last 16 messages
        
        session.modified = True
        return redirect(url_for('chat'))
    
    # Format conversation for display
    formatted_conversation = format_conversation(session['conversation'])
    
    return render_template('chat.html', conversation=formatted_conversation)

@app.route('/clear')
def clear_chat():
    """Clear conversation history"""
    session.pop('conversation', None)
    flash('Conversation cleared.', 'info')
    return redirect(url_for('chat'))

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('index.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
