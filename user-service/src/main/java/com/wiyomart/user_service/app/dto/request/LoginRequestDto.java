package com.wiyomart.user_service.app.dto.request;

import jakarta.validation.constraints.NotBlank;

public record LoginRequestDto(

        @NotBlank(message = "Username wajib diisi")
        String username,

        @NotBlank(message = "Password wajib diisi")
        String password

) {}