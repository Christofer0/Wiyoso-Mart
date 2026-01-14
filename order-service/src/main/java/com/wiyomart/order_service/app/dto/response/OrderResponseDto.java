package com.wiyomart.order_service.app.dto.response;

import java.util.List;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class OrderResponseDto {
    private Long orderId;
    private String status;    
    private Long userId;
    private List<OrderItemResponseDto> items;
}






