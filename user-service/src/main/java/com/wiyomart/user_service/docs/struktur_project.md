**Struktur Project — user_service**

Dokumen ini menjelaskan struktur folder dan peran utama pada project `user_service` (micro-service untuk manajemen user).

**Struktur Direktori (ringkasan)**

````
user_service/
	UserServiceApplication.java
	app/
		controller/
			AuthController.java
			UserController.java
		```
		user-service/
		├── src/
		│   ├── main/
		│   │   ├── java/
		│   │   │   └── com/wiyomart/user_service/
		│   │   │       ├── UserServiceApplication.java           # Main Application Class
		│   │   │       ├── app/                                  # App Layer (Business Logic)
		│   │   │       │   ├── controller/
		│   │   │       │   │   └── AuthController.java
		│   │   │       │   ├── dto/                              # Data Transfer Objects
		│   │   │       │   │   ├── request/
		│   │   │       │   │   │   ├── UserRequestDto.java
		│   │   │       │   │   │   └── UserProfileRequestDto.java
		│   │   │       │   │   └── response/
		│   │   │       │   │       ├── UserResponseDto.java
		│   │   │       │   │       └── ProfileResponseDto.java
		│   │   │       │   ├── mapper/                           # Entity-DTO Mappers
		│   │   │       │   │   ├── UserMapper.java
		│   │   │       │   │   └── UserProfileMapper.java
		│   │   │       │   ├── model/                            # Entity Classes (JPA)
		│   │   │       │   │   ├── User.java
		│   │   │       │   │   ├── UserProfile.java
		│   │   │       │   │   ├── Role.java
		│   │   │       │   │   └── UserStatus.java
		│   │   │       │   ├── repo/                             # Repository Interfaces
		│   │   │       │   │   ├── UserRepository.java
		│   │   │       │   │   ├── UserProfileRepository.java
		│   │   │       │   │   └── RoleRepository.java
		│   │   │       │   └── service/                          # Service Layer (Business Logic)
		│   │   │       │       ├── UserService.java
		│   │   │       │       └── impl/
		│   │   │       │           └── UserServiceImpl.java
		│   │   │       ├── config/                               # Configuration Classes
		│   │   │       │   └── (kosong - siap untuk konfigurasi tambahan)
		│   │   │       ├── security/                             # Security Configuration
		│   │   │       │   └── SecurityConfig.java
		│   │   │       └── common/                               # Common & Utility Classes
		│   │   │           ├── constant/                         # Konstanta Aplikasi
		│   │   │           ├── exception/                        # Custom Exceptions
		│   │   │           │   └── BadRequestException.java
		│   │   │           ├── response/
    │   │   │           │   ├── ApiResponse.java              # Response Wrappers
		│   │   │           └── util/                             # Utility Classes
		│   │   └── resources/
		│   │       ├── application.properties                    # Application Configuration
		│   │       ├── static/                                   # Static Resources
		│   │       └── templates/                                # Template Files
		│   └── test/
		│       └── java/
		│           └── com/wiyomart/user_service/
		│               └── UserServiceApplicationTests.java
		├── pom.xml                                               # Maven Configuration
		└── mvnw / mvnw.cmd                                       # Maven Wrapper
		```
- **`app/service`**: Logika bisnis utama.
````
