package com.wiyomart.order_service.app.mapper;

import com.wiyomart.order_service.app.dto.response.OrderItemResponseDto;
import com.wiyomart.order_service.app.dto.response.OrderResponseDto;
import com.wiyomart.order_service.app.model.Order;
import com.wiyomart.order_service.app.model.OrderItem;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

import java.util.List;

@Mapper(componentModel = "spring")
public interface OrderMapper {

    @Mapping(target = "orderId", source = "id")
    @Mapping(target = "userId", source = "userId")
    @Mapping(target = "status", expression = "java(order.getStatus() != null ? order.getStatus().name() : null)")
    @Mapping(target = "items", source = "items")
    OrderResponseDto toResponseDto(Order order);

    List<OrderResponseDto> toResponseDtoList(List<Order> orders);

    // Mapping item
    @Mapping(target = "itemId", source = "id")
    @Mapping(target = "productId", source = "productId")
    @Mapping(target = "productName", source = "productName")
    @Mapping(target = "productPrice", source = "productPrice")
    @Mapping(target = "quantity", source = "quantity")
    @Mapping(target = "subTotal", source = "subtotal")       
    OrderItemResponseDto toOrderItemDto(OrderItem orderItem);

    List<OrderItemResponseDto> toOrderItemDtoList(List<OrderItem> orderItems);
}