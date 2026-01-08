package com.wiyomart.user_service.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

/**
 * Custom exception untuk kasus autentikasi gagal
 * (username/password salah, token invalid, dll)
 * 
 * Otomatis akan menghasilkan HTTP status 401 Unauthorized
 * ketika ditangkap oleh @ControllerAdvice atau langsung dilempar
 */
@ResponseStatus(HttpStatus.UNAUTHORIZED)  // ← penting: langsung return 401
public class UnauthorizedException extends RuntimeException {

    public UnauthorizedException() {
        super("Autentikasi gagal");
    }

    public UnauthorizedException(String message) {
        super(message);
    }

    public UnauthorizedException(String message, Throwable cause) {
        super(message, cause);
    }
}