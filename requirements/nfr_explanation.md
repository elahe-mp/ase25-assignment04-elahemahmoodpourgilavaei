# NFR Explanation

## Selected Non-Functional Requirement

**NFR number3:** As a customer, I want the system to not lose order details if the system crashes so that my order information is preserved and I don't lose my orders or need to re-enter my orders.

## How the Implementation Addresses NFR number3

The implementation addresses this requirement by saving each order in two places at the same time. Orders are stored in an in-memory structure for normal use and also copied into a separate persistent state that represents durable storage. This allows the system to restore orders if the in-memory data is lost, simulating recovery after a crash. A recovery method shows how the system can rebuild its state using the saved order data. This approach demonstrates how order data can be protected even in a simple prototype.

## Limitations and Assumptions

Because this is a prototype, both storage structures are kept in memory, so the persistent state does not survive real crashes. In a real system, this data would be stored in a database or file system. The implementation also assumes that orders are created one at a time, without concurrent access. Despite these limitations, the prototype shows the basic idea of preserving and recovering order data.
