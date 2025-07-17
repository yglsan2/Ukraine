package com.ukraine.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

/**
 * Entité représentant un utilisateur de l'application Lumières d'Ukraine.
 * 
 * <p>Cette entité gère les informations des utilisateurs qui peuvent être
 * à la fois propriétaires de livres et emprunteurs. Elle inclut la gestion
 * des rôles, de l'adhésion et des informations de contact.</p>
 * 
 * @author Équipe Lumières d'Ukraine
 * @version 1.0.0
 * @since 2024-01-01
 */
@Entity
@Table(name = "users", indexes = {
    @Index(name = "idx_user_email", columnList = "email", unique = true),
    @Index(name = "idx_user_city", columnList = "city"),
    @Index(name = "idx_user_membership_status", columnList = "membership_status")
})
@EntityListeners(AuditingEntityListener.class)
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "L'email est obligatoire")
    @Email(message = "Format d'email invalide")
    @Column(unique = true, nullable = false)
    private String email;

    @NotBlank(message = "Le mot de passe est obligatoire")
    @Size(min = 8, message = "Le mot de passe doit contenir au moins 8 caractères")
    @Column(nullable = false)
    private String password;

    @NotBlank(message = "Le prénom est obligatoire")
    @Size(max = 50, message = "Le prénom ne peut pas dépasser 50 caractères")
    @Column(name = "first_name", nullable = false)
    private String firstName;

    @NotBlank(message = "Le nom de famille est obligatoire")
    @Size(max = 50, message = "Le nom de famille ne peut pas dépasser 50 caractères")
    @Column(name = "last_name", nullable = false)
    private String lastName;

    @Size(max = 20, message = "Le numéro de téléphone ne peut pas dépasser 20 caractères")
    @Column(name = "phone_number")
    private String phoneNumber;

    @NotBlank(message = "La ville est obligatoire")
    @Size(max = 100, message = "La ville ne peut pas dépasser 100 caractères")
    @Column(nullable = false)
    private String city;

    @Size(max = 10, message = "Le code postal ne peut pas dépasser 10 caractères")
    @Column(name = "postal_code")
    private String postalCode;

    @Column(name = "latitude")
    private Double latitude;

    @Column(name = "longitude")
    private Double longitude;

    @Enumerated(EnumType.STRING)
    @Column(name = "membership_status", nullable = false)
    private MembershipStatus membershipStatus = MembershipStatus.NOT_MEMBER;

    @Column(name = "membership_number")
    private String membershipNumber;

    @Column(name = "membership_start_date")
    private LocalDateTime membershipStartDate;

    @Column(name = "membership_end_date")
    private LocalDateTime membershipEndDate;

    @Column(name = "is_active", nullable = false)
    private Boolean isActive = true;

    @Column(name = "email_verified", nullable = false)
    private Boolean emailVerified = false;

    @Column(name = "last_login_date")
    private LocalDateTime lastLoginDate;

    @Enumerated(EnumType.STRING)
    @Column(name = "preferred_language", nullable = false)
    private Language preferredLanguage = Language.FRENCH;

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "user_roles", joinColumns = @JoinColumn(name = "user_id"))
    @Column(name = "role")
    @Enumerated(EnumType.STRING)
    private Set<UserRole> roles = new HashSet<>();

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    // Constructeurs
    public User() {
        // Constructeur par défaut requis par JPA
    }

    public User(String email, String password, String firstName, String lastName, String city) {
        this.email = email;
        this.password = password;
        this.firstName = firstName;
        this.lastName = lastName;
        this.city = city;
    }

    // Getters et Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getPostalCode() {
        return postalCode;
    }

    public void setPostalCode(String postalCode) {
        this.postalCode = postalCode;
    }

    public Double getLatitude() {
        return latitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public Double getLongitude() {
        return longitude;
    }

    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }

    public MembershipStatus getMembershipStatus() {
        return membershipStatus;
    }

    public void setMembershipStatus(MembershipStatus membershipStatus) {
        this.membershipStatus = membershipStatus;
    }

    public String getMembershipNumber() {
        return membershipNumber;
    }

    public void setMembershipNumber(String membershipNumber) {
        this.membershipNumber = membershipNumber;
    }

    public LocalDateTime getMembershipStartDate() {
        return membershipStartDate;
    }

    public void setMembershipStartDate(LocalDateTime membershipStartDate) {
        this.membershipStartDate = membershipStartDate;
    }

    public LocalDateTime getMembershipEndDate() {
        return membershipEndDate;
    }

    public void setMembershipEndDate(LocalDateTime membershipEndDate) {
        this.membershipEndDate = membershipEndDate;
    }

    public Boolean getIsActive() {
        return isActive;
    }

    public void setIsActive(Boolean isActive) {
        this.isActive = isActive;
    }

    public Boolean getEmailVerified() {
        return emailVerified;
    }

    public void setEmailVerified(Boolean emailVerified) {
        this.emailVerified = emailVerified;
    }

    public LocalDateTime getLastLoginDate() {
        return lastLoginDate;
    }

    public void setLastLoginDate(LocalDateTime lastLoginDate) {
        this.lastLoginDate = lastLoginDate;
    }

    public Language getPreferredLanguage() {
        return preferredLanguage;
    }

    public void setPreferredLanguage(Language preferredLanguage) {
        this.preferredLanguage = preferredLanguage;
    }

    public Set<UserRole> getRoles() {
        return roles;
    }

    public void setRoles(Set<UserRole> roles) {
        this.roles = roles;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }

    // Méthodes utilitaires
    public String getFullName() {
        return firstName + " " + lastName;
    }

    public boolean hasRole(UserRole role) {
        return roles.contains(role);
    }

    public boolean isMember() {
        return membershipStatus == MembershipStatus.ACTIVE;
    }

    public boolean isMembershipExpired() {
        return membershipEndDate != null && membershipEndDate.isBefore(LocalDateTime.now());
    }

    // Énumérations
    public enum MembershipStatus {
        NOT_MEMBER("Non adhérent"),
        ACTIVE("Adhérent actif"),
        EXPIRED("Adhésion expirée"),
        PENDING("Adhésion en attente");

        private final String displayName;

        MembershipStatus(String displayName) {
            this.displayName = displayName;
        }

        public String getDisplayName() {
            return displayName;
        }
    }

    public enum UserRole {
        USER("Utilisateur"),
        OWNER("Propriétaire"),
        ADMIN("Administrateur");

        private final String displayName;

        UserRole(String displayName) {
            this.displayName = displayName;
        }

        public String getDisplayName() {
            return displayName;
        }
    }

    public enum Language {
        FRENCH("Français", "fr"),
        ENGLISH("English", "en"),
        GERMAN("Deutsch", "de"),
        POLISH("Polski", "pl"),
        UKRAINIAN("Українська", "uk");

        private final String displayName;
        private final String code;

        Language(String displayName, String code) {
            this.displayName = displayName;
            this.code = code;
        }

        public String getDisplayName() {
            return displayName;
        }

        public String getCode() {
            return code;
        }
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", email='" + email + '\'' +
                ", firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", city='" + city + '\'' +
                ", membershipStatus=" + membershipStatus +
                ", isActive=" + isActive +
                '}';
    }
} 