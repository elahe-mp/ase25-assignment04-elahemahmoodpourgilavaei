# SmartCater - Ingredient Ordering Service

SmartCater is a catering ingredient-ordering service prototype that allows customers to browse meals, view ingredients, and order ingredients for selected meals. This implementation focuses on the core ordering functionality and demonstrates data persistence to prevent order loss.

## Project Description

This prototype implements:

- **FR3**: Order ingredients for a selected meal
- **NFR3**: Data persistence to prevent order loss on system crashes

The system provides a simple interface for customers to:

- Browse available meals and their ingredients
- Place orders for meal ingredients
- Track their orders
- Rely on data persistence to ensure orders are not lost

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## How to Run

1. **Clone the repository**:

   ```bash
   git clone https://github.com/elahe-mp/ase25-assignment04-elahemahmoodpourgilavaei
   cd ase25-assignment04-elahemahmoodpourgilavaei
   ```

2. **Run in interactive mode** (default):

   ```bash
   python smart_cater.py
   ```

   Or

   ```bash
   python3 smart_cater.py
   ```

   The interactive mode provides a menu-driven interface where you can:

   - Browse available meals and their ingredients
   - Place orders by selecting a meal, entering your name, and choosing a delivery date
   - View your order history
   - View detailed information about specific orders

3. **Run automated demo**:

   ```bash
   python smart_cater.py --demo
   ```

   Or:

   ```bash
   python3 smart_cater.py --demo
   ```

   The automated demo shows:

   - Loading sample meals into the catalog
   - Displaying available meals with their ingredients
   - Placing multiple orders for different customers
   - Viewing order details
   - Listing customer order history
   - Demonstrating data persistence by simulating a system crash and recovery

## Project Structure

```
.
├── README.md                          # This file
├── smart_cater.py                     # Main implementation
└── requirements/
    ├── functional.md                  # Functional requirements
    ├── nonfunctional.md               # Non-functional requirements
    ├── selected.md                    # Selected FR and NFR with explanation
    └── nfr_explanation.md             # NFR implementation explanation
```

## Notes

- This is a prototype implementation using in-memory storage
- The demo includes sample data and demonstrates the complete ordering workflow
