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
                for i, (item_name, item_value) in enumerate(menu.items(), start=1):
                    print(f"{i}. {item_name}: {', '.join([f'{key}:{value}' for key, value in item_value.items()])}")
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
        self.people = people

    def make_order(self):
        try:
            self.show_menu()
            order_input = input("Choose the dishes you want by entering their numbers separated by commas: ")
            selected_indices = [int(index) for index in order_input.split(',')]

            total_cost = 0
            selected_dishes = []

            with shelve.open('data/menu') as menu:
                for index in selected_indices:
                    if 1 <= index <= len(menu):
                        item_name = list(menu.keys())[index - 1]
                        item_price = float(menu[item_name]['price'])
                        total_cost += item_price
                        selected_dishes.append(item_name)
                    else:
                        raise ValueError("Invalid menu item or wrong input.")

                rounded_cost = round(total_cost, 2)
                final_order = f"Your order is: \"{', '.join(selected_dishes)}\". Total cost is: {rounded_cost}$"
                print(final_order)
                self.save_order(customer_order=final_order)

        except ValueError:
            print("Sorry but you had wrong input, please try again and enter the correct data.")

    def show_order(self):
        try:
            with shelve.open('data/order') as order:
                if not order:
                    raise ValueError
                else:
                    for customer, details in order.items():
                        print(f"{customer}, {details}")
        except Exception:
            print("Sorry, probably your order was deleted or something went wrong.")

    def save_order(self, customer_order):
        with shelve.open('data/order') as order:
            order[self.customer_name] = customer_order

    def delete_order(self):
        with shelve.open('data/order') as order:
            if self.customer_name in order:
                del order[self.customer_name]


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

c = Customer("Julia", 5)
# c.make_order()
# print(c.load_menu())
# c.delete_order()
c.show_order()