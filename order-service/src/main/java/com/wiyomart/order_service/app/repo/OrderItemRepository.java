package com.wiyomart.order_service.app.repo;

import org.springframework.data.jpa.repository.JpaRepository;

import com.wiyomart.order_service.app.model.OrderItem;

public interface OrderItemRepository extends JpaRepository<OrderItem,Long>{
    
}
