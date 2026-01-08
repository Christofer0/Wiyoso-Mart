package com.wiyomart.user_service.app.mapper;

import java.util.Set;
import java.util.stream.Collectors;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

import com.wiyomart.user_service.app.dto.response.UserResponseDto;
import com.wiyomart.user_service.app.model.Role;
import com.wiyomart.user_service.app.model.User;

@Mapper(componentModel = "spring")
public interface UserMapper {
    UserMapper INSTANCE = Mappers.getMapper(UserMapper.class);

    @Mapping(target = "jwt_token", ignore = true)
    @Mapping(target = "roles",source = "roles")
    @Mapping(target = "profile",source = "profile")
    UserResponseDto toResponseDto(User user);

    default Set<String> mapRoles(Set<Role> roles) {
        if (roles == null) return null;
        return roles.stream()
                .map(Role::getName)
                .collect(Collectors.toSet());
    }

} 