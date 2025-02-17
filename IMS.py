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
def add_item(name, quantity, purchase_quantity, shelf_life_days, cost_per_unit, date_added):
    st.session_state.item_count += 1
    item_id = st.session_state.item_count  # Unique item ID
    balance_quantity = quantity + purchase_quantity  # No consumption during inward
    expiry_date = date_added + timedelta(days=shelf_life_days)  # Calculate expiry date
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
        "Date Added": date_added.strftime("%Y-%m-%d"),  # Track the date the item was added
    }
    st.session_state.inventory.append(item)

# Function to issue material from inventory
def issue_material(item_id, issue_quantity, date_issued):
    for item in st.session_state.inventory:
        if item["Item ID"] == item_id:
            if item["Balance Quantity"] >= issue_quantity:
                item["Balance Quantity"] -= issue_quantity
                item["Total Cost"] = item["Cost Per Unit"] * item["Balance Quantity"]
                item["Date Issued"] = date_issued.strftime("%Y-%m-%d")  # Track the date the item was issued
                st.success(f"Issued {issue_quantity} units of '{item['Name']}' on {date_issued.strftime('%Y-%m-%d')}.")
            else:
                st.error(f"Insufficient stock for '{item['Name']}'. Available: {item['Balance Quantity']}")

# Function to calculate inventory status for a specific date
def calculate_inventory_status(selected_date):
    updated_inventory = []
    for item in st.session_state.inventory:
        # Check if the item was added on or before the selected date
        date_added = datetime.strptime(item["Date Added"], "%Y-%m-%d")
        if date_added <= selected_date:
            # Check if the item was issued on or before the selected date
            if "Date Issued" in item:
                date_issued = datetime.strptime(item["Date Issued"], "%Y-%m-%d")
                if date_issued <= selected_date:
                    balance_quantity = item["Balance Quantity"]
                else:
                    balance_quantity = item["Initial Quantity"] + item["Purchase Quantity"]
            else:
                balance_quantity = item["Initial Quantity"] + item["Purchase Quantity"]
            
            # Check if the item has expired by the selected date
            expiry_date = datetime.strptime(item["Expiry Date"], "%Y-%m-%d")
            status = "Usable" if expiry_date > selected_date else "Expired"
            
            updated_item = item.copy()
            updated_item["Balance Quantity"] = balance_quantity
            updated_item["Status"] = status
            updated_inventory.append(updated_item)
    return updated_inventory

# Function to calculate wastage and loss
def calculate_wastage(inventory):
    wastage_items = [item for item in inventory if item["Status"] == "Expired"]
    total_wastage_quantity = sum(item["Balance Quantity"] for item in wastage_items)
    total_loss = sum(item["Total Cost"] for item in wastage_items)
    return wastage_items, total_wastage_quantity, total_loss

# Sidebar for adding new items (Inward)
with st.sidebar:
    st.header("Inward")
    date_added = st.date_input("Date", value=datetime.now())
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
                add_item(name, quantity, purchase_quantity, shelf_life_days, cost_per_unit, date_added)
                st.success(f"Item '{name}' added to inventory on {date_added.strftime('%Y-%m-%d')}!")
            else:
                st.error("Please enter a valid item name.")

# Sidebar for issuing materials
with st.sidebar:
    st.header("Issue Material")
    if st.session_state.inventory:
        date_issued = st.date_input("Date", value=datetime.now(), key="issue_date")
        item_names = [item["Name"] for item in st.session_state.inventory]
        selected_item = st.selectbox("Select Item to Issue", item_names)
        issue_quantity = st.number_input("Issue Quantity", min_value=1, step=1)

        if st.button("Issue"):
            selected_item_id = next(item["Item ID"] for item in st.session_state.inventory if item["Name"] == selected_item)
            issue_material(selected_item_id, issue_quantity, date_issued)

# Select date to view inventory status
selected_date = st.date_input("Select Date to View Inventory Status", value=datetime.now())

# Calculate inventory status for the selected date
updated_inventory = calculate_inventory_status(selected_date)

# Display the inventory as of the selected date
st.header(f"Status of Inventory on {selected_date.strftime('%Y-%m-%d')}")
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
