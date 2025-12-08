# Document Creation

Automatically create Frappe documents when a conversation flow completes.

## Setup

1. Edit your **WhatsApp Chatbot Flow**
2. Set **On Complete Action**: `Create Document`
3. Select the **Create DocType** (e.g., Lead, Issue, Customer)
4. Configure **Field Mapping**
5. Save

## Field Mapping

Map flow variables to DocType fields using JSON:

```json
{
  "doctype_field": "flow_variable",
  "another_field": "another_variable"
}
```

### Example: Create Lead

Flow steps collect:
- `customer_name` (Store As)
- `customer_email` (Store As)
- `company_name` (Store As)

Field Mapping:
```json
{
  "lead_name": "customer_name",
  "email_id": "customer_email",
  "company_name": "company_name"
}
```

### Example: Create Issue

Flow steps collect:
- `issue_subject` (Store As)
- `issue_description` (Store As)

Field Mapping:
```json
{
  "subject": "issue_subject",
  "description": "issue_description"
}
```

## Adding Extra Fields

You can add static values by creating them in the script action instead:

```python
# On Complete Action: Run Script

doc = frappe.get_doc({
    'doctype': 'Lead',
    'lead_name': data.get('customer_name'),
    'email_id': data.get('customer_email'),
    'source': 'WhatsApp',  # Static value
    'status': 'Open'       # Static value
})
doc.insert(ignore_permissions=True)
frappe.db.commit()
```

## Troubleshooting

### Document Not Created

Check Error Log for:
- `create_document: Missing doctype or field_mapping`
- `create_document: Variable 'x' not found in session data`
- `create_document: No data mapped`

### Variable Not Found

Ensure:
1. **Store As** field is filled in flow steps
2. Variable names match exactly (case-sensitive)
3. **Input Type** is not "None" for data collection steps

### Validation Errors

If the DocType has required fields or validation:
- Ensure all required fields are mapped
- Check field types match (e.g., don't put text in a number field)

## Checking Logs

1. Go to **Error Log** in Frappe Desk
2. Filter by title containing "WhatsApp Chatbot"
3. Look for success: `create_document: Successfully created...`
4. Look for errors: `FlowEngine create_document error...`
