package com.ukraine.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;

/**
 * Entité représentant une photo d'un livre.
 * 
 * <p>Chaque livre doit avoir exactement 3 photos obligatoires :
 * - Couverture (avant)
 * - Dos du livre
 * - Intérieur (pour voir l'état)</p>
 * 
 * @author Équipe Lumières d'Ukraine
 * @version 1.0.0
 * @since 2024-01-01
 */
@Entity
@Table(name = "book_photos", indexes = {
    @Index(name = "idx_book_photo_book", columnList = "book_id"),
    @Index(name = "idx_book_photo_type", columnList = "type")
})
@EntityListeners(AuditingEntityListener.class)
public class BookPhoto {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Le nom du fichier est obligatoire")
    @Column(name = "file_name", nullable = false)
    private String fileName;

    @NotBlank(message = "Le chemin du fichier est obligatoire")
    @Column(name = "file_path", nullable = false)
    private String filePath;

    @Column(name = "file_size")
    private Long fileSize;

    @Column(name = "content_type")
    private String contentType;

    @NotNull(message = "Le type de photo est obligatoire")
    @Enumerated(EnumType.STRING)
    @Column(name = "type", nullable = false)
    private PhotoType type;

    @Column(name = "description")
    private String description;

    @NotNull(message = "Le livre est obligatoire")
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "book_id", nullable = false)
    private Book book;

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    // Constructeurs
    public BookPhoto() {
        // Constructeur par défaut requis par JPA
    }

    public BookPhoto(String fileName, String filePath, PhotoType type, Book book) {
        this.fileName = fileName;
        this.filePath = filePath;
        this.type = type;
        this.book = book;
    }

    // Getters et Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public String getFilePath() {
        return filePath;
    }

    public void setFilePath(String filePath) {
        this.filePath = filePath;
    }

    public Long getFileSize() {
        return fileSize;
    }

    public void setFileSize(Long fileSize) {
        this.fileSize = fileSize;
    }

    public String getContentType() {
        return contentType;
    }

    public void setContentType(String contentType) {
        this.contentType = contentType;
    }

    public PhotoType getType() {
        return type;
    }

    public void setType(PhotoType type) {
        this.type = type;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Book getBook() {
        return book;
    }

    public void setBook(Book book) {
        this.book = book;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    // Énumération des types de photos
    public enum PhotoType {
        COVER("Couverture", "Photo de la couverture du livre"),
        BACK("Dos", "Photo du dos du livre"),
        INTERIOR("Intérieur", "Photo de l'intérieur pour voir l'état");

        private final String displayName;
        private final String description;

        PhotoType(String displayName, String description) {
            this.displayName = displayName;
            this.description = description;
        }

        public String getDisplayName() {
            return displayName;
        }

        public String getDescription() {
            return description;
        }
    }

    @Override
    public String toString() {
        return "BookPhoto{" +
                "id=" + id +
                ", fileName='" + fileName + '\'' +
                ", type=" + type +
                ", bookId=" + (book != null ? book.getId() : null) +
                '}';
    }
} 