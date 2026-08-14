"""Final teacher-requirements integration demonstration."""

from charges.additional_charge import AdditionalCharge
from delivery.delivery_method import ExpressDelivery
from discounts.discount import PercentageDiscount
from models.cart import ShoppingCart
from models.customer import PremiumCustomer
from models.product import DigitalProduct, PhysicalProduct, SubscriptionProduct
from payments.payment_method import CreditCard
from store.store import Store
from taxes.tax import PercentageTax


def section(title):
    """Print a readable demonstration section."""
    print(f"\n=== {title} ===")


def main():
    """Run the complete teacher-required order workflow."""
    section("CUSTOMER")
    customer = PremiumCustomer("C001", "Ali", "ali@example.com")
    print(f"Customer: {customer.name}")
    print(f"Role: {customer.display_role()}")

    section("PRODUCTS / STORE / AGGREGATION")
    physical_product = PhysicalProduct(
        "P001", "Headphones", "Wireless headphones", 2000.0,
        stock=10, weight=0.4, dimensions="20 x 18 x 8 cm"
    )
    digital_product = DigitalProduct(
        "P002", "Design Pack", "Downloadable assets", 1000.0,
        download_url="https://example.com/design-pack"
    )
    subscription_product = SubscriptionProduct(
        "P003", "Learning Plan", "Monthly access", 500.0,
        subscription_duration=1, auto_renew=True
    )
    products = [physical_product, digital_product, subscription_product]
    store = Store("S001", "Main Store")
    for product in products:
        store.add_product(product)
        print(
            f"{product.name}: Price={product.calculatePrice()}, "
            f"Requires Shipping={product.requires_shipping()}"
        )

    section("SHOPPING CART / ORDER")
    cart = ShoppingCart(customer)
    try:
        cart.add_product(physical_product, 0)
    except ValueError as error:
        print(f"Invalid quantity rejected: {error}")
    cart.add_product(physical_product, 1)
    cart.add_product(physical_product, 1)
    cart.add_product(digital_product, 2)
    cart.add_product(subscription_product, 1)
    print(f"Cart Total: {cart.calculate_total()}")
    print(f"Physical Stock Before Order: {physical_product.stock}")
    order = cart.place_order("O001")
    print(f"Physical Stock After Order: {physical_product.stock}")
    print(f"Associated Customer: {order.customer.name}")
    for item in order.get_items():
        print(f"OrderItem: {item.product.name} x {item.quantity}")

    section("FINANCIAL CONFIGURATION")
    order.set_discount(PercentageDiscount(10))
    order.set_delivery_method(ExpressDelivery())
    order.set_tax(PercentageTax(5))
    order.add_additional_charge(AdditionalCharge("Handling Fee", 100))

    subtotal = order.calculateSubtotal()
    shipping = order.calculateShipping()
    tax = order.calculateTax()
    customer_discount = order.calculateCustomerDiscount()
    promotional_discount = order.calculateDiscount()
    additional_charges = order.calculateAdditionalCharges()
    final_amount = order.calculateFinalTotal()

    section("FINAL FINANCIAL CALCULATION")
    print(f"Product Subtotal:             {subtotal}")
    print(f"Shipping:                     {shipping}")
    print(f"Tax:                          {tax}")
    print(f"Customer Discount:           -{customer_discount}")
    print(f"Promotional Discount:        -{promotional_discount}")
    print(f"Additional Charges:           {additional_charges}")
    print("-------------------------------------")
    print(f"Final Amount:                 {final_amount}")
    print(f"Legacy Order Total (subtotal - promotion): {order.calculateTotal()}")

    section("PAYMENT")
    try:
        order.pay()
    except ValueError as error:
        print(f"Missing payment method rejected: {error}")
    order.set_payment_method(CreditCard("Ali", "**** **** **** 1234"))
    print(f"Payment Result: {order.pay()}")
    print(f"Amount Paid: {order.amount_paid}")
    print(f"Payment Status: {order.payment_status}")

    section("ORDER LIFECYCLE")
    try:
        order.ship()
    except ValueError as error:
        print(f"Invalid transition rejected: {error}")
    order.mark_paid()
    order.start_processing()
    order.ship()
    order.deliver()
    print(f"Order Status: {order.status}")

    section("INVOICE")
    invoice = order.generate_invoice()
    print(invoice.summary())

    section("REFUND")
    refund = order.create_refund(1000, "Customer request")
    print(f"Refund ID: {refund.refund_id}")
    print(f"Refund Status Before: {refund.status}")
    refund.process()
    print(f"Refund Status After: {refund.status}")
    print(f"Remaining Refundable: {order.remaining_refundable_amount}")
    try:
        order.create_refund(
            order.remaining_refundable_amount + 1,
            "Exceeds remaining refundable amount",
        )
    except ValueError as error:
        print(f"Excess refund rejected: {error}")


if __name__ == "__main__":
    main()
