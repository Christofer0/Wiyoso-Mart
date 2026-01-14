package com.wiyomart.payment_service.app.service;


import java.math.BigDecimal;

import org.springframework.stereotype.Service;

import com.wiyomart.payment_service.app.client.OrderClient;
import com.wiyomart.payment_service.app.dto.request.PaymentRequestDto;
import com.wiyomart.payment_service.app.dto.response.OrderResponseDto;
import com.wiyomart.payment_service.app.dto.response.PaymentResponseDto;
import com.wiyomart.payment_service.app.mapper.PaymentMapper;
import com.wiyomart.payment_service.app.model.Payments;
import com.wiyomart.payment_service.app.model.PaymentStatus;
import com.wiyomart.payment_service.app.repo.PaymentRepository;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;


@Service
@RequiredArgsConstructor
@Transactional
public class PaymentService {

    private final PaymentRepository paymentRepository;
    private final OrderClient orderClient;
    private final PaymentMapper paymentMapper;

    public PaymentResponseDto createPayment(
        Long orderId,
        Long userId,
        PaymentRequestDto request,
        String token
    ) {

        OrderResponseDto order =
                orderClient.getOrderById(orderId, token);

        if (!"CREATED".equals(order.getStatus())) {
            throw new RuntimeException("Order cannot be paid");
        }

        // HITUNG TOTAL AMOUNT DARI ITEMS
        BigDecimal totalAmount = order.getItems().stream()
                .map(item -> item.getSubTotal())
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        Payments payment = new Payments();
        payment.setOrderId(order.getOrderId());
        payment.setUserId(order.getUserId()); // 🔥 FIX
        payment.setAmount(totalAmount); // 🔥 FIX
        payment.setPaymentMethod(request.getPaymentMethod());
        payment.setPaymentStatus(PaymentStatus.PENDING);

        Payments saved = paymentRepository.save(payment);

        return paymentMapper.toResponseDto(saved);
    }

}
