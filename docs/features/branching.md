# Conditional Branching

Create different conversation paths based on user input.

## How It Works

Use **Conditional Next** in a flow step to route users to different steps based on their response.

## Setup

1. Create a step with **Input Type**: `Select` (or any input type)
2. Set **Store As** to save the response
3. Add **Conditional Next** JSON mapping responses to step names

## Conditional Next Format

```json
{
  "option1": "step_for_option1",
  "option2": "step_for_option2",
  "default": "fallback_step"
}
```

- Keys are matched against user input (case-insensitive)
- `default` is used when no other key matches
- If no match and no default, goes to next step by order

## Example: Support Type Routing

### Step 1: Ask Issue Type

```
Step Name: ask_issue_type
Message: What type of issue do you have?
Input Type: Select
Options: Billing|Technical|General
Store As: issue_type
Conditional Next:
{
  "billing": "billing_response",
  "technical": "tech_collect_details",
  "general": "general_response"
}
```

### Step 2a: Billing Response

```
Step Name: billing_response
Message: For billing issues, please email billing@company.com or call 1800-123-4567.
Input Type: None
```

### Step 2b: Technical - Collect Details

```
Step Name: tech_collect_details
Message: Please describe your technical issue in detail.
Input Type: Text
Store As: tech_issue
Next Step: tech_response
```

### Step 2c: Tech Response

```
Step Name: tech_response
Message: Thanks! A technician will contact you within 2 hours.
Input Type: None
```

### Step 2d: General Response

```
Step Name: general_response
Message: Please describe your question and we'll get back to you.
Input Type: Text
Store As: general_query
```

## Flow Diagram

```
                    ┌─────────────────┐
                    │  ask_issue_type │
                    │  (Select)       │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐  ┌─────────────────┐  ┌───────────────┐
│billing_response│  │tech_collect_    │  │general_       │
│               │  │details          │  │response       │
└───────────────┘  └────────┬────────┘  └───────────────┘
                            ▼
                   ┌────────────────┐
                   │ tech_response  │
                   └────────────────┘
```

## Skip Conditions

Skip steps based on previously collected data using **Skip Condition**.

### Example: Skip Email If Already Provided

```
Step Name: ask_email
Message: What's your email address?
Input Type: Email
Store As: email
Skip Condition: data.get('email') is not None
```

### Skip Condition Variables

- `data` - Dictionary of all collected values
- Standard Python expressions

### Examples

```python
# Skip if email already exists
data.get('email') is not None

# Skip if user is VIP
data.get('customer_type') == 'vip'

# Skip if order total is below threshold
float(data.get('order_total', 0)) < 1000
```

## Tips

1. **Always have a default** - Prevents users from getting stuck
2. **Test all paths** - Verify each branch works correctly
3. **Keep it simple** - Complex branching is hard to maintain
4. **Document your flows** - Draw diagrams for complex flows
