import shelve


class Restaurant:
    def __init__(self, restaurant_name, ):
        self.restaurant_name = restaurant_name
        self.table = []

    def add_menu_item(self, item_name, item_details):
        try:
            with shelve.open('data/menu') as menu:
                menu[item_name] = item_details
        except:
            print("Sorry, try to contact the developer for more info.")

    def delete_menu_item(self, menu_item):
        with shelve.open('data/menu') as menu:
            if menu_item in menu:
                del menu[menu_item]
                print(f"The item: {menu_item} was successfully deleted")
            else:
                print(f"The item: {menu_item} was not found")

    def show_menu(self):
        try:
            with shelve.open('data/menu') as menu:
                for item_name, item_value in menu.items():
                    print(f"{item_name}: {', '.join([f'{key}:{value}' for key, value in item_value.items()])}")
        except:
            print("Sorry, something went wrong, try again later")

    def book_table(self):
        try:
            table = int(input(f"{self.table} < This numbers of tables now reserved. Please, choose a table you want, one number from 1 to 15: "))
            if table in self.table:
                print(f"Dear customer, sorry, but this table is booked. Please choose one number from 1 to 15, excluding these numbers: {self.table}")
            elif table > 15 or table <= 0:
                print("Sorry, but we have only 15 tables numbered from 1 to 15. Please choose a correct number.")
            else:
                self.table.append(table)
                self.save_tables()
        except ValueError:
            print("Sorry but you had wrong input, please try again and enter the correct data:'Numbers from 1 to 15'")

    def save_tables(self):
        with shelve.open('data/tables') as tables:
            if self.table not in tables['tables']:
                tables.setdefault('tables', []).append(self.table)

    def show_booked_tables(self):
        with shelve.open('data/tables') as tables:
            print(','.join(map(str, tables['tables'])))

    def unbook_table(self, table):
        with shelve.open('data/tables', writeback=True) as tables:
            if table in tables['tables']:
                tables.setdefault('tables', []).remove(table)


class Customer(Restaurant):

    def __init__(self, customer_name, people):
        self.customer_name = customer_name

    def make_order(self):
        self.show_menu()
        order = str(input("Choose what you want from menu by comma please: "))
        list_order = order.split(',')
        total_cost = 0
        with shelve.open('data/menu') as menu:
            for dish in menu.items():
                if dish in menu.items():
                    total_cost += float(menu[dish[0]]['price'])
            rounded_cost = round(total_cost, 2)
            final_order = f"Your order is: \"{', '.join(list_order)}\". Total cost is: {rounded_cost}$"
            print(final_order)




# r = Restaurant('Avrora')
# r.book_table()
# r.add_menu_item("Chocolate Fondant", {
#     "price": 7.99,
#     "weight": "200g",
#     "composition": "Chocolate cake, molten chocolate center, vanilla ice cream"
#   })
# r.show_menu()
# r.delete_menu_item("Chocolate Fondant")
# r.unbook_table(5)
# r.show_booked_tables()

# c = Customer("Julia", 5)
# c.make_order()