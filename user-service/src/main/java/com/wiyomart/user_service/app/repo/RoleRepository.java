package com.wiyomart.user_service.app.repo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.wiyomart.user_service.app.model.Role;

@Repository
public interface RoleRepository extends JpaRepository<Role,Long>{
    
}
