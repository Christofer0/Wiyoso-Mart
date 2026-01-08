package com.wiyomart.order_service.app.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import com.wiyomart.order_service.app.dto.request.CreateOrderItemRequestDto;
import com.wiyomart.order_service.app.dto.request.CreateOrderRequestDto;
import com.wiyomart.order_service.app.dto.response.CreateOrderResponseDto;
import com.wiyomart.order_service.app.model.Order;
import com.wiyomart.order_service.app.model.OrderItem;
import com.wiyomart.order_service.app.model.OrderStatus;
import com.wiyomart.order_service.app.repo.OrderRepository;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;

@Service
@Transactional
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;

    //create
    public CreateOrderResponseDto createOrder(CreateOrderRequestDto request ){
        
        // 1. Buat Order
        Order order = new Order();
        order.setUserId(1L);
        order.setStatus(OrderStatus.CREATED);

        List<OrderItem> orderItems = new ArrayList<>();
        BigDecimal totalAmount = BigDecimal.ZERO;

        // 2. Loop Item 
        for(CreateOrderItemRequestDto itemDto : request.getItems()){

            // 3 buat order item
            OrderItem item = new OrderItem();
            item.setOrder(order);
            item.setProductId(itemDto.getProductId());

            item.setProductName("DUummy Product");
            item.setProductPrice(BigDecimal.valueOf(10000));

            item.setQuantity(itemDto.getQuantity());

            BigDecimal subTotal = item.getProductPrice().multiply(BigDecimal.valueOf(item.getQuantity()));

            item.setSubtotal(subTotal);

            totalAmount = totalAmount.add(subTotal);
            orderItems.add(item);
        }

        // 4. Set ke Order 
        order.setItems(orderItems); 
        order.setTotalAMount(totalAmount);

        // 5. Simpan
        Order saveOrder = orderRepository.save(order);

        // 6. Response 
        return new CreateOrderResponseDto(
            saveOrder.getId(),
            saveOrder.getStatus().name()
        );

    }

}
