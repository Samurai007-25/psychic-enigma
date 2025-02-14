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
def add_item(name, quantity, purchase_quantity, consumption_quantity, shelf_life_days, cost_per_unit):
    st.session_state.item_count += 1
    item_id = st.session_state.item_count  # Unique item ID
    balance_quantity = quantity + purchase_quantity - consumption_quantity
    expiry_date = datetime.now() + timedelta(days=shelf_life_days)  # Calculate expiry date
    item = {
        "Item ID": item_id,
        "Name": name,
        "Initial Quantity": quantity,
        "Purchase Quantity": purchase_quantity,
        "Consumption Quantity": consumption_quantity,
        "Balance Quantity": balance_quantity,
        "Shelf Life (Days)": shelf_life_days,
        "Expiry Date": expiry_date.strftime("%Y-%m-%d"),  # Format expiry date
        "Cost Per Unit": cost_per_unit,
        "Total Cost": cost_per_unit * balance_quantity,
        "Status": "Usable" if expiry_date > datetime.now() else "Expired",
    }
    st.session_state.inventory.append(item)

# Function to calculate inventory status for a specific date
def calculate_inventory_status(selected_date):
    updated_inventory = []
    for item in st.session_state.inventory:
        expiry_date = datetime.strptime(item["Expiry Date"], "%Y-%m-%d")
        status = "Usable" if expiry_date > selected_date else "Expired"
        updated_item = item.copy()
        updated_item["Status"] = status
        updated_inventory.append(updated_item)
    return updated_inventory

# Function to calculate wastage and loss
def calculate_wastage(inventory):
    wastage_items = [item for item in inventory if item["Status"] == "Expired"]
    total_wastage_quantity = sum(item["Balance Quantity"] for item in wastage_items)
    total_loss = sum(item["Total Cost"] for item in wastage_items)
    return wastage_items, total_wastage_quantity, total_loss

# Sidebar for adding new items
with st.sidebar:
    st.header("Add Items")
    num_items = st.number_input("Number of Items to Add", min_value=1, step=1)

    for i in range(num_items):
        st.subheader(f"Item {i + 1}")
        name = st.text_input(f"Item Name {i + 1}", key=f"name_{i}")
        quantity = st.number_input(f"Initial Quantity {i + 1}", min_value=0, step=1, key=f"quantity_{i}")
        purchase_quantity = st.number_input(f"Purchase Quantity {i + 1}", min_value=0, step=1, key=f"purchase_{i}")
        consumption_quantity = st.number_input(f"Consumption Quantity {i + 1}", min_value=0, step=1, key=f"consumption_{i}")
        shelf_life_days = st.number_input(f"Shelf Life (Days) {i + 1}", min_value=1, step=1, key=f"shelf_life_{i}")
        cost_per_unit = st.number_input(f"Cost Per Unit {i + 1}", min_value=0.0, step=0.01, key=f"cost_{i}")

        if st.button(f"Add Item {i + 1}"):
            if name:  # Check if the name is not empty
                add_item(name, quantity, purchase_quantity, consumption_quantity, shelf_life_days, cost_per_unit)
                st.success(f"Item '{name}' added to inventory!")
            else:
                st.error("Please enter a valid item name.")

# Date selection for inventory status
st.header("Inventory Status")
selected_date = st.date_input("Select a date to view inventory status", min_value=datetime.now())

# Calculate inventory status for the selected date
updated_inventory = calculate_inventory_status(selected_date)

# Display the inventory as of the selected date
st.subheader(f"Inventory as on {selected_date.strftime('%d/%m/%Y')}")
if updated_inventory:
    # Convert inventory to a DataFrame for tabular display
    inventory_df = pd.DataFrame(updated_inventory)
    st.table(inventory_df)

    # Calculate wastage and loss
    wastage_items, total_wastage_quantity, total_loss = calculate_wastage(updated_inventory)
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
