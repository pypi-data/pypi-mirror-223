import logging
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from investing_algorithm_framework.domain.models import OrderType, \
    OrderSide, Order, OrderStatus, OrderFee
from investing_algorithm_framework.infrastructure.database import SQLBaseModel
from investing_algorithm_framework.infrastructure.models.model_extension \
    import SQLAlchemyModelExtension

logger = logging.getLogger(__name__)


class SQLOrder(SQLBaseModel, Order, SQLAlchemyModelExtension):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, unique=True)
    external_id = Column(Integer)
    target_symbol = Column(String)
    trading_symbol = Column(String)
    side = Column(String, nullable=False, default=OrderSide.BUY.value)
    type = Column(String, nullable=False, default=OrderType.LIMIT.value)
    price = Column(Float)
    amount = Column(Float)
    filled_amount = Column(Float)
    remaining_amount = Column(Float)
    cost = Column(Float)
    status = Column(String)
    position_id = Column(Integer, ForeignKey('positions.id'))
    position = relationship("SQLPosition", back_populates="orders")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    trade_closed_at = Column(DateTime, default=None)
    trade_closed_price = Column(Float, default=None)
    net_gain = Column(Float, default=0)
    fee = relationship(
        "SQLOrderFee",
        uselist=False,
        back_populates="order",
        cascade="all, delete"
    )

    def __init__(
        self,
        side,
        type,
        status,
        amount,
        position_id=None,
        target_symbol=None,
        trading_symbol=None,
        external_id=None,
        price=None,
        created_at=None,
        updated_at=None,
        trade_closed_at=None,
        trade_closed_price=None,
        net_gain=0,
        filled_amount=None,
        remaining_amount=None,
        cost=None,
        fee=None
    ):
        super().__init__(
            target_symbol=target_symbol,
            trading_symbol=trading_symbol,
            type=type,
            side=side,
            status=status,
            amount=amount,
            price=price,
            external_id=external_id,
            position_id=position_id,
            net_gain=net_gain,
            trade_closed_at=trade_closed_at,
            trade_closed_price=trade_closed_price,
            created_at=created_at,
            updated_at=updated_at,
            filled_amount=filled_amount,
            remaining_amount=remaining_amount,
            cost=cost,
            fee=fee
        )

    @staticmethod
    def from_order(order):
        return SQLOrder(
            external_id=order.external_id,
            amount=order.get_amount(),
            price=order.price,
            type=order.get_type(),
            side=order.get_side(),
            status=order.get_status(),
            target_symbol=order.get_target_symbol(),
            trading_symbol=order.get_trading_symbol(),
            created_at=order.get_created_at(),
            updated_at=order.get_updated_at(),
            trade_closed_at=order.get_trade_closed_at(),
            trade_closed_price=order.get_trade_closed_price(),
            net_gain=order.get_net_gain(),
        )

    @staticmethod
    def from_ccxt_order(ccxt_order):
        status = OrderStatus.from_value(ccxt_order["status"])
        target_symbol = ccxt_order.get("symbol").split("/")[0]
        trading_symbol = ccxt_order.get("symbol").split("/")[1]

        return Order(
            external_id=ccxt_order.get("id", None),
            target_symbol=target_symbol,
            trading_symbol=trading_symbol,
            price=ccxt_order.get("price", None),
            amount=ccxt_order.get("amount", None),
            status=status,
            type=ccxt_order.get("type", None),
            side=ccxt_order.get("side", None),
            filled_amount=ccxt_order.get("filled", None),
            remaining_amount=ccxt_order.get("remaining", None),
            cost=ccxt_order.get("cost", None),
            fee=OrderFee.from_ccxt_fee(ccxt_order.get("fee", None)),
            created_at=ccxt_order.get("datetime", None),
        )
