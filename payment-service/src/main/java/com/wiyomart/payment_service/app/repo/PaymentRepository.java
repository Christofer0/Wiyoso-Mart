package com.wiyomart.payment_service.app.repo;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import com.wiyomart.payment_service.app.model.Payments;

public interface PaymentRepository extends JpaRepository<Payments,UUID>{

    
} 