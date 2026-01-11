package com.wiyomart.order_service.app.controller;


import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.wiyomart.order_service.app.dto.request.OrderRequestDto;
import com.wiyomart.order_service.app.dto.response.OrderResponseDto;
import com.wiyomart.order_service.app.service.OrderService;
import com.wiyomart.order_service.response.ApiResponse;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;

        @PostMapping
        public ResponseEntity<ApiResponse<OrderResponseDto>> createOrder(
                @Valid @RequestBody OrderRequestDto request,
                HttpServletRequest httpServletRequest) {

                Long userId = (Long) httpServletRequest.getAttribute("userId");

                String authHeader = httpServletRequest.getHeader("Authorization");
                String token = authHeader.substring(7); 

                OrderResponseDto response =
                        orderService.createOrder(userId, request, token);

                return ResponseEntity
                        .status(HttpStatus.CREATED)
                        .body(ApiResponse.success(response, "Order created successfully"));
        }

        @GetMapping
        public ResponseEntity<ApiResponse<List<OrderResponseDto>>>getAllOrders() {
                List<OrderResponseDto> result = orderService.getAllOrders();

                return ResponseEntity.ok(ApiResponse.success(result,"Lust Order"));
        }

        @GetMapping("/{id}")
        public ResponseEntity<ApiResponse<OrderResponseDto>> getOrderById(@PathVariable Long id) {
                OrderResponseDto result = orderService.getOrderById(id);
                
                return ResponseEntity.ok(
                        ApiResponse.<OrderResponseDto>success(result, "Order retrieved successfully")
                );
        }



}
