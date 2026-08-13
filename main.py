from repositories.db import init_db
from repositories.item_repository import SQLiteItemRepository
from repositories.movement_repository import SQLiteMovementRepository
from services.catalog_service import CatalogService
from services.stock_service import StockService
from services.query_service import QueryService
from controllers.catalog_controller import CatalogController
from controllers.stock_controller import StockController
from controllers.query_controller import QueryController
from models.enums import Category, UnitOfMeasure, StockStatus
from datetime import date

init_db()

item_repo = SQLiteItemRepository()
movement_repo = SQLiteMovementRepository()
catalog_service = CatalogService(item_repo)
stock_service = StockService(item_repo, movement_repo)
query_service = QueryService(item_repo, movement_repo)
catalog_controller = CatalogController(catalog_service, query_service)
stock_controller = StockController(stock_service)
query_controller = QueryController(query_service)


def format_entry(entry, status: StockStatus) -> str:
      if status == StockStatus.OUT_OF_STOCK:
          return f"{entry.item.item_name} : OUT OF STOCK"
      elif status == StockStatus.LOW:
          return f"{entry.item.item_name} : {entry.quantity_on_hand} on hand : LOW STOCK"
      return f"{entry.item.item_name} : {entry.quantity_on_hand} on hand : OK"


while True:
      print("\n--- Inventory Management System ---")
      print("1. Register Item")
      print("2. View Item")
      print("3. Restock Item")
      print("4. Consume Item")
      print("5. List Low Stock")
      print("6. List Out of Stock")
      print("7. Search Item")
      print("8. Exit")
      choice = input("Enter choice: ")

      try:
          if choice == "1":
              name = input("Item name: ")
              category = Category(input("Category (PANTRY/WASHROOM/ONBOARDING): "))
              unit = UnitOfMeasure(input("Unit (PIECES/KG/LITERS/PACKETS): "))
              qty = float(input("Initial Quantity: "))
              reorder = float(input("Reorder Level: "))
              supplier = input("Supplier (press Enter to skip): ") or None
              location = input("Storage Location: ")
              entry = catalog_controller.register_item(name, category, unit, qty, reorder, supplier, location)
              print(f"Registered: {entry.item.item_name} with ID {entry.item.item_id}")

          elif choice == "2":
              item_id = input("Enter Item ID: ")
              entry, status = catalog_controller.view_item(item_id)
              print(format_entry(entry, status))

          elif choice == "3":
              item_id = input("Enter Item ID: ")
              qty = float(input("Quantity to restock: "))
              supplier = input("Supplier: ")
              unit_cost = float(input("Unit Cost: "))
              expiry_input = input("Expiry Date (YYYY-MM-DD, press Enter to skip): ")
              expiry_date = date.fromisoformat(expiry_input) if expiry_input else None
              stock_controller.restock(item_id, qty, supplier, unit_cost, expiry_date)
              print(f"Restocked {qty} units successfully.")

          elif choice == "4":
              item_id = input("Enter Item ID: ")
              qty = float(input("Quantity consumed: "))
              note = input("Note: ")
              stock_controller.consume(item_id, qty, note)
              print(f"Consumed {qty} units successfully.")

          elif choice == "5":
              entries = query_controller.list_low_stock()
              if not entries:
                  print("No low stock items.")
              else:
                  for entry in entries:
                      status = query_service.get_stock_status(entry)
                      print(format_entry(entry, status))

          elif choice == "6":
              entries = query_controller.list_out_of_stock()
              if not entries:
                  print("No out of stock items.")
              else:
                  for entry in entries:
                      print(format_entry(entry, StockStatus.OUT_OF_STOCK))

          elif choice == "7":
              name = input("Search by name: ")
              entries = query_controller.search_by_name(name)
              if not entries:
                  print("No items found.")
              else:
                  for entry in entries:
                      status = query_service.get_stock_status(entry)
                      print(format_entry(entry, status))

          elif choice == "8":
              print("Goodbye!")
              break

      except ValueError as e:
          print(f"Error: {e}")
