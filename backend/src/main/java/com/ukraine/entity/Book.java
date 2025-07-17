package com.ukraine.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * Entité représentant un livre dans l'application Lumières d'Ukraine.
 * 
 * <p>Cette entité gère toutes les informations d'un livre mis à disposition
 * par un propriétaire. Elle inclut les 3 photos obligatoires (couverture,
 * dos, intérieur), la géolocalisation, et les statistiques d'emprunt.</p>
 * 
 * @author Équipe Lumières d'Ukraine
 * @version 1.0.0
 * @since 2024-01-01
 */
@Entity
@Table(name = "books", indexes = {
    @Index(name = "idx_book_isbn", columnList = "isbn"),
    @Index(name = "idx_book_owner", columnList = "owner_id"),
    @Index(name = "idx_book_city", columnList = "city"),
    @Index(name = "idx_book_status", columnList = "status"),
    @Index(name = "idx_book_availability", columnList = "available_from")
})
@EntityListeners(AuditingEntityListener.class)
public class Book {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Le titre est obligatoire")
    @Size(max = 200, message = "Le titre ne peut pas dépasser 200 caractères")
    @Column(nullable = false)
    private String title;

    @NotBlank(message = "L'auteur est obligatoire")
    @Size(max = 100, message = "Le nom de l'auteur ne peut pas dépasser 100 caractères")
    @Column(nullable = false)
    private String author;

    @Size(max = 20, message = "L'ISBN ne peut pas dépasser 20 caractères")
    @Column(unique = true)
    private String isbn;

    @NotNull(message = "L'année de publication est obligatoire")
    @Column(name = "publication_year", nullable = false)
    private Integer publicationYear;

    @Enumerated(EnumType.STRING)
    @Column(name = "genre", nullable = false)
    private Genre genre;

    @Enumerated(EnumType.STRING)
    @Column(name = "target_age", nullable = false)
    private TargetAge targetAge;

    @Enumerated(EnumType.STRING)
    @Column(name = "language", nullable = false)
    private Language language;

    @Enumerated(EnumType.STRING)
    @Column(name = "condition", nullable = false)
    private BookCondition condition;

    @Size(max = 1000, message = "La description ne peut pas dépasser 1000 caractères")
    @Column(columnDefinition = "TEXT")
    private String description;

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

