package com.wiyomart.payment_service.app.dto.response;

import java.math.BigDecimal;
import java.util.List;
import lombok.Data;


@Data
public class OrderResponseDto {

    private Long orderId;
    private Long userId;
    private String status;
    private List<OrderItemDto> items;

    public BigDecimal getTotalAmount() {
        return items.stream().map(OrderItemDto::getSubTotal).reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}
