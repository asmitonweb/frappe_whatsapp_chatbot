# Frappe WhatsApp Chatbot

> A comprehensive chatbot solution for Frappe WhatsApp integration

## What is this?

Frappe WhatsApp Chatbot is an extension for [frappe_whatsapp](https://github.com/shridarpatil/frappe_whatsapp) that adds powerful chatbot capabilities to your WhatsApp Business integration.

## Features

- **Keyword-Based Replies** - Configure automatic responses based on keywords with multiple match types (exact, contains, regex)
- **Conversation Flows** - Build multi-step decision trees to collect information from users
- **Dynamic Script Responses** - Execute Python scripts to generate responses from your database (e.g., check order status)
- **Document Creation** - Automatically create Frappe documents (Leads, Issues, etc.) from collected data
- **Optional AI Integration** - OpenAI and Anthropic support for intelligent fallback responses
- **Session Management** - Track conversations with automatic timeout handling
- **Business Hours** - Restrict bot responses to specified hours

## Quick Example

**Keyword Reply:**
```
User: "hello"
Bot: "Hi! How can I help you today?"
```

**Conversation Flow:**
```
User: "sales"
Bot: "Great! What's your name?"
User: "John"
Bot: "Thanks John! What's your email?"
User: "john@example.com"
Bot: "Thank you! Our sales team will contact you shortly."
→ Creates Lead document automatically
```

## Getting Started

1. [Install the app](installation.md)
2. [Enable the chatbot](quickstart.md)
3. [Create your first keyword reply](configuration/keywords.md)

## Requirements

- Frappe Framework >= 15.0.0
- [frappe_whatsapp](https://github.com/shridarpatil/frappe_whatsapp) app

## License

MIT with Commons Clause - Free to use, modify, and distribute. Cannot be sold commercially.

## Author

Shridhar Patil (shrip.dev@gmail.com)
