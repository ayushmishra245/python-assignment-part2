# ============================================
# BITSOM 3 - Part 2: Data Structures
# Restaurant Menu & Order Management System
# ============================================

import copy

# We have been given three data structures for the assignment.

# The first one is the menu.
# It stores each dish with its category, price and whether its available or not.

# The inventory stores how much stock we have for each dish
# and at what level we should reorder it.

# The sales log stores orders date wise.
# Each date has a list of orders placed on that day.

menu = {
    "Paneer Tikka":  {"category": "Starters", "price": 180.0,  "available": True},
    "Chicken Wings": {"category": "Starters", "price": 220.0,  "available": False},
    "Veg Soup":      {"category": "Starters", "price": 120.0,  "available": True},
    "Butter Chicken":{"category": "Mains",    "price": 320.0,  "available": True},
    "Dal Tadka":     {"category": "Mains",    "price": 180.0,  "available": True},
    "Veg Biryani":   {"category": "Mains",    "price": 250.0,  "available": True},
    "Garlic Naan":   {"category": "Mains",    "price": 40.0,   "available": True},
    "Gulab Jamun":   {"category": "Desserts", "price": 90.0,   "available": True},
    "Rasgulla":      {"category": "Desserts", "price": 80.0,   "available": True},
    "Ice Cream":     {"category": "Desserts", "price": 110.0,  "available": False},
}

