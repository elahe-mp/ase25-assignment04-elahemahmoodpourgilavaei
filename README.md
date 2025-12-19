# SmartCater - Ingredient Ordering Service

SmartCater is a catering ingredient-ordering service prototype that allows customers to browse meals, view ingredients, and order ingredients for selected meals. This implementation focuses on the core ordering functionality and demonstrates data persistence to prevent order loss.

## Project Description

This prototype implements:

- **FR number3**: Order ingredients for a selected meal
- **NFR number3**: Data persistence to prevent order loss on system crashes

The system provides a simple interface for customers to:

- Browse available meals and their ingredients
- Place orders for meal ingredients
- Track their orders
- Rely on data persistence to ensure orders are not lost

## Requirements

- Python 3.6 or higher
- No external dependencies

## How to Run

1. **Clone the repository**:

   ```bash
   git clone https://github.com/elahe-mp/ase25-assignment04-elahemahmoodpourgilavaei
   cd ase25-assignment04-elahemahmoodpourgilavaei
   ```

2. **Run the application**:

   ```bash
   python smart_cater.py
   ```

   Or

   ```bash
   python3 smart_cater.py
   ```

   The application provides an interactive menu-driven interface where you can:

   - Browse available meals and their ingredients
   - Place orders by selecting a meal, entering your name, and choosing a delivery date
   - View your order history
   - View detailed information about specific orders

## Project Structure

```
.
├── README.md                          # This file
├── smart_cater.py                     # Main implementation
├── meals.json                         # Meal catalog data
└── requirements/
    ├── functional.md                  # Functional requirements
    ├── nonfunctional.md               # Non-functional requirements
    ├── selected.md                    # Selected FR and NFR with explanation
    └── nfr_explanation.md             # NFR implementation explanation
```

## Notes

- This is a prototype implementation using in-memory storage
- Meal data is loaded from `meals.json` file
- The application includes sample meals and demonstrates the complete ordering workflow
- Orders are persisted in memory to prevent data loss (NFR3)
