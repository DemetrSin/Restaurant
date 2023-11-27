import json


class Restaurant:
    lst = []

    def __init__(self):
        self._book_table = self.load_tables()
        self._menu_items = self.load_menu()

    def add_item_to_menu(self, items):
        for key, value in items.items():
            if key not in self._menu_items:
                self._menu_items[key] = {}
            self._menu_items[key] = value
        self.save_menu()

    @classmethod
    def load_menu(cls):
        try:
            with open('menu.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_menu(self):
        with open('menu.json', 'w') as file:
            json.dump(self._menu_items, file, indent=2)

    def book_tables(self):
        success = False
        while not success:
            try:
                persons = int(input("Please indicate how many people you will be: "))
                if persons <= 5:
                    self._book_table['small_tables'] -= 1
                    print(f"You booked table for {persons}")
                    self.save_tables()
                    success = True
                elif persons > 5 and persons <= 10:
                    self._book_table['big_tables'] -= 1
                    print(f"You booked table for {persons}")
                    self.save_tables()
                    success = True
                elif persons > 10:
                    print("Sorry but max number of people is '10'")
            except ValueError:
                print("Type of input must be integer")

    @classmethod
    def load_tables(cls):
        try:
            with open('tables.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_tables(self):
        with open('tables.json', 'w') as file:
            json.dump(self._book_table, file, indent=2)

    def customer_order(self):
        self.get_menu()
        order = str(input("Choose what you want from menu by comma please: "))
        list_order = order.split(',')
        total_cost = 0
        for dish in list_order:
            if dish in self._menu_items:
                total_cost += float(self._menu_items[dish]['price'])
        rounded_cost = round(total_cost, 2)
        final_order = f"Your order is: \"{', '.join(list_order)}\". Total cost is: {rounded_cost}$"
        self.lst.append(final_order)
        return final_order

    def show_order(self):
        print(' ,'.join(self.lst))

    def get_menu(self):
        for k, v in self._menu_items.items():
            print(f"{k} - {v['price']}$ - {v['weight']} - {v['composition']}")


r = Restaurant()


# r.add_item_to_menu({'New Dish': {"price": 15.99, "weight": "350g", "composition": "New ingredients"}})
def customer_behavior():
    r.book_tables()
    ask_menu = input("Do you wanna look at menu? Type 'yes' or 'no': ")
    if ask_menu == 'yes':
        r.get_menu()
    else:
        print("Okay, you\'ll get the chance do it right here.")
    ask_order = input("Do you wanna make order? Type 'yes' or 'no': ")
    if ask_order == 'yes':
        r.customer_order()
        r.show_order()
    else:
        print("We'll be glad to see you again if you change your mind. Have a nice day!")


customer_behavior()
