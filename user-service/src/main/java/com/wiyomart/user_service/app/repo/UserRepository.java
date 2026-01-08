package com.wiyomart.user_service.app.repo;


import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.wiyomart.user_service.app.model.User;

@Repository
public interface UserRepository extends JpaRepository<User,Long>{    
    Boolean existsByUsername(String username);
    Optional<User> findByUsername(String username);
} 