inventory = {
    "Paneer Tikka":  {"stock": 10, "reorder_level": 3},
    "Chicken Wings": {"stock": 8,  "reorder_level": 2},
    "Veg Soup":      {"stock": 15, "reorder_level": 5},
    "Butter Chicken":{"stock": 12, "reorder_level": 4},
    "Dal Tadka":     {"stock": 20, "reorder_level": 5},
    "Veg Biryani":   {"stock": 6,  "reorder_level": 3},
    "Garlic Naan":   {"stock": 30, "reorder_level": 10},
    "Gulab Jamun":   {"stock": 5,  "reorder_level": 2},
    "Rasgulla":      {"stock": 4,  "reorder_level": 3},
    "Ice Cream":     {"stock": 7,  "reorder_level": 4},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1, "items": ["Paneer Tikka", "Garlic Naan"],      "total": 220.0},
        {"order_id": 2, "items": ["Gulab Jamun", "Veg Soup"],          "total": 210.0},
        {"order_id": 3, "items": ["Butter Chicken", "Garlic Naan"],    "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4, "items": ["Dal Tadka", "Garlic Naan"],         "total": 220.0},
        {"order_id": 5, "items": ["Veg Biryani", "Gulab Jamun"],       "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6, "items": ["Paneer Tikka", "Rasgulla"],         "total": 260.0},
        {"order_id": 7, "items": ["Butter Chicken", "Veg Biryani"],    "total": 570.0},
        {"order_id": 8, "items": ["Garlic Naan", "Gulab Jamun"],       "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9,  "items": ["Dal Tadka", "Garlic Naan", "Rasgulla"], "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"],          "total": 270.0},
    ],
}


# wrote these functions so i dont have to repeat the same logic in every task

def print_cart(cart):
    """prints whatever is in the cart at that point"""
    print("\n  Cart contents:")
    if not cart:
        print("    (cart is empty)")
        return
    for e in cart:
        line_total = e["quantity"] * e["price"]
        print(f'    {e["item"]} x{e["quantity"]} @ ₹{e["price"]} = ₹{line_total:.2f}')


def add_item(cart, item_name, qty):
    """
    adds a dish to the cart.
    checks 3 things before adding:
    1. is the dish even in the menu?
    2. is it currently available?
    3. if its already in cart, just increase qty instead of adding again
    """
    if item_name not in menu:
        print(f'  "{item_name}" not found in menu.')
        return

    if not menu[item_name]["available"]:
        print(f'  "{item_name}" is currently unavailable.')
        return

    for e in cart:
        if e["item"] == item_name:
            e["quantity"] += qty
            print(f'  "{item_name}" already in cart - updated qty to {e["quantity"]}.')
            return

    # only reaches here if its a new item
    cart.append({
        "item":     item_name,
        "quantity": qty,
        "price":    menu[item_name]["price"]
    })
    print(f'  Added "{item_name}" x{qty} to cart.')


def delete_item(cart, item_name):
    """
    removes a dish from cart by name.
    used range + pop instead of removing inside a for loop
    because that causes some items to get skipped
    """
    for i in range(len(cart)):
        if cart[i]["item"] == item_name:
            cart.pop(i)
            print(f'  Removed "{item_name}" from cart.')
            return
    print(f'  "{item_name}" was not found in cart.')


def change_qty(cart, item_name, new_qty):
    """changes qty of something already in cart. removes it if qty goes to 0"""
    for e in cart:
        if e["item"] == item_name:
            if new_qty <= 0:
                cart.remove(e)
                print(f'  "{item_name}" removed (qty set to {new_qty}).')
            else:
                e["quantity"] = new_qty
                print(f'  "{item_name}" qty changed to {new_qty}.')
            return
    print(f'  "{item_name}" not found in cart.')


def show_bill(cart):
    """
    prints the final bill with GST.
    restaurant food in india comes under 5% GST slab
    so applying 5% on subtotal
    """
    print("\n  ---- Order Summary ----")
    if not cart:
        print("  nothing in cart.")
        return

    subtotal = 0
    for e in cart:
        line_total = e["quantity"] * e["price"]
        subtotal += line_total
        print(f'  {e["item"]:<18} x{e["quantity"]}  =  ₹{line_total:.2f}')

    gst   = round(subtotal * 0.05, 2)
    total = subtotal + gst
    print("  " + "-" * 32)
    print(f'  Subtotal  : ₹{subtotal:.2f}')
    print(f'  GST (5%)  : ₹{gst:.2f}')
    print(f'  Total     : ₹{total:.2f}')
    print("  " + "-" * 32)


def print_stock(inv):
    """prints current stock and reorder level for all items"""
    for name, d in inv.items():
        print(f'    {name:<18} stock: {d["stock"]}   reorder at: {d["reorder_level"]}')


def get_revenue(sales_data):
    """
    totals up orders for each date and returns a dict with date wise revenue.
    used sum() with a generator instead of writing a separate counter variable
    """
    result = {}
    for date, orders in sales_data.items():
        result[date] = sum(o["total"] for o in orders)
    return result


# TASK 1 - EXPLORE THE MENU
# printing the full menu by category + some basic stats

print("\n" + "=" * 55)
print("  TASK 1 - EXPLORE THE MENU")
print("=" * 55)

# using a list to preserve the order categories appear in the menu
# cant use set() here because sets dont maintain order
cats = []
for item, d in menu.items():
    if d["category"] not in cats:
        cats.append(d["category"])

for cat in cats:
    print(f"\n  -- {cat} --")
    for item, d in menu.items():
        if d["category"] == cat:
            status = "Available" if d["available"] else "Unavailable"
            print(f'    {item:<18} ₹{d["price"]:.2f}   [{status}]')

print(f"\n  Total items on menu : {len(menu)}")

count = sum(1 for d in menu.values() if d["available"])
print(f"  Currently available : {count}")

# lambda here so i can find max by price in one line
costliest = max(menu.keys(), key=lambda x: menu[x]["price"])
print(f'  Most expensive item : {costliest}  (₹{menu[costliest]["price"]:.2f})')

print("\n  Items under ₹150:")
for item, d in menu.items():
    if d["price"] < 150:
        print(f'    {item}: ₹{d["price"]:.2f}')


# TASK 2 - CART OPERATIONS
# simulating add, duplicate check, unavailable item, remove, and final bill

print("\n\n" + "=" * 55)
print("  TASK 2 - CART OPERATIONS")
print("=" * 55)

cart = []  # each item in cart is stored as a dict

print("\n  > Adding Paneer Tikka x2")
add_item(cart, "Paneer Tikka", 2)
print_cart(cart)

print("\n  > Adding Gulab Jamun x1")
add_item(cart, "Gulab Jamun", 1)
print_cart(cart)

# paneer tikka already in cart so qty should go to 3, not add a new row
print("\n  > Adding Paneer Tikka x1 again (checking duplicate handling)")
add_item(cart, "Paneer Tikka", 1)
print_cart(cart)

print("\n  > Trying Mystery Burger (not in menu at all)")
add_item(cart, "Mystery Burger", 1)
print_cart(cart)

# chicken wings exists in menu but its marked as unavailable
print("\n  > Trying Chicken Wings (marked unavailable)")
add_item(cart, "Chicken Wings", 1)
print_cart(cart)

print("\n  > Removing Gulab Jamun")
delete_item(cart, "Gulab Jamun")
print_cart(cart)

show_bill(cart)


# TASK 3 - INVENTORY TRACKER
# backup inventory with deepcopy, test that it works,
# deduct cart items from stock, check what needs reordering

print("\n\n" + "=" * 55)
print("  TASK 3 - INVENTORY TRACKER")
print("=" * 55)

# deepcopy makes a completely separate copy of inventory
# shallow copy would still share the inner dicts so both would get updated
backup = copy.deepcopy(inventory)
print("\n  Inventory backup created using deepcopy.")

# testing deepcopy - changing original should not affect backup
print("\n  [deepcopy test] Changing Paneer Tikka stock to 999 in original...")
inventory["Paneer Tikka"]["stock"] = 999

print("\n  Original inventory now:")
print_stock(inventory)
print("\n  Backup (Paneer Tikka should still show 10):")
print_stock(backup)

# restore inventory before doing actual deductions
inventory = copy.deepcopy(backup)
print("\n  Inventory restored from backup.")

print("\n  Deducting cart items from stock:")
for e in cart:
    dish = e["item"]
    need = e["quantity"]

    if dish in inventory.keys():
        have = inventory[dish]["stock"]
        if have >= need:
            inventory[dish]["stock"] -= need
            print(f'    {dish}: -{need}  ->  {inventory[dish]["stock"]} left')
        else:
            # not enough stock for this order, setting to 0
            print(f'    WARNING: low stock for {dish} (need {need}, only {have} left) -> setting to 0')
            inventory[dish]["stock"] = 0

# check which items have gone below their reorder level
print("\n  Reorder Alerts:")
low = [(nm, d) for nm, d in inventory.items() if d["stock"] <= d["reorder_level"]]
if low:
    for nm, d in low:
        print(f'    !! {nm}: only {d["stock"]} left (reorder at {d["reorder_level"]})')
else:
    print("    all good, nothing to reorder.")

print("\n  Current inventory:")
print_stock(inventory)
print("\n  Original backup:")
print_stock(backup)


# TASK 4 - SALES LOG ANALYSIS
# daily revenue, best day, most ordered item
# then adding jan 5 data and redoing the analysis

print("\n\n" + "=" * 55)
print("  TASK 4 - SALES LOG ANALYSIS")
print("=" * 55)

daily = get_revenue(sales_log)

print("\n  Revenue per day:")
for date, r in daily.items():
    print(f'    {date}  ->  ₹{r:.2f}')

best = max(daily, key=daily.get)
print(f'\n  Best day so far: {best}  (₹{daily[best]:.2f})')

# going through all orders and counting how many times each dish appears
# .get(item, 0) saves me from having to check if the key exists
freq = {}
for date, orders in sales_log.items():
    for o in orders:
        for item in o["items"]:
            freq[item] = freq.get(item, 0) + 1

popular = max(freq, key=freq.get)
print(f'  Most ordered dish: {popular}  ({freq[popular]} times)')

# adding a new date to the sales log
sales_log["2025-01-05"] = [
    {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
    {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"],                     "total": 260.0},
]
print("\n  Added 2025-01-05 to sales_log.")

new_daily = get_revenue(sales_log)
print("\n  Updated revenue:")
for date, r in new_daily.items():
    print(f'    {date}  ->  ₹{r:.2f}')

new_best = max(new_daily, key=new_daily.get)
print(f'\n  New best day: {new_best}  (₹{new_daily[new_best]:.2f})')

# combining all orders from all dates into one flat list
flat_orders = []
for date, orders in sales_log.items():
    for o in orders:
        flat_orders.append((date, o))

print(f'\n  All orders ({len(flat_orders)} total):')
for idx, (date, o) in enumerate(flat_orders, start=1):
    items_str = ", ".join(o["items"])
    print(f'    {idx:>2}. [{date}]  Order #{o["order_id"]}  ₹{o["total"]:.2f}  |  {items_str}')

print("\n" + "=" * 55)
print("  done")
print("=" * 55)