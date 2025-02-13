import streamlit as st
import pandas as pd

# Title of the app
st.title("Inventory Management System")

# Initialize session state to store inventory and item count
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "item_count" not in st.session_state:
    st.session_state.item_count = 0

# Function to add an item to the inventory
def add_item(name, quantity, purchase_quantity, consumption_quantity):
    st.session_state.item_count += 1
    item_id = st.session_state.item_count  # Unique item ID
    balance_quantity = quantity + purchase_quantity - consumption_quantity
    item = {
        "Item ID": item_id,
        "Name": name,
        "Initial Quantity": quantity,
        "Purchase Quantity": purchase_quantity,
        "Consumption Quantity": consumption_quantity,
        "Balance Quantity": balance_quantity,
    }
    st.session_state.inventory.append(item)

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

        if st.button(f"Add Item {i + 1}"):
            if name:  # Check if the name is not empty
                add_item(name, quantity, purchase_quantity, consumption_quantity)
                st.success(f"Item '{name}' added to inventory!")
            else:
                st.error("Please enter a valid item name.")

# Display the current inventory in a table
st.header("Current Inventory")
if st.session_state.inventory:
    # Convert inventory to a DataFrame for tabular display
    inventory_df = pd.DataFrame(st.session_state.inventory)
    st.table(inventory_df)
else:
    st.info("No items in the inventory yet. Add items using the sidebar.")
