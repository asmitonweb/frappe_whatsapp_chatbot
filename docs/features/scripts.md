# Script Responses

Execute Python scripts to generate dynamic responses based on your database.

## Use Cases

- Check order status
- Look up customer information
- Query product availability
- Calculate prices or discounts
- Any database lookup

## Setting Up a Script Response

1. Create a flow step
2. Set **Message Type**: `Script`
3. Write your Python code in **Response Script**
4. Set the `response` variable with the message to send

## Available Variables

| Variable | Description |
|----------|-------------|
| `data` | Dictionary of all collected session data |
| `frappe` | Frappe module for database queries |
| `json` | JSON module |
| `session` | Current session document |
| `phone_number` | User's WhatsApp phone number |
| `response` | **Set this** with the message to send |

## Basic Example

```python
order_id = data.get('order_id')
if order_id:
    response = f"Looking up order {order_id}..."
else:
    response = "No order ID provided."
```

## Database Query Example

```python
order_id = data.get('order_id')

try:
    order = frappe.get_doc('Sales Order', order_id)
    response = f"""📦 Order Details:
Order ID: {order.name}
Status: {order.status}
Total: ₹{order.grand_total}
Date: {order.transaction_date}"""

except frappe.DoesNotExistError:
    response = f"Sorry, order '{order_id}' was not found."

except Exception as e:
    response = "Sorry, unable to fetch order details."
```

## Customer Lookup Example

```python
phone = phone_number

# Find customer by phone number
customer = frappe.db.get_value(
    'Customer',
    {'mobile_no': phone},
    ['name', 'customer_name', 'outstanding_amount'],
    as_dict=True
)

if customer:
    response = f"""👤 Customer Details:
Name: {customer.customer_name}
ID: {customer.name}
Outstanding: ₹{customer.outstanding_amount or 0}"""
else:
    response = "No customer found with this phone number."
```

## Product Availability Example

```python
item_code = data.get('product_code')

# Get stock quantity
stock = frappe.db.get_value(
    'Bin',
    {'item_code': item_code, 'warehouse': 'Main Warehouse - ABC'},
    'actual_qty'
) or 0

if stock > 0:
    response = f"✅ {item_code} is in stock! Available: {int(stock)} units"
else:
    response = f"❌ Sorry, {item_code} is currently out of stock."
```

## Conditional Response Example

```python
service_type = data.get('service_type', '').lower()
issue = data.get('issue_description', '')

if service_type == 'billing':
    response = """For billing issues:
📧 Email: billing@company.com
📞 Phone: 1800-123-4567
⏰ Mon-Fri, 9 AM - 6 PM"""

elif service_type == 'technical':
    # Create a support ticket
    ticket = frappe.get_doc({
        'doctype': 'Issue',
        'subject': f'WhatsApp Support: {issue[:50]}',
        'description': issue,
        'raised_by': phone_number
    })
    ticket.insert(ignore_permissions=True)
    frappe.db.commit()

    response = f"""🎫 Support ticket created!
Ticket ID: {ticket.name}
Our team will contact you within 24 hours."""

else:
    response = "Please specify your issue type: billing or technical"
```

## Error Handling

Always wrap database queries in try-except:

```python
try:
    # Your code here
    doc = frappe.get_doc('DocType', name)
    response = f"Found: {doc.field}"

except frappe.DoesNotExistError:
    response = "Record not found."

except frappe.PermissionError:
    response = "Access denied."

except Exception as e:
    # Log error for debugging
    frappe.log_error(f"Script error: {str(e)}", "WhatsApp Chatbot")
    response = "An error occurred. Please try again."
```

## Tips

1. **Always set `response`** - If you don't set it, the Message field will be used as fallback
2. **Keep it simple** - Complex logic is harder to debug
3. **Use logging** - Use `frappe.log_error()` for debugging
4. **Handle all cases** - Always have an else/except for edge cases
5. **Test thoroughly** - Test with various inputs before going live

## Debugging

Check the Error Log in Frappe Desk:
1. Go to **Error Log**
2. Filter by "WhatsApp Chatbot"
3. Look for `FlowEngine run_response_script error`

Add debug logging:
```python
frappe.log_error(f"Debug: order_id={data.get('order_id')}", "Chatbot Debug")
```
