package com.wiyomart.order_service.app.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class CreateOrderResponseDto {
    private Long orderId;
    private String status;    
}






