# Troubleshooting

## Common Issues

### Chatbot Not Responding

**Symptoms:** Messages received but no bot response

**Check:**

1. **Is chatbot enabled?**
   - Go to WhatsApp Chatbot settings
   - Ensure **Enabled** is checked

2. **Is the account configured?**
   - Either enable **Process All Accounts**
   - Or select the specific **WhatsApp Account**

3. **Is the number excluded?**
   - Check **Excluded Numbers** in settings

4. **Business hours?**
   - If **Business Hours Only** is enabled, check the time range

5. **Check Error Log**
   - Go to Error Log in Frappe
   - Filter by "WhatsApp Chatbot"

---

### Keywords Not Matching

**Symptoms:** Keyword reply not triggered

**Check:**

1. **Is the rule enabled?**
   - Check **Enabled** checkbox

2. **Match Type correct?**
   - `Exact` requires exact match
   - Try `Contains` for partial match

3. **Case sensitivity?**
   - By default, matching is case-insensitive
   - Check **Case Sensitive** setting

4. **Priority conflicts?**
   - Higher priority rules match first
   - Check if another rule is matching

5. **Date range?**
   - Check **Active From** / **Active Until**

---

### Flow Not Triggering

**Symptoms:** Flow trigger keyword doesn't start flow

**Check:**

1. **Is flow enabled?**
   - Check **Enabled** in the flow

2. **Trigger keywords correct?**
   - Keywords are comma-separated
   - Matching is case-insensitive

3. **Active session exists?**
   - User might have an existing active session
   - Check WhatsApp Chatbot Session for active sessions

4. **Account filter?**
   - Check if flow is restricted to specific account

---

### Session Data Not Saving

**Symptoms:** Variables not captured, document creation fails

**Check:**

1. **Store As field filled?**
   - Each data collection step needs **Store As**
   - Variable names are case-sensitive

2. **Input Type correct?**
   - Steps with **Input Type: None** don't collect data
   - Use Text, Number, Email, etc.

3. **Validation failing?**
   - Check if input validation is rejecting responses
   - Check **Max Retries** setting

---

### Script Response Not Working

**Symptoms:** Script message type not executing

**Check:**

1. **Message Type is Script?**
   - Must be set to **Script**, not Text

2. **`response` variable set?**
   - Script must set: `response = "your message"`

3. **Check Error Log**
   - Look for "FlowEngine run_response_script error"

4. **Syntax errors?**
   - Test your script in bench console first

---

### Document Not Created

**Symptoms:** Flow completes but no document created

**Check:**

1. **On Complete Action set?**
   - Must be **Create Document**

2. **DocType selected?**
   - **Create DocType** must be set

3. **Field Mapping correct?**
   ```json
   {
     "doctype_field": "flow_variable"
   }
   ```

4. **Variables exist?**
   - Check Error Log for "Variable 'x' not found"
   - Verify **Store As** matches mapping

5. **DocType permissions?**
   - Chatbot creates with `ignore_permissions=True`
   - But check for validation errors

---

### AI Not Responding

**Symptoms:** AI fallback not working

**Check:**

1. **AI enabled?**
   - Enable **Enable AI** in settings

2. **API key valid?**
   - Check **AI API Key**
   - Verify with provider dashboard

3. **Library installed?**
   ```bash
   pip install openai   # For OpenAI
   pip install anthropic  # For Anthropic
   ```

4. **Model name correct?**
   - OpenAI: `gpt-4o-mini`, `gpt-4o`
   - Anthropic: `claude-3-haiku-20240307`

5. **Check Error Log**
   - Look for "OpenAI API error" or "Anthropic API error"

---

## Debugging

### View Error Logs

1. Go to **Error Log** in Frappe
2. Filter by title containing "WhatsApp Chatbot"
3. Check the traceback for details

### Add Debug Logging

In your scripts:
```python
frappe.log_error(f"Debug: value={some_value}", "Chatbot Debug")
```

### Test in Console

```bash
bench --site your-site console
```

```python
# Test keyword matcher
from frappe_whatsapp_chatbot.chatbot.keyword_matcher import KeywordMatcher
matcher = KeywordMatcher("Default")
match = matcher.match("hello")
print(match)

# Check active sessions
frappe.get_all('WhatsApp Chatbot Session', filters={'status': 'Active'})
```

### Check Session Data

```python
session = frappe.get_doc('WhatsApp Chatbot Session', 'SESSION-00001')
import json
print(json.loads(session.session_data))
```

---

## Error Reference

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `WhatsApp Chatbot Error` | General processing error | Check Error Log for stack trace |
| `WhatsApp Chatbot Script Error` | Server Script execution failed | Review script syntax and variables |
| `App X is not installed` | Script name doesn't exist | Use Server Script name, not api_method |
| `Account Name is required` | Missing WhatsApp Account config | Configure WhatsApp Account properly |
| `Failed to send message` | WhatsApp API error | Check token validity, phone format |
| `AI Fallback error` | AI provider API failed | Check API key and model name |
| `FlowEngine error` | Flow processing failed | Check flow configuration and steps |

### Error Log Categories

Filter Error Log by these titles:

| Title | Component |
|-------|-----------|
| `WhatsApp Chatbot Error` | Main processor |
| `WhatsApp Chatbot Script Error` | Script execution |
| `WhatsApp Flow Error` | Flow engine |
| `AI Fallback error` | AI responder |
| `cleanup_expired_sessions error` | Session cleanup |

### Interpreting Stack Traces

Common patterns in stack traces:

**Missing variable:**
```
KeyError: 'order_id'
```
→ Variable not collected or wrong name in mapping

**Invalid document:**
```
frappe.DoesNotExistError: DocType Customer with name CUST-001 does not exist
```
→ Referenced document doesn't exist

**Permission error:**
```
frappe.PermissionError
```
→ Check doctype permissions or use `ignore_permissions=True`

**Validation error:**
```
frappe.ValidationError: Mobile No is required
```
→ Required field missing in document creation

---

## Performance Issues

### Slow Responses

**Check:**
1. AI response time (3-10s is normal)
2. Database query performance
3. External API call timeouts

**Solutions:**
- Reduce conversation history length
- Optimize DocType query filters
- Increase worker count

### Messages Piling Up

**Check:**
1. Worker status: `bench doctor`
2. Redis connection: `redis-cli ping`
3. Queue length: `bench show-pending-jobs`

**Solutions:**
- Restart workers: `bench restart`
- Add more workers
- Check for blocking operations in scripts

---

## Getting Help

1. Check this documentation
2. Search Error Log for specific errors
3. Review [Security Guide](security.md) for script issues
4. Check [Production Guide](../deployment.md) for deployment issues
5. Open an issue on GitHub: https://github.com/shridarpatil/frappe_whatsapp_chatbot/issues
