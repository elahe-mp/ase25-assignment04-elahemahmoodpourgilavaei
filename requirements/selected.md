# Selected Requirements for Prototype

## Selected Functional Requirement (FR)

**FR number3:** As a customer, I want to order the ingredients for a selected meal so that I can receive everything needed to prepare it.

## Selected Non-Functional Requirement (NFR)

**NFR number3:** As a customer, I want the system to not lose order details if the system crashes so that my order information is preserved and I don't lose my orders or need to re-enter my orders.

## Explanation

### Why These Requirements Were Selected

I selected the FR number3 (Order Ingredients) because it is the core value of this application. Browsing meals and viewing ingredients are also important, but the ability to place an order is the most important action that delivers value to customers. That's the feature that that makes the service useful.

I selected NFR number3 (Data Persistence and reliability) because placing an order is a critical action that must be trustworthy. If order details are lost due to a system failure, the service becomes unreliable for users. This requirement is fundamental to building trust with users. If customers cannot rely on the system to preserve their orders, they will not use the service.

### How These Requirements Relate

These two requirements are directly related because ordering ingredients creates critical data that must be stored and protected. The FR depends on the NFR, as an order that cannot survive from a crash does not provide value to the customer.
These two together can form a complete, trustworthy ordering experience in which the user can place orders with confidence that their data will be preserved.

### Why This Scope is Reasonable for a Prototype

This FR is a good fit for the prototype because it only needs a simple ordering flow and basic data storage. A minimal version can show a customer selecting a meal, viewing its ingredients, and placing an order from start to finish. This keeps the scope manageable by avoiding complex features like delivery optimization, payments, or multi-user handling. Pairing it with the mentioned NFR ensures the prototype demonstrates reliability by safely storing order data, which helps build trust in the system.
