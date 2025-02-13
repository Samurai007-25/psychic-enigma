class InventoryItem:
    def __init__(self, name, quantity, purchase_quantity, consumption_quantity):
        self.name = name
        self.quantity = quantity
        self.purchase_quantity = purchase_quantity
        self.consumption_quantity = consumption_quantity
        self.balance_quantity = quantity

    def update_balance(self):
        self.balance_quantity = self.quantity + self.purchase_quantity - self.consumption_quantity

    def __str__(self):
        return (f"Item: {self.name}, Quantity: {self.quantity}, "
                f"Purchase Quantity: {self.purchase_quantity}, "
                f"Consumption Quantity: {self.consumption_quantity}, "
                f"Balance Quantity: {self.balance_quantity}")

def create_inventory():
    inventory = []
    num_items = int(input("Enter the number of items to be stocked: "))

    for i in range(num_items):
        print(f"\nEnter details for item {i + 1}:")
        name = input("Enter the name of the item: ")
        quantity = int(input("Enter the initial quantity: "))
        purchase_quantity = int(input("Enter the purchase quantity: "))
        consumption_quantity = int(input("Enter the consumption quantity: "))

        item = InventoryItem(name, quantity, purchase_quantity, consumption_quantity)
        item.update_balance()
        inventory.append(item)

    return inventory

def display_inventory(inventory):
    print("\nCurrent Inventory:")
    for item in inventory:
        print(item)

def main():
    print("Welcome to the Inventory Management System!")
    inventory = create_inventory()
    display_inventory(inventory)

if __name__ == "__main__":
    main()
