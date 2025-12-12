# Security Best Practices

This guide covers security considerations when configuring and using the WhatsApp Chatbot.

## Script Execution

### Available Variables

When writing scripts for Keyword Replies or Flow completion actions, these variables are available:

| Variable | Type | Description |
|----------|------|-------------|
| `doc` | Document | The WhatsApp Message document |
| `phone_number` | String | Sender's phone number |
| `message` | String | The message text |
| `account` | String | WhatsApp Account name |
| `response` | None | Set this to return a response |
| `frappe` | Module | Frappe framework (limited in safe_exec) |

### Setting Response

```python
# Simple text response
response = "Hello! Your request has been received."

# Or use frappe.response for API-style scripts
frappe.response['message'] = "Hello! Your request has been received."
```

### Safe Script Writing

**DO:**
```python
# Use provided variables
response = f"Hello {phone_number}, we received: {message}"

# Query data safely
customer = frappe.db.get_value("Customer", {"mobile_no": phone_number}, "name")
if customer:
    response = f"Welcome back, {customer}!"
```

**DON'T:**
```python
# Never use eval() or exec() on user input
eval(message)  # DANGEROUS!

# Never expose sensitive data
response = frappe.get_doc("User", "Administrator").as_dict()  # DANGEROUS!

# Never modify system settings
frappe.db.set_value("System Settings", None, "enable_password_policy", 0)  # DANGEROUS!
```

### Script Execution Context

Scripts run with `safe_exec()` which restricts:
- File system access
- System command execution
- Import of dangerous modules
- Network operations (use `frappe.make_get_request` instead)

## Input Validation

### Phone Number Validation

The chatbot accepts phone numbers as-is from WhatsApp. When using phone numbers in your scripts:

```python
# Validate phone number format before database queries
import re
if re.match(r'^\d{10,15}$', phone_number):
    # Safe to use
    pass
else:
    response = "Invalid phone number format"
```

### Message Content

User messages can contain:
- Special characters
- Very long text
- Malicious payloads

Always sanitize before:
- Storing in database fields
- Using in SQL queries (use Frappe ORM)
- Displaying in HTML

```python
# Frappe ORM is safe from SQL injection
frappe.get_all("Lead", filters={"mobile_no": phone_number})  # Safe

# Never concatenate user input into queries
frappe.db.sql(f"SELECT * FROM tabLead WHERE mobile = '{phone_number}'")  # DANGEROUS!
```

## Regex Patterns

When using Regex match type in Keyword Replies:

### Safe Patterns
```
^hello$          # Exact match
^order\s+\d+$    # Order followed by number
```

### Dangerous Patterns (ReDoS)
```
(a+)+$           # Exponential backtracking
(.*a){20}        # Catastrophic backtracking
```

Test your regex patterns with long inputs before deploying.

## API Endpoints

When configuring API endpoints for flow completion:

### Recommendations

1. **Use HTTPS only** - Never use HTTP endpoints
2. **Validate SSL certificates** - Don't disable verification
3. **Use authentication** - Add API keys or tokens
4. **Whitelist domains** - Only allow trusted endpoints

### Example Safe Configuration

```
Endpoint: https://api.yourcompany.com/webhook
Headers: {"Authorization": "Bearer ${api_key}"}
```

## Data Protection

### Sensitive Data

Never log or expose:
- Full phone numbers in public logs
- Message content in error messages
- API keys or tokens

### Session Data

Session data is stored in JSON format. Avoid storing:
- Passwords
- Credit card numbers
- Personal identification numbers

```python
# Good - store reference
session_data["customer_id"] = "CUST-001"

# Bad - store sensitive data
session_data["credit_card"] = "4111-1111-1111-1111"  # NEVER!
```

### Data Retention

Consider implementing:
- Automatic session cleanup after X days
- Message archival policy
- Right to deletion (GDPR)

## Access Control

### Who Can Configure

Restrict access to:
- **WhatsApp Chatbot** settings - System Managers only
- **Server Scripts** - Script Manager role only
- **Keyword Replies** - Trusted users only

### Role Permissions

```
WhatsApp Chatbot: System Manager (read, write)
WhatsApp Keyword Reply: System Manager (read, write, create, delete)
WhatsApp Chatbot Flow: System Manager (read, write, create, delete)
WhatsApp Chatbot Session: System Manager (read, write)
```

## Monitoring & Alerts

### What to Monitor

1. **Error Log** - Check for script errors daily
2. **Failed messages** - Messages with no response
3. **Unusual patterns** - Spam or abuse

### Setting Up Alerts

Create a scheduled job to alert on anomalies:

```python
# Example: Alert on high error rate
error_count = frappe.db.count("Error Log", {
    "creation": (">", frappe.utils.add_days(frappe.utils.now(), -1)),
    "method": ("like", "%WhatsApp Chatbot%")
})

if error_count > 100:
    frappe.sendmail(
        recipients=["admin@example.com"],
        subject="High Chatbot Error Rate",
        message=f"{error_count} errors in last 24 hours"
    )
```

## Checklist

Before going to production:

- [ ] Review all Server Scripts for security issues
- [ ] Test regex patterns with long/malicious inputs
- [ ] Verify API endpoints use HTTPS
- [ ] Set appropriate role permissions
- [ ] Configure error monitoring
- [ ] Document data retention policy
- [ ] Test rate limiting (if implemented)
- [ ] Review session timeout settings
