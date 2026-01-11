package com.wiyomart.order_service.app.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import com.wiyomart.order_service.app.dto.request.OrderItemRequestDto;
import com.wiyomart.order_service.app.dto.request.OrderRequestDto;
import com.wiyomart.order_service.app.dto.response.OrderResponseDto;
import com.wiyomart.order_service.app.dto.response.ProductResponseDto;
import com.wiyomart.order_service.app.mapper.OrderMapper;
import com.wiyomart.order_service.app.model.Order;
import com.wiyomart.order_service.app.model.OrderItem;
import com.wiyomart.order_service.app.model.OrderStatus;
import com.wiyomart.order_service.app.repo.OrderRepository;
import com.wiyomart.order_service.app.client.ProductClient;

import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@Transactional
@RequiredArgsConstructor
@Slf4j
public class OrderService {
    private final OrderRepository orderRepository;
    private final ProductClient productClient;
    private final OrderMapper orderMapper;
    //create
    public OrderResponseDto createOrder(Long userId,OrderRequestDto request,String token ){
        
        // 1. Buat Order
        Order order = new Order();
        order.setUserId(userId);
        order.setStatus(OrderStatus.CREATED);

        List<OrderItem> orderItems = new ArrayList<>();
        BigDecimal totalAmount = BigDecimal.ZERO;

        // 2. Loop Item 
        for (OrderItemRequestDto itemDto : request.getItems()) {

            ProductResponseDto product =
                    productClient.getProductById(itemDto.getProductId(),token);

            OrderItem item = new OrderItem();
            item.setOrder(order);
            item.setProductId(itemDto.getProductId());
            item.setProductName(product.getName());
            item.setProductPrice(product.getPrice());
            item.setQuantity(itemDto.getQuantity());

            BigDecimal subTotal =
                    product.getPrice()
                        .multiply(BigDecimal.valueOf(itemDto.getQuantity()));

            item.setSubtotal(subTotal);

            totalAmount = totalAmount.add(subTotal);
            orderItems.add(item);
        }


        // 4. Set ke Order 
        order.setItems(orderItems); 
        order.setTotalAmount(totalAmount);

        // 5. Simpan
        Order saveOrder = orderRepository.save(order);

        // 6. Response 
        // 6. Response 
        return orderMapper.toResponseDto(saveOrder);

    }

    //get all
    public List<OrderResponseDto> getAllOrders() {
        List<Order> orders = orderRepository.findAll();
        return orderMapper.toResponseDtoList(orders);
    }

    // public OrderResponseDto getOrderById(Long orderId){
    //     Order order = orderRepository.findById(orderId).orElseThrow(() -> new RuntimeException("Order not found"));
    //     return orderMapper.toResponseDto(order);
    // }

    public OrderResponseDto getOrderById(Long id) {
    log.info("Fetching order with id: {}", id);
    
    Order order = orderRepository.findById(id)
        .orElseThrow(() -> new EntityNotFoundException("Order not found with id: " + id));
    
    log.info("Order found - items size: {}", order.getItems() != null ? order.getItems().size() : "null");
    
    return orderMapper.toResponseDto(order);
}

}
