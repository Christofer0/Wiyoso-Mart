package com.wiyomart.order_service.app.dto.response;

import java.math.BigDecimal;

import lombok.Data;

@Data
public class ProductResponseDto {
    private String id;
    private String name;
    private BigDecimal price;
    private Integer stock;
}


    


