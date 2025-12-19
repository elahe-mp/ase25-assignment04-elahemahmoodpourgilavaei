from datetime import datetime, date, timedelta
from typing import List, Dict, Optional

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
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Meal':
        # Create meal
        return cls(
            meal_id=data["meal_id"],
            name=data["name"],
            ingredients=data["ingredients"],
            category=data.get("category", "general")
        )


class Order:
    # show ingredient order
    
    def __init__(self, order_id: str, meal: Meal, customer_name: str, 
                 delivery_date: str, status: str = "pending"):
        self.order_id = order_id
        self.meal = meal
        self.customer_name = customer_name
        self.delivery_date = delivery_date
        self.status = status
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "order_id": self.order_id,
            "meal": self.meal.to_dict(),
            "customer_name": self.customer_name,
            "delivery_date": self.delivery_date,
            "status": self.status,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Order':
        meal = Meal.from_dict(data["meal"])
        order = cls(
            order_id=data["order_id"],
            meal=meal,
            customer_name=data["customer_name"],
            delivery_date=data["delivery_date"],
            status=data.get("status", "pending")
        )
        order.created_at = data.get("created_at", datetime.now().isoformat())
        return order


class OrderRepository:

    # Manages order storage and retrieval + Data persistence strategy to prevent order loss
   
    def __init__(self):
        # In-memory storage
        self._orders: Dict[str, Order] = {}
        # Simulated persistent storage (in a real system, this would be a database)
        self._persistent_state: List[Dict] = []
    
    def add_order(self, order: Order) -> bool:
        try:
            self._orders[order.order_id] = order
            order_dict = order.to_dict()
            self._persistent_state.append(order_dict)
            return True
        except Exception as e:
            print(f"Error adding order: {e}")
            return False
    
    def get_order(self, order_id: str) -> Optional[Order]:
        # Retrieve an order
        return self._orders.get(order_id)
    
    def get_all_orders(self) -> List[Order]:
        # Retrieve all orders
        return list(self._orders.values())
    
    def get_orders_by_customer(self, customer_name: str) -> List[Order]:
        # Retrieve all orders for a specific customer
        return [order for order in self._orders.values() 
                if order.customer_name == customer_name]
    
    def update_order_status(self, order_id: str, new_status: str) -> bool:
        # Update the status of an order
        if order_id in self._orders:
            self._orders[order_id].status = new_status
            for order_dict in self._persistent_state:
                if order_dict["order_id"] == order_id:
                    order_dict["status"] = new_status
            return True
        return False
    
    def recover_from_persistent_state(self):
        # Recover orders from persistent state
        recovered_count = 0
        for order_dict in self._persistent_state:
            try:
                order = Order.from_dict(order_dict)
                self._orders[order.order_id] = order
                recovered_count += 1
            except Exception as e:
                print(f"Error recovering order {order_dict.get('order_id', 'unknown')}: {e}")
        return recovered_count
    
    def get_persistent_state(self) -> List[Dict]:
        return self._persistent_state.copy()


class SmartCaterService:
    #Handles meal management and order processing
    def __init__(self):
        self.meals: Dict[str, Meal] = {}
        self.order_repository = OrderRepository()
        self._next_order_id = 1
    
    def add_meal(self, meal: Meal):
        # Add a meal to the catalog
        self.meals[meal.meal_id] = meal
    
    def get_meal(self, meal_id: str) -> Optional[Meal]:
        # Retrieve a meal by ID
        return self.meals.get(meal_id)
    
    def list_meals(self) -> List[Meal]:
        # List all meals
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
        
        # Create order
        order = Order(
            order_id=order_id,
            meal=meal,
            customer_name=customer_name,
            delivery_date=delivery_date
        )
        
        if self.order_repository.add_order(order):
            print(f"✓ Order {order_id} created successfully!")
            return order
        else:
            print(f"✗ Failed to create order {order_id}.")
            return None
    
    def view_order(self, order_id: str):
        # View order details 
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
    
    def list_customer_orders(self, customer_name: str):
        # List all orders for a customer
        orders = self.order_repository.get_orders_by_customer(customer_name)
        if orders:
            print(f"\nOrders for {customer_name}:")
            for order in orders:
                print(f"  - {order.order_id}: {order.meal.name} "
                      f"(Status: {order.status}, Delivery: {order.delivery_date})")
        else:
            print(f"No orders found for {customer_name}.")


def create_sample_meals() -> List[Meal]:
    # sample meals
    return [
        Meal("M001", "Vegan Pasta", ["pasta", "tomatoes", "basil", "olive oil"], "vegan"),
        Meal("M002", "Chicken Curry", ["chicken", "curry powder", "coconut milk", "rice"], "quick meals"),
        Meal("M003", "Gluten-Free Salad", ["lettuce", "tomatoes", "cucumber", "olive oil"], "gluten-free"),
        Meal("M004", "Beef Steak", ["beef", "potatoes", "green beans", "butter"], "general"),
        Meal("M005", "Vegetable Stir Fry", ["broccoli", "carrots", "soy sauce", "ginger"], "vegan")
    ]


