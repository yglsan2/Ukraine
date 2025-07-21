package com.ukraine.controller;

import com.ukraine.ragtime.RagTimeClient;
import com.ukraine.ragtime.RagTimeClient.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Contrôleur pour l'intégration RagTime
 * Expose les fonctionnalités RagTime via des endpoints REST
 */
@RestController
@RequestMapping("/api/ragtime")
@CrossOrigin(origins = "*")
public class RagTimeController {
    
    @Autowired
    private RagTimeClient ragTimeClient;
    
    /**
     * Recherche de livres avec RagTime
     */
    @PostMapping("/search")
    public ResponseEntity<?> searchBooks(@RequestBody Map<String, Object> request) {
        try {
            String query = (String) request.get("query");
            @SuppressWarnings("unchecked")
            Map<String, String> filters = (Map<String, String>) request.get("filters");
            Integer maxResults = (Integer) request.getOrDefault("maxResults", 10);
            Boolean useAI = (Boolean) request.getOrDefault("useAI", true);
            String userId = (String) request.get("userId");
            
            if (query == null || query.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(Map.of("error", "Query requise"));
            }
            
            RagTimeSearchResponse response = ragTimeClient.searchBooks(
                query, filters, maxResults, useAI, userId
            );
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Liste des livres
     */
    @GetMapping("/books")
    public ResponseEntity<?> getBooks(
            @RequestParam(defaultValue = "50") int limit,
            @RequestParam(defaultValue = "0") int offset) {
        try {
            List<Book> books = ragTimeClient.getBooks(limit, offset);
            
            Map<String, Object> response = new HashMap<>();
            response.put("books", books);
            response.put("total", books.size());
            response.put("limit", limit);
            response.put("offset", offset);
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Détails d'un livre
     */
    @GetMapping("/books/{bookId}")
    public ResponseEntity<?> getBook(@PathVariable int bookId) {
        try {
            Book book = ragTimeClient.getBook(bookId);
            return ResponseEntity.ok(book);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Résumé d'un livre
     */
    @GetMapping("/books/{bookId}/summary")
    public ResponseEntity<?> getBookSummary(
            @PathVariable int bookId,
            @RequestParam(defaultValue = "standard") String style) {
        try {
            String summary = ragTimeClient.getBookSummary(bookId, style);
            
            Map<String, Object> response = new HashMap<>();
            response.put("bookId", bookId);
            response.put("style", style);
            response.put("summary", summary);
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Recommandations personnalisées
     */
    @PostMapping("/recommendations")
    public ResponseEntity<?> getRecommendations(@RequestBody Map<String, Object> request) {
        try {
            String userId = (String) request.get("userId");
            @SuppressWarnings("unchecked")
            Map<String, String> filters = (Map<String, String>) request.get("filters");
            Integer maxResults = (Integer) request.getOrDefault("maxResults", 10);
            
            if (userId == null || userId.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(Map.of("error", "userId requis"));
            }
            
            List<Book> recommendations = ragTimeClient.getRecommendations(userId, filters, maxResults);
            
            Map<String, Object> response = new HashMap<>();
            response.put("recommendations", recommendations);
            response.put("userId", userId);
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Statistiques du système
     */
    @GetMapping("/statistics")
    public ResponseEntity<?> getStatistics() {
        try {
            RagTimeStatistics stats = ragTimeClient.getStatistics();
            return ResponseEntity.ok(stats);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Vérification de santé
     */
    @GetMapping("/health")
    public ResponseEntity<?> healthCheck() {
        try {
            boolean isHealthy = ragTimeClient.isHealthy();
            
            Map<String, Object> response = new HashMap<>();
            response.put("status", isHealthy ? "healthy" : "unhealthy");
            response.put("service", "RagTime Integration");
            response.put("timestamp", System.currentTimeMillis());
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Statut de l'IA
     */
    @GetMapping("/ai/status")
    public ResponseEntity<?> getAIStatus() {
        try {
            AIStatus status = ragTimeClient.getAIStatus();
            return ResponseEntity.ok(status);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Configuration de l'IA
     */
    @PostMapping("/ai/configure")
    public ResponseEntity<?> configureAI(@RequestBody Map<String, String> request) {
        try {
            String mode = request.get("mode");
            
            if (mode == null || (!mode.equals("fast") && !mode.equals("quality"))) {
                return ResponseEntity.badRequest().body(Map.of("error", "Mode invalide. Utilisez 'fast' ou 'quality'"));
            }
            
            boolean success = ragTimeClient.configureAI(mode);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", success);
            response.put("mode", mode);
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Recherche simple (sans IA)
     */
    @PostMapping("/search/simple")
    public ResponseEntity<?> simpleSearch(@RequestBody Map<String, Object> request) {
        try {
            String query = (String) request.get("query");
            @SuppressWarnings("unchecked")
            Map<String, String> filters = (Map<String, String>) request.get("filters");
            Integer maxResults = (Integer) request.getOrDefault("maxResults", 10);
            
            if (query == null || query.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(Map.of("error", "Query requise"));
            }
            
            // Recherche sans IA
            RagTimeSearchResponse response = ragTimeClient.searchBooks(
                query, filters, maxResults, false, null
            );
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Recherche avec IA (mode rapide)
     */
    @PostMapping("/search/fast")
    public ResponseEntity<?> fastSearch(@RequestBody Map<String, Object> request) {
        try {
            String query = (String) request.get("query");
            @SuppressWarnings("unchecked")
            Map<String, String> filters = (Map<String, String>) request.get("filters");
            Integer maxResults = (Integer) request.getOrDefault("maxResults", 10);
            String userId = (String) request.get("userId");
            
            if (query == null || query.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(Map.of("error", "Query requise"));
            }
            
            // Configuration mode rapide
            ragTimeClient.configureAI("fast");
            
            // Recherche avec IA rapide
            RagTimeSearchResponse response = ragTimeClient.searchBooks(
                query, filters, maxResults, true, userId
            );
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Recherche avec IA (mode qualité)
     */
    @PostMapping("/search/quality")
    public ResponseEntity<?> qualitySearch(@RequestBody Map<String, Object> request) {
        try {
            String query = (String) request.get("query");
            @SuppressWarnings("unchecked")
            Map<String, String> filters = (Map<String, String>) request.get("filters");
            Integer maxResults = (Integer) request.getOrDefault("maxResults", 10);
            String userId = (String) request.get("userId");
            
            if (query == null || query.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(Map.of("error", "Query requise"));
            }
            
            // Configuration mode qualité
            ragTimeClient.configureAI("quality");
            
            // Recherche avec IA qualité
            RagTimeSearchResponse response = ragTimeClient.searchBooks(
                query, filters, maxResults, true, userId
            );
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Recherche par thème
     */
    @GetMapping("/search/theme/{theme}")
    public ResponseEntity<?> searchByTheme(
            @PathVariable String theme,
            @RequestParam(defaultValue = "10") int maxResults) {
        try {
            Map<String, String> filters = new HashMap<>();
            // Le filtre par thème sera appliqué côté Python
            
            RagTimeSearchResponse response = ragTimeClient.searchBooks(
                "thème: " + theme, filters, maxResults, false, null
            );
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Recherche par genre
     */
    @GetMapping("/search/genre/{genre}")
    public ResponseEntity<?> searchByGenre(
            @PathVariable String genre,
            @RequestParam(defaultValue = "10") int maxResults) {
        try {
            Map<String, String> filters = new HashMap<>();
            filters.put("genre", genre);
            
            RagTimeSearchResponse response = ragTimeClient.searchBooks(
                "genre: " + genre, filters, maxResults, false, null
            );
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Recherche par auteur
     */
    @GetMapping("/search/author/{author}")
    public ResponseEntity<?> searchByAuthor(
            @PathVariable String author,
            @RequestParam(defaultValue = "10") int maxResults) {
        try {
            RagTimeSearchResponse response = ragTimeClient.searchBooks(
                "auteur: " + author, null, maxResults, false, null
            );
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
} 