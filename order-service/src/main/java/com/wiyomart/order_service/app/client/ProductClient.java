package com.wiyomart.order_service.app.client;

import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import com.wiyomart.order_service.app.dto.response.ProductResponseDto;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ProductClient {

    private final WebClient.Builder webClientBuilder;

    public ProductResponseDto getProductById(String productId, String token) {
        return webClientBuilder.build()
                .get()
                .uri("http://localhost:9002/api/products/{id}", productId)
                .header("Authorization", "Bearer " + token)
                .retrieve()
                .bodyToMono(ProductResponseDto.class)
                .block(); // OK untuk sekarang
    }
}

