# Production Deployment Guide

This guide covers best practices for deploying the WhatsApp Chatbot in production.

## Pre-Deployment Checklist

### Configuration

- [ ] WhatsApp Account configured with valid token
- [ ] Chatbot enabled in settings
- [ ] Default response message set
- [ ] Business hours configured (if needed)
- [ ] Session timeout set appropriately (default: 30 mins)

### Testing

- [ ] All keyword replies tested
- [ ] All conversation flows tested end-to-end
- [ ] Document creation verified
- [ ] AI responses tested (if enabled)
- [ ] Error scenarios handled gracefully

### Security

- [ ] Server Scripts reviewed (see [Security Guide](reference/security.md))
- [ ] API endpoints verified (HTTPS only)
- [ ] Role permissions configured
- [ ] Excluded numbers list updated

## Infrastructure Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| Frappe/ERPNext | v15+ |
| Python | 3.10+ |
| Redis | Required for queues |
| Workers | At least 1 default worker |

### Recommended for Production

| Component | Recommendation |
|-----------|----------------|
| Workers | 2-4 default workers |
| Redis | Dedicated Redis instance |
| Database | PostgreSQL or MariaDB with replication |
| Monitoring | Error log monitoring enabled |

## Scaling Considerations

### High Volume Messaging

For high message volumes (>1000/day):

1. **Increase workers**
   ```bash
   bench config set workers 4
   ```

2. **Separate queue for chatbot** (optional)
   ```python
   # In hooks.py, use dedicated queue
   frappe.enqueue(..., queue="chatbot")
   ```

3. **Database indexing**
   ```sql
   -- Add index for session lookups
   CREATE INDEX idx_session_phone ON `tabWhatsApp Chatbot Session` (phone_number, status);
   ```

### AI Integration

If using AI responses:

1. **Set appropriate token limits** to control costs
2. **Cache common responses** where possible
3. **Monitor API usage** in provider dashboard
4. **Set rate limits** to prevent abuse

## Monitoring

### Error Logs

Monitor these error categories:

| Error Type | Action |
|------------|--------|
| `WhatsApp Chatbot Error` | Check processor issues |
| `WhatsApp Chatbot Script Error` | Review Server Scripts |
| `WhatsApp Flow Error` | Check flow configuration |

### Key Metrics to Track

1. **Response rate** - % of messages that got a response
2. **Error rate** - Errors per 100 messages
3. **Session completion rate** - Flows completed vs started
4. **AI fallback rate** - Messages handled by AI

### Setting Up Monitoring

Create a daily digest report:

```python
# Server Script: Daily Chatbot Report
import frappe
from frappe.utils import add_days, nowdate

yesterday = add_days(nowdate(), -1)

stats = {
    "messages_received": frappe.db.count("WhatsApp Message", {
        "type": "Incoming",
        "creation": (">=", yesterday)
    }),
    "messages_sent": frappe.db.count("WhatsApp Message", {
        "type": "Outgoing",
        "creation": (">=", yesterday)
    }),
    "sessions_started": frappe.db.count("WhatsApp Chatbot Session", {
        "creation": (">=", yesterday)
    }),
    "errors": frappe.db.count("Error Log", {
        "creation": (">=", yesterday),
        "method": ("like", "%WhatsApp Chatbot%")
    })
}

frappe.sendmail(
    recipients=["admin@example.com"],
    subject=f"Chatbot Daily Report - {yesterday}",
    message=f"""
    Messages Received: {stats['messages_received']}
    Messages Sent: {stats['messages_sent']}
    Sessions Started: {stats['sessions_started']}
    Errors: {stats['errors']}
    """
)
```

## Backup & Recovery

### What to Backup

1. **DocType data**
   - WhatsApp Chatbot (settings)
   - WhatsApp Keyword Reply
   - WhatsApp Chatbot Flow
   - WhatsApp Flow Step
   - WhatsApp AI Context

2. **Server Scripts** used by chatbot

3. **WhatsApp Account** configuration

### Backup Command

```bash
# Backup specific doctypes
bench --site yoursite backup --include-doctypes "WhatsApp Keyword Reply,WhatsApp Chatbot Flow"
```

### Recovery Steps

1. Restore database backup
2. Verify WhatsApp Account token is valid
3. Test one keyword reply
4. Test one flow end-to-end
5. Enable chatbot in settings

## Maintenance

### Regular Tasks

| Task | Frequency | Command/Action |
|------|-----------|----------------|
| Clear old sessions | Weekly | See cleanup script below |
| Review error logs | Daily | Desk > Error Log |
| Check API token expiry | Monthly | WhatsApp Account |
| Update AI context | As needed | WhatsApp AI Context |

### Session Cleanup Script

```python
# Scheduler Event: Weekly
import frappe
from frappe.utils import add_days, nowdate

# Delete completed sessions older than 30 days
old_date = add_days(nowdate(), -30)
old_sessions = frappe.get_all("WhatsApp Chatbot Session",
    filters={
        "status": ["in", ["Completed", "Timeout", "Cancelled"]],
        "creation": ("<", old_date)
    },
    pluck="name"
)

for session in old_sessions:
    frappe.delete_doc("WhatsApp Chatbot Session", session, force=True)

frappe.db.commit()
```

### Updating Chatbot

When updating the app:

1. **Backup first**
   ```bash
   bench --site yoursite backup
   ```

2. **Update app**
   ```bash
   bench update --apps frappe_whatsapp_chatbot
   ```

3. **Run migrations**
   ```bash
   bench --site yoursite migrate
   ```

4. **Test critical flows**

## Troubleshooting Production Issues

### Messages Not Being Processed

1. Check workers are running:
   ```bash
   bench doctor
   ```

2. Check Redis connection:
   ```bash
   redis-cli ping
   ```

3. Verify chatbot is enabled:
   ```
   Desk > WhatsApp Chatbot > Enabled = Yes
   ```

### High Error Rate

1. Check Error Log for patterns
2. Verify WhatsApp token is valid
3. Check API endpoint availability
4. Review recent configuration changes

### Slow Responses

1. Check worker queue length:
   ```bash
   bench show-pending-jobs
   ```

2. Monitor database performance
3. Check AI API response times
4. Consider adding more workers

## Rollback Procedure

If issues arise after update:

1. **Stop workers**
   ```bash
   sudo supervisorctl stop all
   ```

2. **Restore backup**
   ```bash
   bench --site yoursite restore /path/to/backup.sql.gz
   ```

3. **Rollback code**
   ```bash
   cd apps/frappe_whatsapp_chatbot
   git checkout <previous-version>
   ```

4. **Restart**
   ```bash
   bench migrate
   sudo supervisorctl start all
   ```
