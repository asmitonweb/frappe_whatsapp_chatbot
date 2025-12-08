# Session Management

Track and manage conversation sessions.

## How Sessions Work

1. User triggers a flow → Session created with status "Active"
2. User responds → Session updated, moves to next step
3. Flow completes → Session marked "Completed"
4. User cancels or times out → Session marked "Cancelled" or "Timeout"

## Session States

| Status | Description |
|--------|-------------|
| **Active** | Flow in progress, waiting for user input |
| **Completed** | Flow finished successfully |
| **Cancelled** | User cancelled (typed cancel keyword) |
| **Timeout** | Session expired due to inactivity |

## Session Timeout

Configure in **WhatsApp Chatbot** settings:

- **Session Timeout (Minutes)**: Default 30 minutes
- Inactive sessions are marked as "Timeout"
- Timeout message is sent (configured in flow)

## Cancel Keywords

Users can cancel a flow by typing cancel keywords:

Default: `cancel, stop, quit, exit`

Configure per-flow in **WhatsApp Chatbot Flow** → **Cancel Keywords**

## Viewing Sessions

Go to **WhatsApp Chatbot Session** to see:

- Phone number
- Current flow
- Current step
- Session data (collected values)
- Status
- Start/end times

## Session Data

All collected values are stored in **Session Data** as JSON:

```json
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "issue_type": "technical"
}
```

## Message History

Each session tracks messages in **Session Messages** child table:

- Direction (Incoming/Outgoing)
- Message content
- Step name
- Timestamp

## Cleanup

Expired sessions are cleaned up hourly by the scheduler:

```python
# hooks.py
scheduler_events = {
    "hourly": [
        "frappe_whatsapp_chatbot.chatbot.session_manager.cleanup_expired_sessions"
    ]
}
```

## Manual Session Management

### Clear Active Session

If a user is stuck, you can manually cancel their session:

1. Go to **WhatsApp Chatbot Session**
2. Find the active session for the phone number
3. Change **Status** to "Cancelled"
4. Save

### Restart Flow

To let a user restart:
1. Cancel their current session (if any)
2. They can type the trigger keyword again

## Debugging

### Check Active Sessions

```python
# In bench console
frappe.get_all(
    'WhatsApp Chatbot Session',
    filters={'status': 'Active'},
    fields=['phone_number', 'current_flow', 'current_step']
)
```

### Check Session Data

```python
session = frappe.get_doc('WhatsApp Chatbot Session', 'SESSION-00001')
print(session.session_data)
```
