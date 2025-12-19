from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import json
import os

class Meal:
    # Represent meal & its ingredients
    def __init__(self, meal_id: str, name: str, ingredients: List[str], 
                 category: str = "general"):
        self.meal_id = meal_id
        self.name = name
        self.ingredients = ingredients
        self.category = category
    
    def to_dict(self) -> Dict:
        # Convert meal to dictionary
        return {
            "meal_id": self.meal_id,
            "name": self.name,
            "ingredients": self.ingredients,
            "category": self.category
        }


class Order:
    # Show ingredient order
    def __init__(self, order_id: str, meal: Meal, customer_name: str, 
                 delivery_date: str, status: str = "pending"):
        self.order_id = order_id
        self.meal = meal
        self.customer_name = customer_name
        self.delivery_date = delivery_date
        self.status = status
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        # Convert order to dictionary
        return {
            "order_id": self.order_id,
            "meal": self.meal.to_dict(),
            "customer_name": self.customer_name,
            "delivery_date": self.delivery_date,
            "status": self.status,
            "created_at": self.created_at
        }


class OrderRepository:
    # Manages order storage and retrieval + Data persistence strategy to prevent order loss
    def __init__(self):
        # In-memory storage
        self._orders: Dict[str, Order] = {}
        # Persistent storage (in production would be a database)
        self._persistent_state: List[Dict] = []
    
    def add_order(self, order: Order) -> bool:
        try:
            self._orders[order.order_id] = order
            # Persist immediately to prevent data loss (NFR3)
            self._persistent_state.append(order.to_dict())
            return True
        except Exception as e:
            print(f"Error adding order: {e}")
            return False
    
    def get_order(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)
    
    def get_orders_by_customer(self, customer_name: str) -> List[Order]:
        return [order for order in self._orders.values() 
                if order.customer_name == customer_name]

class SmartCaterService:
    # Handles meal management & order processing
    def __init__(self):
        self.meals: Dict[str, Meal] = {}
        self.order_repository = OrderRepository()
        self._next_order_id = 1
    
    def add_meal(self, meal: Meal):
        self.meals[meal.meal_id] = meal
    
    def get_meal(self, meal_id: str) -> Optional[Meal]:
        return self.meals.get(meal_id)
    
    def list_meals(self) -> List[Meal]:
        return list(self.meals.values())
    
    def order_ingredients(self, meal_id: str, customer_name: str, 
                         delivery_date: str) -> Optional[Order]:
        # Create order for ingredients of the meal
        meal = self.get_meal(meal_id)
        if not meal:
            print(f"Error: Meal with ID '{meal_id}' not found.")
            return None
        
        order_id = f"ORD-{self._next_order_id:04d}"
        self._next_order_id += 1
        
        order = Order(order_id, meal, customer_name, delivery_date)
        
        if self.order_repository.add_order(order):
            print(f"✓ Order {order_id} created successfully!")
            return order
        else:
            print(f"✗ Failed to create order {order_id}.")
            return None
    
    def view_order(self, order_id: str):
        order = self.order_repository.get_order(order_id)
        if order:
            print(f"\n{'='*60}")
            print(f"Order Details: {order_id}")
            print(f"{'='*60}")
            print(f"Customer: {order.customer_name}")
            print(f"Meal: {order.meal.name}")
            print(f"Ingredients: {', '.join(order.meal.ingredients)}")
            print(f"Delivery Date: {order.delivery_date}")
            print(f"Status: {order.status}")
            print(f"Created: {order.created_at}")
            print(f"{'='*60}\n")
        else:
            print(f"Order {order_id} not found.")


def load_meals_from_json(filename: str = "meals.json") -> List[Meal]:
    # Load meals from JSON
    meals = []
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for meal_data in data:
                    meal = Meal(
                        meal_id=meal_data["meal_id"],
                        name=meal_data["name"],
                        ingredients=meal_data["ingredients"],
                        category=meal_data.get("category", "general")
                    )
                    meals.append(meal)
        else:
            print(f"Warning: {filename} not found. Using empty meal list.")
    except json.JSONDecodeError as e:
        print(f"Error reading {filename}: Invalid JSON format. {e}")
    except Exception as e:
        print(f"Error loading meals from {filename}: {e}")
    return meals


