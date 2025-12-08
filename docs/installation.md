# Installation

## Prerequisites

Before installing the chatbot, ensure you have:

- Frappe Framework >= 15.0.0
- [frappe_whatsapp](https://github.com/shridarpatil/frappe_whatsapp) app installed and configured

## Install the App

```bash
# Navigate to your Frappe bench
cd frappe-bench

# Get the app
bench get-app https://github.com/shridarpatil/frappe_whatsapp_chatbot

# Install on your site
bench --site your-site install-app frappe_whatsapp_chatbot

# Run migrations
bench --site your-site migrate
```

## Optional: AI Dependencies

If you want to use AI-powered responses, install the required libraries:

```bash
# For OpenAI
pip install openai

# For Anthropic Claude
pip install anthropic
```

## Verify Installation

After installation, you should see:

1. **WhatsApp Chatbot** in the search bar (Settings)
2. **WhatsApp Keyword Reply** in the search bar
3. **WhatsApp Chatbot Flow** in the search bar

## Docker Installation

If using Docker/containerized setup:

```bash
# Inside your container
bench get-app https://github.com/shridarpatil/frappe_whatsapp_chatbot
bench --site site1.local install-app frappe_whatsapp_chatbot
```

## Next Steps

- [Quick Start Guide](quickstart.md) - Enable and test the chatbot
- [Configuration](configuration/settings.md) - Configure chatbot settings
