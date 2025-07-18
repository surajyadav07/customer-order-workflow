# Customer Order Processing Workflow

## Overview
This project implements a customer order processing workflow using Python and LangGraph. It manages orders with status transitions (pending, shipped, delivered, cancelled), validates transitions, tracks history, and supports querying orders by status.

## Features
- Manage orders with ID, customer ID, amount, status, and timestamp.
- Validate status transitions (e.g., pending → shipped → delivered).
- Maintain order history with timestamps.
- Query orders by status.
- Persist state using `MemorySaver`.
- Visualize workflow graph.

## Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd customer-order-processing-workflow
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage
- The script initializes a sample order and processes it through the workflow.
- Modify `initial_state` in `main.py` to test different orders.
- Use `query_orders(state, status)` to retrieve orders by status (e.g., "shipped").

## Example
```python
initial_state = {
    "orders": [
        {"order_id": 1, "customer_id": 101, "amount": 99.99, "status": "pending", "timestamp": "2025-07-18 10:00:00"}
    ],
    "history": []
}
result = graph.invoke(initial_state, config)
```

## License
MIT