def demo():
    print("="*70)
    print("SmartCater - Ingredient Ordering Service Demo")
    print("="*70)
    print("\nThis demo implements FR3: Order ingredients for a selected meal")
    print("and addresses NFR3: Data persistence to prevent order loss.\n")
    
    service = SmartCaterService()
    
    print("Step 1: Loading meal catalog...")
    sample_meals = create_sample_meals()
    for meal in sample_meals:
        service.add_meal(meal)
    print(f"✓ Loaded {len(sample_meals)} meals\n")
    
    print("Step 2: Available Meals:")
    print("-" * 70)
    for meal in service.list_meals():
        print(f"  [{meal.meal_id}] {meal.name} ({meal.category})")
        print(f"      Ingredients: {', '.join(meal.ingredients)}")
    print()
    
    print("Step 3: Placing Orders...")
    print("-" * 70)
    
    print("\nOrder 1: Customer 'Alice' orders ingredients for Vegan Pasta")
    order1 = service.order_ingredients(
        meal_id="M001",
        customer_name="Alice",
        delivery_date="2025-01-15"
    )
    
    print("\nOrder 2: Customer 'Bob' orders ingredients for Chicken Curry")
    order2 = service.order_ingredients(
        meal_id="M002",
        customer_name="Bob",
        delivery_date="2025-01-16"
    )
    
    print("\nOrder 3: Customer 'Alice' orders ingredients for Gluten-Free Salad")
    order3 = service.order_ingredients(
        meal_id="M003",
        customer_name="Alice",
        delivery_date="2025-01-15"
    )
    
    print("\n" + "="*70)
    print("Step 4: Viewing Order Details")
    print("="*70)
    if order1:
        service.view_order(order1.order_id)
    if order2:
        service.view_order(order2.order_id)
    
    print("\n" + "="*70)
    print("Step 5: Customer Order History")
    print("="*70)
    service.list_customer_orders("Alice")
    
    # Demonstrate data persistence
    print("\n" + "="*70)
    print("Step 6: Demonstrating Data Persistence (NFR3)")
    print("="*70)
    print("Simulating system crash and recovery...")
    print("Before crash: Orders in memory:", len(service.order_repository._orders))
    print("Persistent state: Orders saved:", len(service.order_repository.get_persistent_state()))
    
    print("\n[SYSTEM CRASH SIMULATED - In-memory data cleared]")
    service.order_repository._orders.clear()
    print("After crash: Orders in memory:", len(service.order_repository._orders))
    
    print("\nRecovering orders from persistent storage...")
    recovered = service.order_repository.recover_from_persistent_state()
    print(f"✓ Recovered {recovered} orders from persistent state")
    print("After recovery: Orders in memory:", len(service.order_repository._orders))
    
    print("\nVerifying recovered orders:")
    for order in service.order_repository.get_all_orders():
        print(f"  ✓ {order.order_id}: {order.meal.name} for {order.customer_name}")
    
    print("\n" + "="*70)
    print("Demo completed successfully!")
    print("="*70)


def display_menu():
    # Main options
    print("\n" + "="*70)
    print("SmartCater - Ingredient Ordering Service")
    print("="*70)
    print("1. Browse available meals")
    print("2. Place an order")
    print("3. View my orders")
    print("4. View order details")
    print("5. Exit")
    print("="*70)


def display_meals(service: SmartCaterService):
    # Display all meals
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
    # Interactive order placement process
    print("\n" + "-"*70)
    print("Place an Order")
    print("-"*70)
    
    # Display available meals
    meals = service.list_meals()
    if not meals:
        print("No meals available to order.")
        return
    
    print("\nAvailable Meals:")
    for meal in meals:
        print(f"  [{meal.meal_id}] {meal.name} ({meal.category})")
    
    # Get meal selection
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
    
    # Get customer name
    while True:
        customer_name = input("\nEnter your name: ").strip()
        if customer_name:
            break
        print("Name cannot be empty. Please enter your name.")
    
    # Get delivery date
    while True:
        delivery_date = input("Enter delivery date (YYYY-MM-DD) or 'today' or 'tomorrow': ").strip().lower()
        if delivery_date == 'today':
            delivery_date = date.today().isoformat()
            break
        elif delivery_date == 'tomorrow':
            delivery_date = (date.today() + timedelta(days=1)).isoformat()
            break
        elif delivery_date and len(delivery_date) == 10:
            # Basic date format validation
            try:
                datetime.strptime(delivery_date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD format.")
        else:
            print("Invalid input. Please enter a date (YYYY-MM-DD), 'today', or 'tomorrow'.")
    
    # Confirm order
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
    # View orders for a customer
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
    # View details of an order
    print("\n" + "-"*70)
    print("View Order Details")
    print("-"*70)
    
    order_id = input("Enter order ID: ").strip().upper()
    if not order_id:
        print("Order ID cannot be empty.")
        return
    
    service.view_order(order_id)


def interactive_mode():
    print("="*70)
    print("SmartCater - Ingredient Ordering Service")
    print("="*70)
    print("Welcome! This interactive mode allows you to:")
    print("  • Browse available meals")
    print("  • Place orders for meal ingredients")
    print("  • View your order history")
    print("  • View detailed order information")
    
    service = SmartCaterService()
    
    # Load sample meals
    sample_meals = create_sample_meals()
    for meal in sample_meals:
        service.add_meal(meal)
    print(f"\n✓ Loaded {len(sample_meals)} meals into catalog")
    
    # Main interaction loop
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


def main():
    import sys
    
    # Check if user wants demo mode
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo()
    else:
        interactive_mode()


if __name__ == "__main__":
    main()

