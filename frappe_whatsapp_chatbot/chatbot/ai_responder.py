import frappe
import json


class AIResponder:
    """Generate AI-powered responses (optional feature)."""

    def __init__(self, settings):
        self.settings = settings
        self.provider = settings.ai_provider
        self.api_key = settings.get_password("ai_api_key") if settings.ai_api_key else None
        self.model = settings.ai_model or "gpt-4o-mini"
        self.system_prompt = settings.ai_system_prompt or "You are a helpful assistant."
        self.max_tokens = settings.ai_max_tokens or 500
        self.temperature = settings.ai_temperature or 0.7

    def generate_response(self, message, conversation_history=None):
        """Generate AI response for message."""
        if not self.api_key:
            frappe.log_error("AI API key not configured")
            return None

        try:
            if self.provider == "OpenAI":
                return self.openai_response(message, conversation_history)
            elif self.provider == "Anthropic":
                return self.anthropic_response(message, conversation_history)
            elif self.provider == "Custom":
                return self.custom_response(message, conversation_history)
        except Exception as e:
            frappe.log_error(f"AIResponder generate_response error: {str(e)}")

        return None

    def build_context(self):
        """Build context from AI Context documents."""
        try:
            contexts = frappe.get_all(
                "WhatsApp AI Context",
                filters={"enabled": 1},
                fields=["*"],
                order_by="priority desc"
            )

            context_parts = []
            for ctx in contexts:
                try:
                    if ctx.context_type == "Static Text" and ctx.static_content:
                        context_parts.append(ctx.static_content)
                    elif ctx.context_type == "DocType Query":
                        data = self.query_doctype(ctx)
                        if data:
                            context_parts.append(json.dumps(data, indent=2, default=str))
                except Exception as e:
                    frappe.log_error(f"AIResponder context '{ctx.title}' error: {str(e)}")
                    continue

            return "\n\n".join(context_parts) if context_parts else ""

        except Exception as e:
            frappe.log_error(f"AIResponder build_context error: {str(e)}")
            return ""

    def query_doctype(self, ctx):
        """Query DocType for context."""
        try:
            # Get the target DocType to query (field renamed to avoid conflict with Frappe's doctype attribute)
            target_doctype = ctx.query_doctype
            if not target_doctype:
                return None

            # Handle filters that might already be parsed
            filters = ctx.filters or {}
            if isinstance(filters, str):
                filters = json.loads(filters) if filters else {}
            fields = ["name"]

            if ctx.fields_to_include:
                fields = [f.strip() for f in ctx.fields_to_include.split(",") if f.strip()]

            return frappe.get_all(
                target_doctype,
                filters=filters,
                fields=fields,
                limit=50
            )
        except Exception as e:
            frappe.log_error(f"AIResponder query_doctype error: {str(e)}")
            return None

    def openai_response(self, message, conversation_history):
        """Generate response using OpenAI."""
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)

            messages = [{"role": "system", "content": self.system_prompt}]

            # Add context
            context = self.build_context()
            if context:
                messages.append({
                    "role": "system",
                    "content": f"Here is relevant information you can use to answer questions:\n{context}"
                })

            # Add conversation history (last 10 messages)
            if conversation_history:
                for msg in conversation_history[-10:]:
                    role = "user" if msg["direction"] == "Incoming" else "assistant"
                    messages.append({"role": role, "content": msg["message"]})

            # Add current message
            messages.append({"role": "user", "content": message})

            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            return response.choices[0].message.content

        except ImportError:
            frappe.log_error("OpenAI library not installed. Run: pip install openai")
            return None
        except Exception as e:
            frappe.log_error(f"OpenAI API error: {str(e)}")
            return None

    def anthropic_response(self, message, conversation_history):
        """Generate response using Anthropic Claude."""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)

            # Build messages
            messages = []

            if conversation_history:
                for msg in conversation_history[-10:]:
                    role = "user" if msg["direction"] == "Incoming" else "assistant"
                    messages.append({"role": role, "content": msg["message"]})

            messages.append({"role": "user", "content": message})

            # Build system prompt with context
            system = self.system_prompt
            context = self.build_context()
            if context:
                system += f"\n\nHere is relevant information you can use to answer questions:\n{context}"

            response = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system,
                messages=messages
            )

            return response.content[0].text

        except ImportError:
            frappe.log_error("Anthropic library not installed. Run: pip install anthropic")
            return None
        except Exception as e:
            frappe.log_error(f"Anthropic API error: {str(e)}")
            return None

    def custom_response(self, message, conversation_history):
        """Generate response using custom endpoint."""
        # Placeholder for custom AI provider integration
        frappe.log_error("Custom AI provider not implemented")
        return None
