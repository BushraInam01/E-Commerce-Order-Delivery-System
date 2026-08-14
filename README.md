# E-Commerce Order & Delivery Management System

A beginner-friendly Python project for managing an e-commerce ordering and
delivery workflow. The system will be developed phase by phase using
object-oriented programming.

## Technologies Used

- Python 3
- Python standard library

## OOP Concepts to Be Demonstrated

- Classes and objects
- Encapsulation
- Inheritance
- Polymorphism
- Abstraction
- Composition

## Current Phase

**Phase 11 — Final Integration**

Phase 1 provides the project structure. Phase 2 implements the user and customer
hierarchy, including customer-specific discounts and shipping eligibility.

## Phase 3 — Product System

Phase 3 introduces the abstract `Product` base class and three specialized
product types:

- `PhysicalProduct` manages stock, weight, dimensions, and shipping needs.
- `DigitalProduct` provides download access and requires no physical shipping.
- `SubscriptionProduct` represents recurring access and automatic renewal.

The product hierarchy demonstrates encapsulation through validated properties
and controlled stock changes, inheritance through shared product state,
abstraction through a common product interface, and polymorphism through
`calculatePrice()` and `requires_shipping()`.

## Phase 4 — Shopping Cart & Order System

`ShoppingCart` manages products selected by an associated customer, merges
duplicate quantities, calculates totals polymorphically, removes products, and
creates an order only when the cart is not empty.

`Order` owns and manages its `OrderItem` objects, demonstrating Composition.
Each `OrderItem` holds a product reference and quantity and delegates pricing to
the existing `Product` abstraction when calculating its subtotal. An `Order`
also keeps a reference to the customer who placed it, demonstrating the
Customer → Order Association.

Internal item collections are encapsulated and exposed only as immutable
snapshots. Physical stock is unchanged while products remain in a cart. Before
order placement, all products validate availability polymorphically; stock is
reduced only after every validation succeeds. Successful orders start with the
read-only `CREATED` status and clear the cart. This phase does not include
discounts, taxes, payments, delivery, invoices, refunds, or later lifecycle
statuses.

## Phase 5 — Discount System

The abstract `Discount` class defines `applyDiscount(order)` for promotional,
order-level discounts. `PercentageDiscount`, `FixedAmountDiscount`,
`BuyOneGetOneDiscount`, and `SeasonalDiscount` inherit this interface and
provide their own calculations. This demonstrates abstraction, inheritance,
and polymorphism without discount type checks. Configuration values are
encapsulated and validated when each promotion is created.

An `Order` can hold one optional promotional discount. It delegates the
discount amount to that object and calculates its total as subtotal minus the
promotion, never below zero. Promotions are demonstrated independently and are
not stacked.

The BOGO assumption is that one unit is free for every pair of the same product:
`quantity // 2` free units at that product's polymorphic price. The seasonal
assumption is a configured percentage of the subtotal, with no date or time
dependency in this phase.

Customer discounts from Phase 2 remain separate customer behavior. They are not
automatically combined with Phase 5 promotional discounts; that broader final
calculation belongs to a later integration phase.

## Phase 6 — Payment System

The abstract `PaymentMethod` defines the shared `pay(amount)` and
`refund(amount)` interface. `CreditCard`, `BankTransfer`, and `DigitalWallet`
inherit that abstraction and provide distinct simulated results through
polymorphism. All methods validate positive amounts and return a consistent
result containing a status, method, amount, and method-specific message.

An `Order` can be assigned one payment method and delegates payment and refund
behavior to it. Payments use the Phase 5 total—subtotal minus one promotional
discount—with no tax, shipping, delivery, or other charges. Payment state is
encapsulated as `UNPAID`, `PAID`, or `REFUNDED`; paid and refunded amounts are
changed only through controlled operations. Partial refunds are supported and
cannot exceed the remaining refundable amount.

Order status and payment status are separate: an order remains `CREATED` while
its payment status changes. Configurations retain only safe names and masked
identifiers—never CVVs, PINs, passwords, full account numbers, or tokens. Every
payment and refund is an educational simulation; no real gateway, bank, or
wallet service is connected.

## Phase 7 — Delivery System

The abstract `DeliveryMethod` defines `calculateCost(order)` and
`getEstimatedDays()`. `StandardDelivery`, `ExpressDelivery`, and
`SameDayDelivery` inherit this interface and implement distinct fixed costs and
estimates. `Order` holds an optional delivery method through a controlled
setter and delegates both delivery calculations polymorphically.

The fixed educational assumptions are:

- Standard Delivery: 200, estimated in 3-5 days.
- Express Delivery: 500, estimated in 1-2 days.
- Same-Day Delivery: 1000, estimated the same day.

These values are demonstrations because the assignment does not specify exact
delivery pricing. There are no maps, distance calculations, routing services,
or shipping APIs.

