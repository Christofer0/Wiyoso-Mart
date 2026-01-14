package com.wiyomart.payment_service.app.dto.response;

import java.math.BigDecimal;
import java.util.UUID;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PaymentResponseDto {
    private UUID paymentId;
    private Long orderId;
    private Long userId;
    private BigDecimal amount ;
    private String status;
    @JsonProperty("payment_method")
    private String paymentMethod;
}
