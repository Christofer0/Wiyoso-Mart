package com.wiyomart.user_service.app.mapper;

import org.mapstruct.BeanMapping;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.NullValuePropertyMappingStrategy;

import com.wiyomart.user_service.app.dto.request.UserProfileRequestDto;
import com.wiyomart.user_service.app.dto.response.ProfileResponseDto;
import com.wiyomart.user_service.app.model.UserProfile;

@Mapper(
    componentModel = "spring",
    unmappedTargetPolicy = org.mapstruct.ReportingPolicy.IGNORE  
)
public interface UserProfileMapper {

    // Entity → Response DTO
    ProfileResponseDto toResponseDto(UserProfile entity);

    // Request DTO → New Entity (untuk create baru)
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "user", ignore = true)
    UserProfile toEntity(UserProfileRequestDto dto);

    // Partial update (PATCH) — hanya update field yang tidak null di DTO
    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "user", ignore = true)
    void updateEntityFromDto(UserProfileRequestDto dto, @MappingTarget UserProfile entity);
}