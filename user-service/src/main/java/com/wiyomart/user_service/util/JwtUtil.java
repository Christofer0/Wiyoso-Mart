package com.wiyomart.user_service.util;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.util.Date;
import java.util.Set;

@Component
public class JwtUtil {

    // @Value("${jwt.secret}")
    // private String secret;
    private final SecretKey key = Keys.hmacShaKeyFor(
    Decoders.BASE64.decode("superlongbase64secretkeythatisveryrandomandsecure1234567890==")
    );

    private SecretKey getSigningKey() {
        return key;
    }

    // Expiration: 24 jam (bisa diubah)
    private final long EXPIRATION_TIME = 1000 * 60 * 60 * 24; // 24 hours

    // Method untuk mendapatkan signing key dari secret string
    // private SecretKey getSigningKey() {
    //     byte[] keyBytes = Decoders.BASE64.decode(secret);
    //     return Keys.hmacShaKeyFor(keyBytes);
    // }

    // Generate token
    public String generateToken(String username, Set<String> roles) {
        return Jwts.builder()
                .subject(username)
                .claim("roles", roles)
                .issuedAt(new Date())
                .expiration(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
                .signWith(getSigningKey())  // ← pakai method ini
                .compact();
    }

    // Extract all claims
    public Claims extractAllClaims(String token) {
        return Jwts.parser()
                .verifyWith(getSigningKey())  // ← pakai method ini
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }

    public String extractUsername(String token) {
        return extractAllClaims(token).getSubject();
    }

    public boolean isTokenExpired(String token) {
        return extractAllClaims(token).getExpiration().before(new Date());
    }

    public boolean validateToken(String token, String username) {
        return username.equals(extractUsername(token)) && !isTokenExpired(token);
    }
}