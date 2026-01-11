package com.wiyomart.order_service.app.dto.response;

import java.math.BigDecimal;

import lombok.Data;

@Data
public class OrderItemResponseDto {
    private Long itemId;
    private String productId;           
    private String productName;
    private BigDecimal productPrice;
    private Integer quantity;
    private BigDecimal subTotal;        
}
