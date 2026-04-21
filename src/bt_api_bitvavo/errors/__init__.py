from bt_api_base.error import ErrorTranslator, UnifiedErrorCode


class BitvavoErrorTranslator(ErrorTranslator):
    ERROR_MAP = {
        "100": (UnifiedErrorCode.INVALID_API_KEY, "Invalid API key"),
        "101": (UnifiedErrorCode.PERMISSION_DENIED, "No permission for this endpoint"),
        "200": (UnifiedErrorCode.INSUFFICIENT_BALANCE, "Insufficient balance"),
        "201": (UnifiedErrorCode.INVALID_VOLUME, "Order volume too small"),
        "202": (UnifiedErrorCode.INVALID_PRICE, "Price is invalid"),
        "203": (UnifiedErrorCode.MIN_NOTIONAL, "Order value is below minimum"),
        "204": (UnifiedErrorCode.INVALID_ORDER_TYPE, "Invalid order type"),
        "205": (UnifiedErrorCode.INVALID_SIDE, "Invalid order side"),
        "300": (UnifiedErrorCode.RATE_LIMIT_EXCEEDED, "Rate limit exceeded"),
        "301": (UnifiedErrorCode.IP_BANNED, "IP banned"),
        "400": (UnifiedErrorCode.INVALID_SYMBOL, "Market does not exist"),
        "401": (UnifiedErrorCode.ORDER_NOT_FOUND, "Order not found"),
        "402": (UnifiedErrorCode.ORDER_ALREADY_FILLED, "Order already filled"),
        "403": (UnifiedErrorCode.MARKET_CLOSED, "Market is closed"),
        "500": (UnifiedErrorCode.INTERNAL_ERROR, "Internal server error"),
        "501": (UnifiedErrorCode.EXCHANGE_OVERLOADED, "Service temporarily unavailable"),
    }


__all__ = ["BitvavoErrorTranslator"]
