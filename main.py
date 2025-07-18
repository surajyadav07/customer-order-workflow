from typing import List, Literal, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from datetime import datetime
from IPython.display import Image, display

memory = MemorySaver()

class Order(TypedDict):
    order_id: int
    customer_id: int
    amount: float
    status: Literal["pending", "shipped", "delivered", "cancelled"]
    timestamp: str

class OrderState(TypedDict):
    orders: List[Order]
    history: List[str]

def validate_order(order: Order) -> bool:
    try:
        return (isinstance(order["order_id"], int) and order["order_id"] > 0 and
                isinstance(order["customer_id"], int) and order["customer_id"] > 0 and
                isinstance(order["amount"], float) and order["amount"] >= 0 and
                order["status"] in ["pending", "shipped", "delivered", "cancelled"] and
                datetime.strptime(order["timestamp"], "%Y-%m-%d %H:%M:%S"))
    except (KeyError, ValueError):
        return False

def process_order(state: OrderState) -> OrderState:
    latest_order = state["orders"][-1]
    if not validate_order(latest_order):
        state["history"].append(f"{latest_order['timestamp']}: Invalid order {latest_order['order_id']}")
        return state
    state["history"].append(f"{latest_order['timestamp']}: Processed order {latest_order['order_id']} as {latest_order['status']}")
    return state

def update_status(state: OrderState) -> OrderState:
    latest_order = state["orders"][-1]
    current_status = latest_order["status"]
    valid_transitions = {
        "pending": ["shipped", "cancelled"],
        "shipped": ["delivered"],
        "delivered": [],
        "cancelled": []
    }
    if current_status not in valid_transitions:
        state["history"].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Invalid status {current_status}")
        return state
    new_status = state["orders"][-1]["status"]  # Assume new status is in latest order
    if new_status not in valid_transitions[current_status]:
        state["history"].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Invalid transition from {current_status} to {new_status}")
        return state
    state["history"].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Updated order {latest_order['order_id']} to {new_status}")
    return state

def query_orders(state: OrderState, status: str) -> List[Order]:
    if status not in ["pending", "shipped", "delivered", "cancelled"]:
        return []
    return [order for order in state["orders"] if order["status"] == status and validate_order(order)]

def route_order(state: OrderState) -> str:
    latest_order = state["orders"][-1]
    if not validate_order(latest_order):
        return END
    if latest_order["status"] in ["delivered", "cancelled"]:
        return END
    return "update_status"

builder = StateGraph(OrderState)
builder.add_node("process_order", process_order)
builder.add_node("update_status", update_status)
builder.add_edge(START, "process_order")
builder.add_conditional_edges("process_order", route_order, {"update_status": "update_status", END: END})
builder.add_edge("update_status", END)

graph = builder.compile(checkpointer=memory)

display(Image(graph.get_graph().draw_mermaid_png()))

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "1"}}
    initial_state = {
        "orders": [
            {"order_id": 1, "customer_id": 101, "amount": 99.99, "status": "pending", "timestamp": "2025-07-18 10:00:00"}
        ],
        "history": []
    }
    result = graph.invoke(initial_state, config)
    print("State after processing:", result)
    # Query example
    shipped_orders = query_orders(result, "shipped")
    print("Shipped orders:", shipped_orders)