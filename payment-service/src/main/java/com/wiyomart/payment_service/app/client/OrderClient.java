package com.wiyomart.payment_service.app.client;

import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import com.wiyomart.payment_service.app.dto.response.OrderResponseDto;
import com.wiyomart.payment_service.response.ApiResponse;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class OrderClient {
    private final WebClient.Builder webClientBuilder;

    public OrderResponseDto getOrderById(Long orderId, String token) {
        ApiResponse<OrderResponseDto> response =
            webClientBuilder.build()
                .get()
                .uri("http://localhost:9001/api/orders/{id}", orderId)
                .header("Authorization", "Bearer " + token)
                .retrieve()
                .bodyToMono(new ParameterizedTypeReference<ApiResponse<OrderResponseDto>>() {})
                .block();

        return response.getData();
    }

}

