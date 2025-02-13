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
        name = input(f"Enter the name of item {i+1}: ")
        quantity = int(input(f"Enter the initial quantity of {name}: "))
        purchase_quantity = int(input(f"Enter the purchase quantity of {name}: "))
        consumption_quantity = int(input(f"Enter the consumption quantity of {name}: "))

        item = InventoryItem(name, quantity, purchase_quantity, consumption_quantity)
        item.update_balance()
        inventory.append(item)

    return inventory

def display_inventory(inventory):
    print("\nCurrent Inventory:")
    for item in inventory:
        print(item)

def main():
    inventory = create_inventory()
    display_inventory(inventory)

if __name__ == "__main__":
    main()
