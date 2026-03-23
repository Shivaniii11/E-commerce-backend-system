import mysql.connector

# ---------------- DB CONNECTION ----------------
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",
    database="shopping_system"
)

cur = con.cursor()


# ---------------- SAFE EXECUTE ----------------
def safe_execute(query, values):
    try:
        cur.execute(query, values)
        con.commit()
        return True
    except Exception as e:
        print("❌ Error:", e)
        return False


# ---------------- ADMIN ----------------
def admin_login():
    u = input("Admin Username: ")
    p = input("Password: ")

    if u == "admin" and p == "admin123":
        print("\n--- ADMIN DASHBOARD ---")

        cur.execute("SELECT COUNT(*) FROM orders")
        print("Total Orders:", cur.fetchone()[0])

        cur.execute("SELECT SUM(total_price) FROM orders")
        print("Total Revenue:", cur.fetchone()[0] or 0)

        cur.execute("SELECT COUNT(*) FROM buyers")
        print("Total Buyers:", cur.fetchone()[0])

        cur.execute("SELECT COUNT(*) FROM sellers")
        print("Total Sellers:", cur.fetchone()[0])

    else:
        print("Invalid login")


# ---------------- SELLER ----------------
def seller_register():
    sid = input("Shop ID: ")

    cur.execute("SELECT * FROM sellers WHERE shopid=%s", (sid,))
    if cur.fetchone():
        print("Seller already exists")
        return

    name = input("Shop Name: ")
    pwd = input("Password: ")

    if safe_execute("INSERT INTO sellers VALUES(%s,%s,%s)", (sid, name, pwd)):
        print("✅ Seller Registered")


def seller_login():
    sid = input("Shop ID: ")
    pwd = input("Password: ")

    cur.execute("SELECT * FROM sellers WHERE shopid=%s AND password=%s", (sid, pwd))
    if cur.fetchone():
        seller_menu(sid)
    else:
        print("Invalid login")


def seller_menu(shopid):

    while True:

        print("\n1 Add Product")
        print("2 View Products")
        print("3 Logout")

        ch = input("Choice: ")

        # ✅ VALIDATION
        if ch not in ["1", "2", "3"]:
            print("❌ Invalid choice, please enter 1-3")
            continue

        if ch == "1":
            pid = input("Product ID: ")

            cur.execute("select * from products where product_id=%s",(pid,))
            if cur.fetchone():
                print("Product already exists")
                continue

            name = input("Product Name: ")
            cat = input("Category: ")
            sub1 = input("Subcategory1: ")
            sub2 = input("Subcategory2: ")
            qty = int(input("Quantity: "))
            price = float(input("Price: "))

            safe_execute(
                "insert into products values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (pid,name,cat,sub1,sub2,qty,qty,price,shopid)
            )

            print("✅ Product Added")

        elif ch == "2":
            cur.execute("select * from products where shopid=%s",(shopid,))
            for i in cur.fetchall():
                print(i)

        elif ch == "3":
            break


# ---------------- BUYER ----------------
def buyer_register():
    bid = input("Buyer ID: ")

    cur.execute("SELECT * FROM buyers WHERE buyerid=%s", (bid,))
    if cur.fetchone():
        print("Buyer already exists")
        return

    name = input("Name: ")
    addr = input("Address: ")
    pwd = input("Password: ")

    if safe_execute("INSERT INTO buyers VALUES(%s,%s,%s,%s)", (bid, name, addr, pwd)):
        print("✅ Buyer Registered")


def buyer_login():
    bid = input("Buyer ID: ")
    pwd = input("Password: ")

    cur.execute("SELECT * FROM buyers WHERE buyerid=%s AND password=%s", (bid, pwd))
    if cur.fetchone():
        buyer_menu(bid)
    else:
        print("Invalid login")


#  BUYER MENU
def buyer_menu(buyerid):

    while True:

        print("\n1 View Categories")
        print("2 Search Product")
        print("3 Buy Product")
        print("4 History")
        print("5 Logout")

        ch = input("Choice: ")

        # ✅ VALIDATION (IMPORTANT)
        if ch not in ["1", "2", "3", "4", "5"]:
            print("❌ Invalid choice, please enter 1-5")
            continue

        # 1️⃣ VIEW CATEGORIES
        if ch == "1":
            cur.execute("SELECT DISTINCT category FROM products")
            data = cur.fetchall()

            if not data:
                print("No categories found")
            else:
                print("\n--- Categories ---")
                for c in data:
                    print(c[0])

        # 2️⃣ SEARCH PRODUCT
        elif ch == "2":
            name = input("Enter product name: ")
            cur.execute("SELECT * FROM products WHERE product_name LIKE %s", ("%"+name+"%",))
            for i in cur.fetchall():
                print(i)

        # 3️⃣ BUY PRODUCT
        elif ch == "3":
            pid = input("Product ID: ")
            qty = int(input("Quantity: "))

            cur.execute("SELECT price,shopid,current_quantity FROM products WHERE product_id=%s", (pid,))
            data = cur.fetchone()

            if not data:
                print("❌ Product not found")
                continue

            price, shopid, stock = data

            if qty > stock:
                print("❌ Not enough stock")
                continue

            total = price * qty

            if not safe_execute(
                "INSERT INTO orders(buyerid,product_id,quantity,total_price) VALUES(%s,%s,%s,%s)",
                (buyerid, pid, qty, total)
            ):
                print("⚠️ Foreign key error")
                continue

            safe_execute(
                "UPDATE products SET current_quantity=current_quantity-%s WHERE product_id=%s",
                (qty, pid)
            )

            safe_execute(
                "INSERT INTO seller_history(shopid,product_id,quantity,total_amount) VALUES(%s,%s,%s,%s)",
                (shopid, pid, qty, total)
            )

            print("✅ Purchase successful")

        # 4️⃣ HISTORY
        elif ch == "4":
            cur.execute("SELECT * FROM orders WHERE buyerid=%s", (buyerid,))
            for i in cur.fetchall():
                print(i)

        # 5️⃣ LOGOUT
        elif ch == "5":
            break

# ---------------- MAIN ----------------
def main():

    while True:

        print("\n===== E-COMMERCE BACKEND SYSTEM =====")
        print("1 Admin Login")
        print("2 Seller Register")
        print("3 Seller Login")
        print("4 Buyer Register")
        print("5 Buyer Login")
        print("6 Exit")

        ch = input("Choice: ")

        # ✅ VALIDATION (IMPORTANT)
        if ch not in ["1", "2", "3", "4", "5", "6"]:
            print("❌ Invalid choice, please enter 1-6")
            continue

        if ch == "1":
            admin_login()

        elif ch == "2":
            seller_register()

        elif ch == "3":
            seller_login()

        elif ch == "4":
            buyer_register()

        elif ch == "5":
            buyer_login()

        elif ch == "6":
            print("👋 Exiting system...")
            break
        
main()