`calculateTotal()` remains backward compatible and returns subtotal minus the
promotional discount. `calculateDeliveryCost()` returns zero without a selected
method, while `calculateFinalTotal()` adds the selected delivery cost to
`calculateTotal()`. Selecting delivery does not process payment or change the
order's `CREATED` status or its separate payment status. Tax, customer-discount
integration, and additional charges remain outside this phase.

## Phase 8 — Order Lifecycle Management

`Order` now protects its lifecycle state and exposes five controlled operations:
`mark_paid()`, `start_processing()`, `ship()`, `deliver()`, and `cancel()`. Direct
status assignment is not available, and invalid transitions raise clear errors.

The successful lifecycle is:

```text
CREATED
   ↓
PAID
   ↓
PROCESSING
   ↓
SHIPPED
   ↓
DELIVERED
```

Cancellation is available through these alternate transitions:

```text
CREATED ─────→ CANCELLED
PAID ────────→ CANCELLED
PROCESSING ──→ CANCELLED
```

`mark_paid()` requires a successful Phase 6 payment, but payment status and
order status remain separate. Payment leaves the order at `CREATED` until the
explicit lifecycle transition is requested. `ship()` requires a Phase 7
delivery method but does not inspect its concrete type.

`DELIVERED` and `CANCELLED` are terminal states. Cancellation never triggers an
automatic refund in Phase 8, even when an order has already been paid. Refund
integration and a standalone `Refund` class belong to Phase 9. No generic
status setter, external logistics operation, or additional lifecycle state was
introduced.

## Phase 9 — Invoice & Refund System

### Invoice

`Invoice` is associated with an `Order` and uses an internally generated ID
such as `INV001`. At generation time it captures the order's subtotal,
promotional discount, pre-delivery order total, delivery cost, final total, and
issue time. These values are read-only snapshots, so later order changes do not
silently alter an issued invoice. Its safe summary includes the order ID and
customer name but no payment credentials.

The captured financial calculation remains:

```text
Subtotal - Promotional Discount = Order Total
Order Total + Delivery Cost = Invoice Final Total
```

Tax, customer-discount combination, and additional charges are not included.

### Refund

`Refund` is a standalone record associated with an `Order`, with an internally
generated ID such as `REF001`, a positive amount, reason, read-only status, and
safe payment result. A new record starts as `PENDING`; successful explicit
processing changes it to `COMPLETED`, while a processing error changes it to
`FAILED`.

Refund eligibility uses the Order's existing paid and remaining-refundable
amounts. Multiple partial refunds are supported, but their completed total can
never exceed the amount paid. `Refund.process()` delegates to `Order.refund()`,
which in turn delegates the simulated transaction to the selected Phase 6
`PaymentMethod`. The Refund object never directly changes payment status or
payment totals.

### Relationships and cancellation

- Invoice → Order is an Association.
- Refund → Order is an Association.

Cancellation still does not automatically create or process a refund. A paid,
cancelled order requires an explicit Refund request. No real payment service,
tax system, persistence, return workflow, or later financial integration was
added.

## Phase 10 — Object Relationships

### 1. Composition

`Order → OrderItem` is Composition. An Order creates, owns, merges, removes, and
clears its OrderItems as components of its internal structure. The internal
collection cannot be replaced externally, and `get_items()` returns an
immutable tuple snapshot. This strong ownership fits Composition because the
Order controls how its item components participate in the order.

### 2. Association

`Customer → Order` is Association. An Order holds a read-only reference to the
Customer who placed it, but it does not create or own that Customer. Both
objects have independent lifetimes, and the Customer hierarchy remains
independent of order-item management.

### 3. Aggregation

`Store → Product` is Aggregation. Store receives and manages existing Product
objects through `add_product()`, `remove_product()`, `get_product()`, and
`list_products()`. It never creates, clones, or destroys them. A removed Product
remains usable, and the same Product object can be referenced by multiple
Stores. Its protected collection is exposed only through immutable tuple
snapshots, and duplicate product IDs within one Store are rejected.

### Relationship diagram

```text
Customer ───────── Order          Association
                    │
                    │ Composition
                    ↓
                OrderItem

Store                              Aggregation
 ├── Product
 ├── Product
 └── Product
```

These relationships express different ownership strengths in the actual
project: Composition gives Order strong control over OrderItems, Association
lets Customer and Order collaborate without lifetime ownership, and
Aggregation lets Store manage Products whose lifetimes remain independent.
Store uses the common Product behavior polymorphically and contains no concrete
product-type branches.

## Phase 11 — Final Integration

Phase 11 brings the existing systems together without introducing duplicate
domain classes or changing earlier business rules:

```text
Customer → Store → Product → ShoppingCart → Order → Discount
         → Delivery → Payment → Lifecycle → Invoice → Refund
```

### Complete workflow

1. A `PremiumCustomer` is created and its independent customer-discount
   behavior is demonstrated.
