"""Razorpay checkout. Creates a real order when keys are configured,
otherwise returns a stubbed message so the demo flow still works.
"""
from ..config import settings

PLAN_PRICING_INR = {"Free": 0, "Starter": 149, "Pro": 299}


def create_checkout_session(plan_name: str, provider: str = "razorpay") -> dict:
    rupees = PLAN_PRICING_INR.get(plan_name, 299)
    amount_paise = rupees * 100

    if rupees == 0:
        return {
            "message": f"{plan_name} plan is free — no checkout needed.",
            "plan": plan_name,
            "amount": 0,
            "currency": "INR",
        }

    if settings.razorpay_key_id and settings.razorpay_key_secret:
        try:
            import razorpay

            client = razorpay.Client(
                auth=(settings.razorpay_key_id, settings.razorpay_key_secret)
            )
            order = client.order.create(
                {
                    "amount": amount_paise,
                    "currency": "INR",
                    "receipt": f"nivest-{plan_name.lower()}",
                    "notes": {"plan": plan_name},
                }
            )
            return {
                "message": f"Razorpay order created for {plan_name} (₹{rupees}/mo).",
                "orderId": order.get("id"),
                "amount": amount_paise,
                "currency": "INR",
                "keyId": settings.razorpay_key_id,
                "provider": "razorpay",
            }
        except Exception as error:
            return {
                "message": f"Razorpay error for {plan_name}: {error}. Using demo checkout.",
                "plan": plan_name,
                "amount": amount_paise,
                "currency": "INR",
            }

    return {
        "message": (
            f"Checkout initiated for {plan_name} (₹{rupees}/mo). "
            "Add RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET to enable live Razorpay payments."
        ),
        "plan": plan_name,
        "amount": amount_paise,
        "currency": "INR",
    }
