package com.wiyomart.user_service.app.dto.request;

import java.util.Set;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserUpdatePatchRequestDto {
    private String username;
    private String password;
    private Set<Long> roleIds;
    private UserProfileRequestDto profile;
}
