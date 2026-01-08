package com.wiyomart.user_service.app.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.wiyomart.user_service.app.dto.request.UserUpdatePatchRequestDto;
import com.wiyomart.user_service.app.dto.response.UserResponseDto;
import com.wiyomart.user_service.app.service.UserService;
import com.wiyomart.user_service.response.ApiResponse;

import lombok.AllArgsConstructor;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;



@RestController
@RequestMapping("/api/users")
@AllArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<UserResponseDto>> getUserById(@PathVariable Long id) {
        
        UserResponseDto result = userService.getUserById(id);
        
        return ResponseEntity.ok(
            ApiResponse.success(result,"User fatched succesfully")
        );
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<UserResponseDto>>> getAllUsers() {

        List<UserResponseDto> result = userService.getAllUsers();

        return ResponseEntity.ok(
            ApiResponse.success(result, "List User")
        );

    }

    @PatchMapping("/{id}")
    public ResponseEntity<ApiResponse<UserResponseDto>> updatePatch(
                @PathVariable Long id ,
                @RequestBody UserUpdatePatchRequestDto request){
            
        UserResponseDto result = userService.patchUser(id,request);

        return ResponseEntity.ok(
            ApiResponse.success(result, "Patch Update Successfully"));
    }
    
}
