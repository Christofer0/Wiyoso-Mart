package com.wiyomart.order_service.app.repo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.wiyomart.order_service.app.model.Order;


@Repository
public interface OrderRepository extends JpaRepository<Order,Long>{

    
} 