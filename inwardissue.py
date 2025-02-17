import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Title of the app
st.title("Inventory Management System")

# Initialize session state to store inventory and item count
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "item_count" not in st.session_state:
    st.session_state.item_count = 0

# Function to add an item to the inventory
def add_item(name, quantity, purchase_quantity, shelf_life_days, cost_per_unit):
    st.session_state.item_count += 1
    item_id = st.session_state.item_count  # Unique item ID
    balance_quantity = quantity + purchase_quantity  # No consumption during inward
    expiry_date = datetime.now() + timedelta(days=shelf_life_days)  # Calculate expiry date
    item = {
        "Item ID": item_id,
        "Name": name,
        "Initial Quantity": quantity,
        "Purchase Quantity": purchase_quantity,
        "Balance Quantity": balance_quantity,
        "Shelf Life (Days)": shelf_life_days,
        "Expiry Date": expiry_date.strftime("%Y-%m-%d"),  # Format expiry date
        "Cost Per Unit": cost_per_unit,
        "Total Cost": cost_per_unit * balance_quantity,
        "Status": "Usable" if expiry_date > datetime.now() else "Expired",
    }
    st.session_state.inventory.append(item)

# Function to issue material from inventory
def issue_material(item_id, issue_quantity):
    for item in st.session_state.inventory:
        if item["Item ID"] == item_id:
            if item["Balance Quantity"] >= issue_quantity:
                item["Balance Quantity"] -= issue_quantity
                item["Total Cost"] = item["Cost Per Unit"] * item["Balance Quantity"]
                st.success(f"Issued {issue_quantity} units of '{item['Name']}'.")
            else:
                st.error(f"Insufficient stock for '{item['Name']}'. Available: {item['Balance Quantity']}")

# Function to calculate wastage and loss
def calculate_wastage():
    wastage_items = [item for item in st.session_state.inventory if item["Status"] == "Expired"]
    total_wastage_quantity = sum(item["Balance Quantity"] for item in wastage_items)
    total_loss = sum(item["Total Cost"] for item in wastage_items)
    return wastage_items, total_wastage_quantity, total_loss

# Sidebar for adding new items (Inward)
with st.sidebar:
    st.header("Inward")
    num_items = st.number_input("Number of Items to Add", min_value=1, step=1)

    for i in range(num_items):
        st.subheader(f"Item {i + 1}")
        name = st.text_input(f"Item Name {i + 1}", key=f"name_{i}")
        quantity = st.number_input(f"Initial Quantity {i + 1}", min_value=0, step=1, key=f"quantity_{i}")
        purchase_quantity = st.number_input(f"Purchase Quantity {i + 1}", min_value=0, step=1, key=f"purchase_{i}")
        shelf_life_days = st.number_input(f"Shelf Life (Days) {i + 1}", min_value=1, step=1, key=f"shelf_life_{i}")
        cost_per_unit = st.number_input(f"Cost Per Unit {i + 1}", min_value=0.0, step=0.01, key=f"cost_{i}")

        if st.button(f"Add Item {i + 1}"):
            if name:  # Check if the name is not empty
                add_item(name, quantity, purchase_quantity, shelf_life_days, cost_per_unit)
                st.success(f"Item '{name}' added to inventory!")
            else:
                st.error("Please enter a valid item name.")

# Sidebar for issuing materials
with st.sidebar:
    st.header("Issue Material")
    if st.session_state.inventory:
        item_names = [item["Name"] for item in st.session_state.inventory]
        selected_item = st.selectbox("Select Item to Issue", item_names)
        issue_quantity = st.number_input("Issue Quantity", min_value=1, step=1)

        if st.button("Issue"):
            selected_item_id = next(item["Item ID"] for item in st.session_state.inventory if item["Name"] == selected_item)
            issue_material(selected_item_id, issue_quantity)

# Display the current inventory in a table
st.header("Current Inventory")
if st.session_state.inventory:
    # Convert inventory to a DataFrame for tabular display
    inventory_df = pd.DataFrame(st.session_state.inventory)
    st.table(inventory_df)

    # Calculate wastage and loss
    wastage_items, total_wastage_quantity, total_loss = calculate_wastage()
    if wastage_items:
        st.subheader("Wastage Details")
        wastage_df = pd.DataFrame(wastage_items)
        st.table(wastage_df)
        st.write(f"Total Wastage Quantity: {total_wastage_quantity}")
        st.write(f"Total Loss Due to Wastage: ${total_loss:.2f}")
    else:
        st.info("No items have expired yet.")
else:
    st.info("No items in the inventory yet. Add items using the sidebar.")
