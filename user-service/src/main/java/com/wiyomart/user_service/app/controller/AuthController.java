package com.wiyomart.user_service.app.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.wiyomart.user_service.app.dto.request.LoginRequestDto;
import com.wiyomart.user_service.app.dto.request.UserRequestDto;
import com.wiyomart.user_service.app.dto.response.UserResponseDto;
import com.wiyomart.user_service.app.service.UserService;
import com.wiyomart.user_service.response.ApiResponse;

import jakarta.validation.Valid;
import lombok.AllArgsConstructor;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;


@RestController
@RequestMapping("/api/auth")
@AllArgsConstructor
public class AuthController {
    private final UserService userService;

    //register
    @PostMapping("/register")
    public ApiResponse<UserResponseDto> register(@Valid @RequestBody UserRequestDto request) {
        UserResponseDto responseDto = userService.createUser(request);
        
        return ApiResponse.success(responseDto, "User created successfully");
    }
    
   @PostMapping("/login")
    public ResponseEntity<ApiResponse<UserResponseDto>> login(
            @Valid @RequestBody LoginRequestDto request) {

        UserResponseDto result = userService.login(request.username(), request.password());

        return ResponseEntity.ok(
                ApiResponse.success(result, "Login berhasil")
        );
    }
    

}