2. Existing physical, digital, and subscription products are created and used
   polymorphically.
3. A Store aggregates those independently created Product objects.
4. A ShoppingCart merges duplicate quantities and calculates its total.
5. Cart placement creates an associated Order, composes OrderItems, validates
   all stock, reduces physical stock, and clears the cart.
6. An existing promotional Discount is assigned independently of the customer
   discount.
7. An existing DeliveryMethod supplies cost and estimated delivery time.
8. An existing PaymentMethod processes the simulated payment using safe masked
   configuration.
9. Controlled lifecycle methods move the order through `CREATED → PAID →
   PROCESSING → SHIPPED → DELIVERED`.
10. Invoice generation captures an immutable financial snapshot.
11. An explicit Refund record delegates processing through the existing Order
    and PaymentMethod refund architecture.

### OOP principles demonstrated

- **Encapsulation:** private collections and state are accessed through
  read-only properties and controlled operations.
- **Inheritance:** User, Customer, Product, Discount, PaymentMethod, and
  DeliveryMethod hierarchies share common behavior.
- **Abstraction:** Product, Discount, PaymentMethod, and DeliveryMethod expose
  stable common interfaces.
- **Polymorphism:** concrete products, promotions, payments, and deliveries
  implement those shared operations without type-based dispatch.

### Object relationships

- Order → OrderItem = Composition
- Customer → Order = Association
- Store → Product = Aggregation
- Invoice → Order = Association
- Refund → Order = Association

### Financial flow

```text
Subtotal - Promotional Discount = Order Total
Order Total + Delivery Cost = Final Total
```

`calculateTotal()` remains the backward-compatible subtotal-minus-promotional-
discount calculation. The final requirements integration below expands
`calculateFinalTotal()` and payment to the complete teacher-required amount.

### Lifecycle flow

```text
CREATED → PAID → PROCESSING → SHIPPED → DELIVERED
```

Cancellation remains permitted only from `CREATED`, `PAID`, or `PROCESSING` and
does not automatically create a refund. `DELIVERED` and `CANCELLED` remain
terminal states.

### Payment and refund

Payment uses the existing polymorphic PaymentMethod simulation and never stores
unmasked credentials. Refund is always explicit: its `process()` operation
delegates to Order, which delegates to the selected PaymentMethod and maintains
the paid/refunded totals. No database, notification service, reporting feature,
return workflow, or unrelated future functionality was added.

## Final Requirements Integration

The final requirements-gap pass implements the teacher's complete formula:

```text
Product Subtotal
+ Shipping
+ Tax
- Customer Discount
- Promotional Discount
+ Additional Charges
= Final Amount
```

### Financial components

- **Product subtotal:** delegated to composed OrderItems and polymorphic Product
  pricing.
- **Shipping:** delegated to the selected DeliveryMethod and kept separate from
  every other charge.
- **Tax:** delegated through the abstract `Tax` interface. `PercentageTax`
  calculates a validated percentage of product subtotal; `FixedTax` provides a
  validated fixed alternative.
- **Customer discount:** delegated to the associated Customer's existing
  polymorphic `calculateDiscount()` behavior and capped at product subtotal.
- **Promotional discount:** remains the one optional Phase 5 Discount object and
  is displayed separately from customer discount.
- **Additional charges:** immutable, named `AdditionalCharge` objects are
  validated, stored privately, and summed independently of tax and shipping.
- **Final amount:** cannot be negative and is now the amount passed to the
  selected PaymentMethod.

`calculateTotal()` is preserved for backward compatibility as subtotal minus
promotional discount. `calculateFinalTotal()` represents the complete formula.

### OOP principles

- **Encapsulation:** tax configuration, charge values, Order financial state,
  payment totals, lifecycle state, and collections use private state with
  validated operations and read-only properties.
- **Abstraction:** Product, Discount, PaymentMethod, DeliveryMethod, Customer
  behavior, and Tax expose common interfaces.
- **Inheritance:** existing hierarchies remain intact, with `PercentageTax` and
  `FixedTax` inheriting from `Tax`.
- **Polymorphism:** financial and operational behavior is delegated without
  concrete-type branching.

### Object relationships

- Order → OrderItem = Composition
- Customer → Order = Association
- Invoice → Order = Association
- Refund → Order = Association
- Store → Product = Aggregation

### Complete workflow

```text
Customer → Product → Store → Cart → Order → Discount → Tax
         → Delivery → Payment → Lifecycle → Invoice → Refund
```

Invoice remains an immutable snapshot and now captures subtotal, shipping, tax,
customer discount, promotional discount, additional charges, and final amount.
Refund remains explicit and delegates `Refund → Order → PaymentMethod`, using
the amount actually paid as its source of truth. Cancellation still does not
automatically refund payment. No database, external service, framework, or
unrelated future feature was introduced.
