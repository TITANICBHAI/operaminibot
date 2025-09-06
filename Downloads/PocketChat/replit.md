# Ultra-Lightweight Chat Application

## Overview

This is a minimal chatbot application designed specifically for feature phones and low-bandwidth environments. The application provides AI-powered chat functionality through a text-only interface optimized for devices with limited memory, slow network connections, and basic browsers like Opera Mini 4.4. The system prioritizes data efficiency, fast loading times, and compatibility with 2G networks.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **Styling**: Ultra-lightweight CSS (under 5KB) with minimal styling for feature phone compatibility
- **Responsive Design**: Optimized for small screens with basic viewport settings
- **Progressive Enhancement**: Text-only interface that works without JavaScript

### Backend Architecture
- **Web Framework**: Flask with minimal middleware stack
- **Session Management**: Server-side sessions using Flask's built-in session handling
- **Conversation Storage**: In-memory session storage for chat history
- **Response Optimization**: Automatic message truncation and history limiting for memory efficiency
- **Error Handling**: Graceful degradation with retry logic for API failures

### Performance Optimizations
- **Compression**: Automatic gzip compression for text content
- **Caching Strategy**: Static asset caching with appropriate headers
- **Header Minimization**: Removal of unnecessary HTTP headers for Opera Mini compatibility
- **Memory Management**: Conversation history limited to last 8 messages (4 exchanges)
- **Content Limits**: User messages capped at 500 characters, AI responses kept to 2-3 sentences

### Data Flow Architecture
- **Stateless Design**: Each request is independent with session-based state management
- **Conversation Context**: Recent conversation history passed to AI for context while maintaining memory limits
- **Message Processing**: Input validation and sanitization before AI processing

## External Dependencies

### AI Service Integration
- **Groq API**: Primary AI response generation service
- **API Configuration**: Environment variable-based API key management
- **Retry Logic**: Built-in retry mechanism for handling network failures on slow connections

### Runtime Dependencies
- **Flask**: Core web framework for HTTP handling and templating
- **Werkzeug**: WSGI utilities and proxy fix middleware for deployment
- **Groq Python SDK**: Official client library for Groq API integration

### Deployment Requirements
- **Environment Variables**: 
  - `GROQ_API_KEY`: Required for AI functionality
  - `SESSION_SECRET`: Optional session security key
- **Python Runtime**: Compatible with standard Python 3.x environments
- **WSGI Server**: Designed to work with any WSGI-compatible server