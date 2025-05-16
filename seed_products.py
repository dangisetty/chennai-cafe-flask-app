import sqlite3

items = [
    # Soups
    ("Rasam", "Traditional South Indian spicy tamarind soup", 4.99, 10),
    ("Kozhi Rasam", "Spicy chicken soup with herbs", 6.99, 10),
    ("Sweet Corn Soup", "Veg-based thick corn soup", 5.99, 10),

    # Appetizers
    ("Vegetable Samosa", "Stuffed with potato and peas", 5.49, 15),
    ("Medhu Vada", "Fried savory lentil donuts", 5.00, 12),
    ("Chicken 65", "Spicy deep-fried chicken bites", 10.99, 10),
    ("Paneer 65", "Fried paneer cubes with chili seasoning", 10.99, 10),

    # Dosas
    ("Sada Dosa", "Plain rice crepe", 9.99, 20),
    ("Masala Dosa", "Filled with spiced potato", 11.99, 15),
    ("Mysore Masala Dosa", "Red chutney and potato masala", 12.99, 10),
    ("Onion Rava Dosa", "Crispy dosa with onions and semolina", 12.99, 10),
    ("Ghee Roast Dosa", "Rich dosa with clarified butter", 12.99, 10),

    # Parotta Specials
    ("Kothu Parotta (Veg)", "Chopped parotta with veggies & spices", 12.99, 10),
    ("Kothu Parotta (Chicken)", "Chopped parotta with chicken & spicy gravy", 14.99, 10),

    # Thali Platters
    ("Veg Thali", "Roti, curries, rice, and dessert", 18.99, 8),
    ("Non-Veg Thali", "Chicken and mutton curries, rice, dessert", 19.99, 8),

    # Chaat
    ("Pani Puri", "Crispy shells filled with flavored water", 6.99, 12),
    ("Samosa Chaat", "Crushed samosas with yogurt and chutneys", 7.99, 12),

    # Drinks
    ("Madras Filter Coffee", "Authentic South Indian style", 3.99, 20),
    ("Mango Lassi", "Sweet yogurt mango drink", 4.99, 20),
    ("Masala Chai", "Spiced Indian tea", 2.99, 20)
]

# Connect and insert
conn = sqlite3.connect('cafe.db')
cursor = conn.cursor()

cursor.executemany('''
    INSERT INTO products (name, description, price, quantity)
    VALUES (?, ?, ?, ?)
''', items)

conn.commit()
conn.close()

print("✨ All menu items added!")
