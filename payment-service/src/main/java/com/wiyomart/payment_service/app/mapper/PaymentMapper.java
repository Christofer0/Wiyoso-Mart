package com.wiyomart.payment_service.app.mapper;


import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

import com.wiyomart.payment_service.app.dto.response.PaymentResponseDto;
import com.wiyomart.payment_service.app.model.Payments;

@Mapper(componentModel = "spring")
public interface PaymentMapper {

    @Mapping(target = "paymentId", source = "id")
    @Mapping(target = "orderId", source = "orderId")
    @Mapping(target = "userId", source = "userId")
    @Mapping(target = "amount", source = "amount")
    @Mapping(target = "status", source = "paymentStatus")
    @Mapping(target = "paymentMethod", source = "paymentMethod")
    PaymentResponseDto toResponseDto(Payments payment);
}


