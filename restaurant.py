import shelve
from datetime import datetime
from custom_logger import Logger

CURRENT_TIME = datetime.now()
FORMATTED_TIME = CURRENT_TIME.strftime("%Y-%m-%d %H:%M")
CLOSING_TIME = CURRENT_TIME.replace(hour=23, minute=00, second=0, microsecond=0)


class NotYetTimeError(Exception):
    """Custom Class for Error"""
    pass


class Restaurant:
    """Class Restaurant with methods for simply functions, naming says what exactly method do, else in comments."""
    def __init__(self, restaurant_name: str, number_of_tables: int):
        """"Class constructor
        Params:
        restaurant_name (str): Just name for restaurant
        number_of_tables (int): Choose how much tables are in restaurant"""
        self.restaurant_name = restaurant_name
        self.number_of_tables = number_of_tables

    def add_menu_item(self, item_name: str, item_details: dict):
        """Important! Method contain DICT.
        Params:
            item_name (str): Name of the dish to add.
            item_details(dict): Nested DICT with details of dish. See examples in Comment with method call at the code bottom
        Raises:
            Exception: if item_details isn't DICT"""
        try:
            with shelve.open('data/menu') as menu:
                if isinstance(item_name, str) and isinstance(item_details, dict):
                    menu[item_name] = item_details
                    print(f"The item:{item_name} with details {item_details} was successfully added.")
                else:
                    raise Exception
        except Exception as e:
            print("Please, make sure that you use DICT format for item_details.")
            Logger(level='warning', msg="Need to check out what's wrong with add_menu_item.").create_log()

    def delete_menu_item(self, menu_item: str):
        """Params:
            menu_item (str): Name of the dish to delete from dict"""
        with shelve.open('data/menu') as menu:
            if menu_item in menu:
                del menu[menu_item]
                print(f"The item: {menu_item} was successfully deleted")
            else:
                print(f"The item: {menu_item} was not found")

    def show_menu(self):
        """Method for show whole menu with numbering of concrete Restaurant by unpacking dict and formatted by f-string"""
        try:
            with shelve.open('data/menu') as menu:
                for i, (item_name, item_value) in enumerate(menu.items(), start=1):
                    print(f"{i}. {item_name}: {', '.join([f'{key}:{value}' for key, value in item_value.items()])}")
        except Exception:
            print("Sorry, something went wrong, try again later")
            Logger(level='error', msg="Method show menu didn't do his job, check out")

    def book_table(self):
        """Method for booking table and add datetime.now() to it, using DICT, and INPUT for choosing table. There are using checks if table in accessible range and Exception if Input was wrong"""
        try:
            reservation_time = CURRENT_TIME.strftime("%d %H:%M")
            with shelve.open('data/tables') as tables:
                table_number = input(f"Tables currently booked: {', '.join(list(tables.keys()))}. Choose a table number from 1 to {self.number_of_tables}: ")
                if table_number in tables:
                    print(f"Sorry, but table {table_number} is already booked. Please choose an available table.")
                elif int(table_number) > self.number_of_tables or int(table_number) <= 0:
                    print(f"Invalid table number. Please choose a number between 1 and {self.number_of_tables}.")
                else:
                    tables[table_number] = reservation_time
                    print(f"Table {table_number} successfully booked at {reservation_time}.")
        except ValueError:
            print(f"Invalid input. Please, try again and enter a valid table number.")

    def show_booked_tables(self):
        """Method for show whole booked tables, if tables DICT is empty raising ValueError and it's being processed by Exception"""
        with shelve.open('data/tables') as tables:
            if tables:
                for table, time in tables.items():
                    print(f"Table: {table} was reserved at: {time}")
            else:
                print("Whole tables are free now")

    def unbook_table(self, table: int):
        """Params:
            table (int): number of table need to unbook it treats by str() for comfort """
        with shelve.open('data/tables', writeback=True) as tables:
            if str(table) in tables:
                del tables[str(table)]
                print(f"Table {table} successfully unbooked.")
            else:
                print(f"Table {table} is not currently booked.")

    def close_restaurant(self, closing_time: datetime):
        """Method for close restaurant and clear tables and orders data, if not time utilize raise custom Error and treat it by Exception
        Params:
            closing_time(datetime): IMPORTANT! Has to be like that CLOSING_TIME constant
        Raises:
            NotYetTimeError: if it's not time for close"""
        try:
            if CURRENT_TIME > closing_time:
                with shelve.open('data/tables', writeback=True) as tables:
                    tables.clear()

                with shelve.open('data/order', writeback=True) as order:
                    order.clear()
                print("The restaurant is closed. All tables are unbooked, and orders are cleared.")
            else:
                raise NotYetTimeError
        except NotYetTimeError:
            print("It's still not time to close")


class Customer(Restaurant):
    """Class Customer for making order and saving its orders"""

    def __init__(self, customer_name: str):
        """Class constructor
        Params:
            customer_name (str): Just customer name"""
        self.customer_name = customer_name

    def make_order(self):
        """Method for make order comfortable. Accepts dish numbering by INPUT and keep it in LIST variable, then looking for by indexes in menu and count their cost add dishes to another LIST variable, finally print the result.
        Raises:
            ValueError: If invalid menu item or wrong input"""

        try:
            self.show_menu()
            order_input = input("Choose the dishes you want by entering their numbers separated by commas: ")
            selected_indices = [int(index) for index in order_input.split(',')]

            total_cost = 0
            selected_dishes = []
            order_time = FORMATTED_TIME

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
                final_order = f"Order for {self.customer_name}: \"{', '.join(selected_dishes)}\". Total cost is: {rounded_cost}$."
                print(final_order)
                self.save_order(customer_order=final_order, time=order_time)

        except ValueError:
            print("Sorry but you had wrong input, please try again and enter the correct data.")

    def show_order(self):
        """Method for showing order if order DICT is empty raising ValueError and treat it by Exception
        Raises:
            ValueError: if data order is empty"""
        try:
            with shelve.open('data/order') as order:
                if not order:
                    raise ValueError
                else:
                    for customer, details in order.items():
                        order_details = details["order_details"]
                        order_time = details["order_time"]
                        print(f"{customer}, {order_details}, Order time: {order_time}")
        except Exception:
            print("Sorry, probably your order was deleted or something went wrong.")

    def save_order(self, customer_order: str, time: str):
        """Method for saving customer order into DICT
        Params:
            customer_order (str): accepts order from make_order method
            time (str): basically it accepts FORMATTED_TIME constant"""
        with shelve.open('data/order') as order:
            order[self.customer_name] = {"order_details": customer_order, "order_time": time}

    def delete_order(self):
        """Just delete order from DICT"""
        with shelve.open('data/order') as order:
            if self.customer_name in order:
                del order[self.customer_name]
                print(f"Order for {self.customer_name} was successfully deleted")
            else:
                print(f"There is no order to delete for {self.customer_name}")

def test_restaurant_class_logic():
    r = Restaurant('Avrora', 20)
    r.show_menu()
    r.add_menu_item("Chocolate Fondant", {
        "price": 7.99,
        "weight": "200g",
        "composition": "Chocolate cake, molten chocolate center, vanilla ice cream"
      })
    r.delete_menu_item("Chocolate Fondant")
    r.book_table()
    r.show_booked_tables()
    r.unbook_table(6)
    r.close_restaurant(CLOSING_TIME)


def test_customer__class_logic():
    c = Customer("Julia")
    c.make_order()
    c.show_order()
    c.delete_order()

# test_restaurant_class_logic()
# test_customer__class_logic()