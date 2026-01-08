package com.wiyomart.order_service.app.model;

public enum OrderStatus {
    CREATED,
    WAITING_PAYMENT,
    PAID,
    CANCELLED,
    SHIPPED,
    COMPLETED
}