    @NotNull(message = "Le propriétaire est obligatoire")
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "owner_id", nullable = false)
    private User owner;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private BookStatus status = BookStatus.AVAILABLE;

    @Column(name = "available_from")
    private LocalDateTime availableFrom;

    @Column(name = "current_borrower_id")
    private Long currentBorrowerId;

    @Column(name = "total_borrows", nullable = false)
    private Integer totalBorrows = 0;

    @Column(name = "is_active", nullable = false)
    private Boolean isActive = true;

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    // Photos obligatoires (3 photos)
    @OneToMany(mappedBy = "book", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.EAGER)
    private List<BookPhoto> photos = new ArrayList<>();

    // Constructeurs
    public Book() {
        // Constructeur par défaut requis par JPA
    }

    public Book(String title, String author, Integer publicationYear, Genre genre, 
                TargetAge targetAge, Language language, BookCondition condition, String city, User owner) {
        this.title = title;
        this.author = author;
        this.publicationYear = publicationYear;
        this.genre = genre;
        this.targetAge = targetAge;
        this.language = language;
        this.condition = condition;
        this.city = city;
        this.owner = owner;
    }

    // Getters et Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public String getIsbn() {
        return isbn;
    }

    public void setIsbn(String isbn) {
        this.isbn = isbn;
    }

    public Integer getPublicationYear() {
        return publicationYear;
    }

    public void setPublicationYear(Integer publicationYear) {
        this.publicationYear = publicationYear;
    }

    public Genre getGenre() {
        return genre;
    }

    public void setGenre(Genre genre) {
        this.genre = genre;
    }

    public TargetAge getTargetAge() {
        return targetAge;
    }

    public void setTargetAge(TargetAge targetAge) {
        this.targetAge = targetAge;
    }

    public Language getLanguage() {
        return language;
    }

    public void setLanguage(Language language) {
        this.language = language;
    }

    public BookCondition getCondition() {
        return condition;
    }

    public void setCondition(BookCondition condition) {
        this.condition = condition;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
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

    public User getOwner() {
        return owner;
    }

    public void setOwner(User owner) {
        this.owner = owner;
    }

    public BookStatus getStatus() {
        return status;
    }

    public void setStatus(BookStatus status) {
        this.status = status;
    }

    public LocalDateTime getAvailableFrom() {
        return availableFrom;
    }

    public void setAvailableFrom(LocalDateTime availableFrom) {
        this.availableFrom = availableFrom;
    }

    public Long getCurrentBorrowerId() {
        return currentBorrowerId;
    }

    public void setCurrentBorrowerId(Long currentBorrowerId) {
        this.currentBorrowerId = currentBorrowerId;
    }

    public Integer getTotalBorrows() {
        return totalBorrows;
    }

    public void setTotalBorrows(Integer totalBorrows) {
        this.totalBorrows = totalBorrows;
    }

    public Boolean getIsActive() {
        return isActive;
    }

    public void setIsActive(Boolean isActive) {
        this.isActive = isActive;
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

    public List<BookPhoto> getPhotos() {
        return photos;
    }

    public void setPhotos(List<BookPhoto> photos) {
        this.photos = photos;
    }

    // Méthodes utilitaires
    public boolean isAvailable() {
        return status == BookStatus.AVAILABLE && 
               (availableFrom == null || availableFrom.isBefore(LocalDateTime.now()));
    }

    public boolean isCurrentlyBorrowed() {
        return currentBorrowerId != null;
    }

    public void incrementBorrows() {
        this.totalBorrows++;
    }

    public BookPhoto getCoverPhoto() {
        return photos.stream()
                .filter(photo -> photo.getType() == BookPhoto.PhotoType.COVER)
                .findFirst()
                .orElse(null);
    }

    public BookPhoto getBackPhoto() {
        return photos.stream()
                .filter(photo -> photo.getType() == BookPhoto.PhotoType.BACK)
                .findFirst()
                .orElse(null);
    }

    public BookPhoto getInteriorPhoto() {
        return photos.stream()
                .filter(photo -> photo.getType() == BookPhoto.PhotoType.INTERIOR)
                .findFirst()
                .orElse(null);
    }

    // Énumérations
    public enum Genre {
        ROMAN("Roman"),
        POESIE("Poésie"),
        HISTOIRE("Histoire"),
        CULTURE("Culture"),
        JEUNESSE("Jeunesse"),
        SCIENCE_FICTION("Science-fiction"),
        FANTASY("Fantasy"),
        POLICIER("Policier"),
        BIOGRAPHIE("Biographie"),
        ESSAI("Essai"),
        THEATRE("Théâtre"),
        AUTRE("Autre");

        private final String displayName;

        Genre(String displayName) {
            this.displayName = displayName;
        }

        public String getDisplayName() {
            return displayName;
        }
    }

    public enum TargetAge {
        ENFANT("Enfant", 0, 12),
        ADOLESCENT("Adolescent", 13, 17),
        ADULTE("Adulte", 18, 64),
        SENIOR("Senior", 65, 999);

        private final String displayName;
        private final int minAge;
        private final int maxAge;

        TargetAge(String displayName, int minAge, int maxAge) {
            this.displayName = displayName;
            this.minAge = minAge;
            this.maxAge = maxAge;
        }

        public String getDisplayName() {
            return displayName;
        }

        public int getMinAge() {
            return minAge;
        }

        public int getMaxAge() {
            return maxAge;
        }
    }

    public enum BookCondition {
        EXCELLENT("Excellent"),
        TRES_BON("Très bon"),
        BON("Bon"),
        MOYEN("Moyen"),
        MAUVAIS("Mauvais");

        private final String displayName;

        BookCondition(String displayName) {
            this.displayName = displayName;
        }

        public String getDisplayName() {
            return displayName;
        }
    }

    public enum BookStatus {
        AVAILABLE("Disponible"),
        BORROWED("Emprunté"),
        RESERVED("Réservé"),
        UNAVAILABLE("Indisponible");

        private final String displayName;

        BookStatus(String displayName) {
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
        UKRAINIAN("Українська", "uk"),
        RUSSIAN("Русский", "ru"),
        SPANISH("Español", "es"),
        ITALIAN("Italiano", "it");

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
        return "Book{" +
                "id=" + id +
                ", title='" + title + '\'' +
                ", author='" + author + '\'' +
                ", isbn='" + isbn + '\'' +
                ", city='" + city + '\'' +
                ", status=" + status +
                ", totalBorrows=" + totalBorrows +
                '}';
    }
} 