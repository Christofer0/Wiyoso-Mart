package com.wiyomart.user_service.app.service;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.wiyomart.user_service.app.dto.request.UserProfileRequestDto;
import com.wiyomart.user_service.app.dto.request.UserRequestDto;
import com.wiyomart.user_service.app.dto.request.UserUpdatePatchRequestDto;
import com.wiyomart.user_service.app.dto.response.UserResponseDto;
import com.wiyomart.user_service.app.mapper.UserMapper;
import com.wiyomart.user_service.app.model.Role;
import com.wiyomart.user_service.app.model.User;
import com.wiyomart.user_service.app.model.UserProfile;
import com.wiyomart.user_service.app.repo.RoleRepository;
import com.wiyomart.user_service.app.repo.UserRepository;
import com.wiyomart.user_service.app.service.UserService;
import com.wiyomart.user_service.exception.BadRequestException;
import com.wiyomart.user_service.exception.NotFoundException;
import com.wiyomart.user_service.exception.UnauthorizedException;
import com.wiyomart.user_service.util.JwtUtil;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;

@Service
@Transactional
@RequiredArgsConstructor
public class UserService {

    private final PasswordEncoder passwordEncoder;
    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final UserMapper userMapper;
    private final JwtUtil jwtUtil;

        //create
        public UserResponseDto createUser(UserRequestDto request) {
            if(userRepository.existsByUsername(request.getUsername())){
                throw new BadRequestException("username already Exists");
            }

            User user = new User();
            user.setUsername(request.getUsername());
            user.setPasswordHash(passwordEncoder.encode(request.getPassword()));
            
            Set<Role> roles = roleRepository.findAllById(request.getRoleIds()).stream().collect(Collectors.toSet());
            user.setRoles(roles);

            // create profile users
            if(request.getProfile() != null){
                UserProfile profile = new UserProfile();
                profile.setFullName(request.getProfile().getFullName());
                profile.setPhoneNumber(request.getProfile().getPhoneNumber());
                profile.setAddress(request.getProfile().getAddress());

                profile.setUser(user);
                user.setProfile(profile);
            }

            User savedUser = userRepository.save(user);

            return userMapper.toResponseDto(savedUser);
            
        }

        //LOGIN
        public UserResponseDto login(String username, String password) {
            User user = userRepository.findByUsername(username)
                    .orElseThrow(() -> new UnauthorizedException("Username atau password salah"));

            if (!passwordEncoder.matches(password, user.getPasswordHash())) {
                throw new UnauthorizedException("Username atau password salah");
            }

            UserResponseDto responseDto = userMapper.toResponseDto(user);

            Set<String> roles = responseDto.getRoles() != null ? responseDto.getRoles() : Set.of();

            String jwtToken = jwtUtil.generateToken(user.getUsername(), roles);

            responseDto.setJwt_token(jwtToken);

            return responseDto;
        }

        //get by id
        public UserResponseDto getUserById(Long id){
            User user = userRepository.findById(id).orElseThrow(() -> new NotFoundException("User not found"));

            return userMapper.toResponseDto(user);
        }

        //get all
        public List<UserResponseDto> getAllUsers(){
            return userRepository.findAll()
                    .stream()
                    .map(userMapper::toResponseDto)  
                    .collect(Collectors.toList());
        }

        //update patch
        @Transactional
        public UserResponseDto patchUser(Long id, UserUpdatePatchRequestDto request){

            User user = userRepository.findById(id).orElseThrow(() -> new NotFoundException("User not found"));

            if(request.getUsername() != null){
                user.setUsername(request.getUsername());
            }

            if(request.getPassword() != null){
                user.setPasswordHash(request.getPassword());
            }

            // roles
            if (request.getRoleIds() != null) {
                Set<Role> roles = roleRepository.findAllById(request.getRoleIds())
                        .stream()
                        .collect(Collectors.toSet());
                user.setRoles(roles);
            }

            if (request.getProfile() != null) {
                patchProfile(user, request.getProfile());
            }

            userRepository.save(user);

            return userMapper.toResponseDto(user);

        }

        private void patchProfile(User user, UserProfileRequestDto profileRequest) {

            UserProfile profile = user.getProfile();

            if (profile == null) {
                profile = new UserProfile();
                profile.setUser(user);
            }

            if (profileRequest.getFullName() != null) {
                profile.setFullName(profileRequest.getFullName());
            }

            if (profileRequest.getPhoneNumber() != null) {
                profile.setPhoneNumber(profileRequest.getPhoneNumber());
            }

            if (profileRequest.getAddress() != null) {
                profile.setAddress(profileRequest.getAddress());
            }

            user.setProfile(profile);
        }




}
