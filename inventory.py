import streamlit as st

# Title of the app
st.title("Inventory Management System")

# Initialize session state to store inventory
if "inventory" not in st.session_state:
    st.session_state.inventory = []

# Function to add an item to the inventory
def add_item(name, quantity, purchase_quantity, consumption_quantity):
    balance_quantity = quantity + purchase_quantity - consumption_quantity
    item = {
        "name": name,
        "quantity": quantity,
        "purchase_quantity": purchase_quantity,
        "consumption_quantity": consumption_quantity,
        "balance_quantity": balance_quantity,
    }
    st.session_state.inventory.append(item)

# Sidebar for adding new items
with st.sidebar:
    st.header("Add New Item")
    name = st.text_input("Item Name")
    quantity = st.number_input("Initial Quantity", min_value=0, step=1)
    purchase_quantity = st.number_input("Purchase Quantity", min_value=0, step=1)
    consumption_quantity = st.number_input("Consumption Quantity", min_value=0, step=1)
    if st.button("Add Item"):
        if name:  # Check if the name is not empty
            add_item(name, quantity, purchase_quantity, consumption_quantity)
            st.success(f"Item '{name}' added to inventory!")
        else:
            st.error("Please enter a valid item name.")

# Display the current inventory
st.header("Current Inventory")
if st.session_state.inventory:
    for item in st.session_state.inventory:
        st.write(f"""
        **Item:** {item['name']}  
        **Initial Quantity:** {item['quantity']}  
        **Purchase Quantity:** {item['purchase_quantity']}  
        **Consumption Quantity:** {item['consumption_quantity']}  
        **Balance Quantity:** {item['balance_quantity']}  
        """)
        st.write("---")
else:
    st.info("No items in the inventory yet. Add items using the sidebar.")
