import stripe
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.user import User

settings = get_settings()
stripe.api_key = settings.stripe_secret_key

router = APIRouter(prefix="/api/Payment", tags=["Payment"])


@router.post("/create-checkout/{user_id}")
async def create_checkout(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: int = Depends(get_current_user_id),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": "Vibelink Premium",
                            "description": "Swipes ilimitados",
                        },
                        "unit_amount": 999,  # 9.99 EUR in cents
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://localhost:8000/api/Payment/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8000/api/Payment/cancel",
            metadata={"userId": str(user_id)},
        )
        return {"url": session.url}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/success")
async def success(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == "paid":
            user_id = int(session.metadata["userId"])
            user = await db.get(User, user_id)
            if user:
                user.IsPremium = True
                await db.commit()
                return "Felicidades! Ahora eres premium."
        return "Error en el pago"
    except stripe.error.StripeError:
        raise HTTPException(status_code=400, detail="Error en el pago")


@router.get("/cancel")
async def cancel():
    return "Pago cancelado"
