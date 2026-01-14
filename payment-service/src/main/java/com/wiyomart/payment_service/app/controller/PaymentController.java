package com.wiyomart.payment_service.app.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.wiyomart.payment_service.app.dto.request.PaymentRequestDto;
import com.wiyomart.payment_service.app.dto.response.PaymentResponseDto;
import com.wiyomart.payment_service.app.service.PaymentService;
import com.wiyomart.payment_service.response.ApiResponse;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;


@RestController
@RequestMapping("/api/payments")
@RequiredArgsConstructor
public class PaymentController {

    private final PaymentService paymentService;

    @PostMapping("/{orderId}")
    public ResponseEntity<ApiResponse<PaymentResponseDto>> createPayment(
            @PathVariable Long orderId,
            @Valid @RequestBody PaymentRequestDto request,
            HttpServletRequest httpServletRequest
    ) {
        Long userId = (Long) httpServletRequest.getAttribute("user_id");
        String authHeader = httpServletRequest.getHeader("Authorization");
        String token = authHeader.substring(7);

        PaymentResponseDto response =
                paymentService.createPayment(orderId,userId,request, token);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(ApiResponse.success(response, "Payment created"));
    }
}


    