def display_menu():
    print("\n" + "="*70)
    print("SmartCater - Ingredient Ordering Service")
    print("="*70)
    print("1. See available meals")
    print("2. Place an order")
    print("3. View my orders")
    print("4. View order details")
    print("5. Exit")
    print("="*70)


def display_meals(service: SmartCaterService):
    meals = service.list_meals()
    if not meals:
        print("\nNo meals available.")
        return
    
    print("\n" + "-"*70)
    print("Available Meals:")
    print("-"*70)
    for meal in meals:
        print(f"\n[{meal.meal_id}] {meal.name}")
        print(f"   Category: {meal.category}")
        print(f"   Ingredients: {', '.join(meal.ingredients)}")
    print("-"*70)


def interactive_order(service: SmartCaterService):
    print("\n" + "-"*70)
    print("Place an Order")
    print("-"*70)
    
    meals = service.list_meals()
    if not meals:
        print("No meals available to order.")
        return
    
    print("\nAvailable Meals:")
    for meal in meals:
        print(f"  [{meal.meal_id}] {meal.name} ({meal.category})")
    
    while True:
        meal_id = input("\nEnter meal ID to order (or 'cancel' to go back): ").strip().upper()
        if meal_id.lower() == 'cancel':
            return
        
        meal = service.get_meal(meal_id)
        if meal:
            print(f"\nSelected: {meal.name}")
            print(f"Ingredients: {', '.join(meal.ingredients)}")
            break
        else:
            print(f"Invalid meal ID. Please try again.")
    
    while True:
        customer_name = input("\nEnter your name: ").strip()
        if customer_name:
            break
        print("Name cannot be empty. Please enter your name.")
    
    while True:
        delivery_date = input("Enter delivery date ('today' or 'tomorrow'): ").strip().lower()
        if delivery_date == 'today':
            delivery_date = date.today().isoformat()
            break
        elif delivery_date == 'tomorrow':
            delivery_date = (date.today() + timedelta(days=1)).isoformat()
            break
        else:
            print("Invalid input. Please enter 'today' or 'tomorrow'.")
    
    print(f"\nOrder Summary:")
    print(f"  Meal: {meal.name}")
    print(f"  Customer: {customer_name}")
    print(f"  Delivery Date: {delivery_date}")
    confirm = input("\nConfirm order? (yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y']:
        order = service.order_ingredients(meal_id, customer_name, delivery_date)
        if order:
            print(f"\n✓ Order placed successfully!")
            service.view_order(order.order_id)
    else:
        print("Order cancelled.")


def interactive_view_orders(service: SmartCaterService):
    print("\n" + "-"*70)
    print("View My Orders")
    print("-"*70)
    
    customer_name = input("Enter your name: ").strip()
    if not customer_name:
        print("Name cannot be empty.")
        return
    
    orders = service.order_repository.get_orders_by_customer(customer_name)
    if orders:
        print(f"\nOrders for {customer_name}:")
        print("-"*70)
        for order in orders:
            print(f"\n  Order ID: {order.order_id}")
            print(f"  Meal: {order.meal.name}")
            print(f"  Status: {order.status}")
            print(f"  Delivery Date: {order.delivery_date}")
    else:
        print(f"\nNo orders found for {customer_name}.")


def interactive_view_order_details(service: SmartCaterService):
    print("\n" + "-"*70)
    print("View Order Details")
    print("-"*70)
    
    order_id = input("Enter order ID: ").strip().upper()
    if not order_id:
        print("Order ID cannot be empty.")
        return
    
    service.view_order(order_id)


def main():
    print("="*70)
    print("SmartCater - Ingredient Ordering Service")
    print("="*70)
    print("Welcome to SmartCater!")
    
    service = SmartCaterService()
    
    meals = load_meals_from_json("meals.json")
    for meal in meals:
        service.add_meal(meal)
    print(f"\n✓ Loaded {len(meals)} meals into catalog")
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            display_meals(service)
        elif choice == '2':
            interactive_order(service)
        elif choice == '3':
            interactive_view_orders(service)
        elif choice == '4':
            interactive_view_order_details(service)
        elif choice == '5':
            print("\nThank you for using SmartCater! Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
