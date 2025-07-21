package com.ukraine.ragtime;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.stereotype.Service;

import java.util.*;

/**
 * Client Java pour l'API RagTime
 * Permet d'intégrer RagTime dans le backend Java
 */
@Service
public class RagTimeClient {
    
    private final String RAGTIME_API_BASE_URL = "http://localhost:5000/api";
    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;
    
    public RagTimeClient() {
        this.restTemplate = new RestTemplate();
        this.objectMapper = new ObjectMapper();
    }
    
    /**
     * Recherche de livres avec RagTime
     */
    public RagTimeSearchResponse searchBooks(String query, Map<String, String> filters, 
                                           int maxResults, boolean useAI, String userId) {
        try {
            String url = RAGTIME_API_BASE_URL + "/search";
            
            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("query", query);
            requestBody.put("filters", filters != null ? filters : new HashMap<>());
            requestBody.put("max_results", maxResults);
            requestBody.put("use_ai", useAI);
            requestBody.put("user_id", userId);
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<Map<String, Object>> request = new HttpEntity<>(requestBody, headers);
            
            ResponseEntity<String> response = restTemplate.postForEntity(url, request, String.class);
            
            if (response.getStatusCode() == HttpStatus.OK) {
                JsonNode jsonResponse = objectMapper.readTree(response.getBody());
                return parseSearchResponse(jsonResponse);
            } else {
                throw new RuntimeException("Erreur API RagTime: " + response.getStatusCode());
            }
            
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche RagTime", e);
        }
    }
    
    /**
     * Récupère la liste des livres
     */
    public List<Book> getBooks(int limit, int offset) {
        try {
            String url = RAGTIME_API_BASE_URL + "/books?limit=" + limit + "&offset=" + offset;
            
            ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
            
            if (response.getStatusCode() == HttpStatus.OK) {
                JsonNode jsonResponse = objectMapper.readTree(response.getBody());
                return parseBooksList(jsonResponse);
            } else {
                throw new RuntimeException("Erreur API RagTime: " + response.getStatusCode());
            }
            
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération des livres", e);
        }
    }
    
    /**
     * Récupère les détails d'un livre
     */
    public Book getBook(int bookId) {
        try {
            String url = RAGTIME_API_BASE_URL + "/books/" + bookId;
            
            ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
            
            if (response.getStatusCode() == HttpStatus.OK) {
                JsonNode jsonResponse = objectMapper.readTree(response.getBody());
                return parseBook(jsonResponse);
            } else if (response.getStatusCode() == HttpStatus.NOT_FOUND) {
                throw new RuntimeException("Livre non trouvé: " + bookId);
            } else {
                throw new RuntimeException("Erreur API RagTime: " + response.getStatusCode());
            }
            
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération du livre", e);
        }
    }
    
    /**
     * Récupère le résumé d'un livre
     */
    public String getBookSummary(int bookId, String style) {
        try {
            String url = RAGTIME_API_BASE_URL + "/summary/" + bookId + "?style=" + style;
            
            ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
            
            if (response.getStatusCode() == HttpStatus.OK) {
                JsonNode jsonResponse = objectMapper.readTree(response.getBody());
                return jsonResponse.get("summary").asText();
            } else {
                throw new RuntimeException("Erreur API RagTime: " + response.getStatusCode());
            }
            
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération du résumé", e);
        }
    }
    
    /**
     * Récupère les recommandations personnalisées
     */
    public List<Book> getRecommendations(String userId, Map<String, String> filters, int maxResults) {
        try {
            String url = RAGTIME_API_BASE_URL + "/recommendations";
            
            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("user_id", userId);
            requestBody.put("filters", filters != null ? filters : new HashMap<>());
            requestBody.put("max_results", maxResults);
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<Map<String, Object>> request = new HttpEntity<>(requestBody, headers);
            
            ResponseEntity<String> response = restTemplate.postForEntity(url, request, String.class);
            
            if (response.getStatusCode() == HttpStatus.OK) {
                JsonNode jsonResponse = objectMapper.readTree(response.getBody());
                return parseBooksList(jsonResponse.get("recommendations"));
            } else {
                throw new RuntimeException("Erreur API RagTime: " + response.getStatusCode());
            }
            
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération des recommandations", e);
        }
    }
    
    /**
     * Récupère les statistiques du système
     */
    public RagTimeStatistics getStatistics() {
        try {
            String url = RAGTIME_API_BASE_URL + "/statistics";
            
            ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
            
            if (response.getStatusCode() == HttpStatus.OK) {
                JsonNode jsonResponse = objectMapper.readTree(response.getBody());
                return parseStatistics(jsonResponse);
            } else {
                throw new RuntimeException("Erreur API RagTime: " + response.getStatusCode());
            }
            
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération des statistiques", e);
        }
    }
    
    /**
     * Vérifie la santé de l'API RagTime
     */
    public boolean isHealthy() {
        try {
            String url = RAGTIME_API_BASE_URL + "/health";
            
            ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
            
            return response.getStatusCode() == HttpStatus.OK;
            
        } catch (Exception e) {
            return false;
        }
    }
    
    /**
     * Récupère le statut de l'IA
     */
    public AIStatus getAIStatus() {
        try {
            String url = RAGTIME_API_BASE_URL + "/ai/status";
            
            ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
            
            if (response.getStatusCode() == HttpStatus.OK) {
                JsonNode jsonResponse = objectMapper.readTree(response.getBody());
                return parseAIStatus(jsonResponse);
            } else {
                throw new RuntimeException("Erreur API RagTime: " + response.getStatusCode());
            }
            
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération du statut IA", e);
        }
    }
    
    /**
     * Configure l'IA
     */
    public boolean configureAI(String mode) {
        try {
            String url = RAGTIME_API_BASE_URL + "/ai/configure";
            
            Map<String, String> requestBody = new HashMap<>();
            requestBody.put("mode", mode);
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<Map<String, String>> request = new HttpEntity<>(requestBody, headers);
            
            ResponseEntity<String> response = restTemplate.postForEntity(url, request, String.class);
            
            return response.getStatusCode() == HttpStatus.OK;
            
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la configuration IA", e);
        }
    }
    
    // Méthodes de parsing
    
    private RagTimeSearchResponse parseSearchResponse(JsonNode jsonResponse) {
        RagTimeSearchResponse response = new RagTimeSearchResponse();
        
        response.setSuccess(jsonResponse.get("success").asBoolean());
        response.setQuery(jsonResponse.get("query").asText());
        response.setResponse(jsonResponse.get("response").asText());
        
        if (jsonResponse.has("rag_response")) {
            response.setRagResponse(jsonResponse.get("rag_response").asText());
        }
        
        if (jsonResponse.has("ai_response")) {
            response.setAiResponse(jsonResponse.get("ai_response").asText());
        }
        
        if (jsonResponse.has("books")) {
            response.setBooks(parseBooksList(jsonResponse.get("books")));
        }
        
        if (jsonResponse.has("timing")) {
            JsonNode timing = jsonResponse.get("timing");
            response.setRagTime(timing.get("rag_time").asDouble());
            response.setAiTime(timing.get("ai_time").asDouble());
            response.setTotalTime(timing.get("total_time").asDouble());
        }
        
        response.setAiUsed(jsonResponse.get("ai_used").asBoolean());
        
        if (jsonResponse.has("ai_model")) {
            response.setAiModel(jsonResponse.get("ai_model").asText());
        }
        
        return response;
    }
    
    private List<Book> parseBooksList(JsonNode booksNode) {
        List<Book> books = new ArrayList<>();
        
        if (booksNode.isArray()) {
            for (JsonNode bookNode : booksNode) {
                books.add(parseBook(bookNode));
            }
        }
        
        return books;
    }
    
    private Book parseBook(JsonNode bookNode) {
        Book book = new Book();
        
        if (bookNode.has("id")) {
            book.setId(bookNode.get("id").asInt());
        }
        
        if (bookNode.has("title")) {
            book.setTitle(bookNode.get("title").asText());
        }
        
        if (bookNode.has("author")) {
            book.setAuthor(bookNode.get("author").asText());
        }
        
        if (bookNode.has("genre")) {
            book.setGenre(bookNode.get("genre").asText());
        }
        
        if (bookNode.has("description")) {
            book.setDescription(bookNode.get("description").asText());
        }
        
        if (bookNode.has("language")) {
            book.setLanguage(bookNode.get("language").asText());
        }
        
        if (bookNode.has("city")) {
            book.setCity(bookNode.get("city").asText());
        }
        
        if (bookNode.has("status")) {
            book.setStatus(bookNode.get("status").asText());
        }
        
        if (bookNode.has("score")) {
            book.setScore(bookNode.get("score").asDouble());
        }
        
        if (bookNode.has("themes")) {
            List<String> themes = new ArrayList<>();
            JsonNode themesNode = bookNode.get("themes");
            if (themesNode.isArray()) {
                for (JsonNode themeNode : themesNode) {
                    themes.add(themeNode.asText());
                }
            }
            book.setThemes(themes);
        }
        
        if (bookNode.has("summary")) {
            book.setSummary(bookNode.get("summary").asText());
        }
        
        return book;
    }
    
    private RagTimeStatistics parseStatistics(JsonNode statsNode) {
        RagTimeStatistics stats = new RagTimeStatistics();
        
        stats.setTotalBooks(statsNode.get("total_books").asInt());
        stats.setTotalSummaries(statsNode.get("total_summaries").asInt());
        stats.setAiEnabled(statsNode.get("ai_enabled").asBoolean());
        
        if (statsNode.has("ai_models")) {
            List<String> aiModels = new ArrayList<>();
            JsonNode aiModelsNode = statsNode.get("ai_models");
            if (aiModelsNode.isArray()) {
                for (JsonNode modelNode : aiModelsNode) {
                    aiModels.add(modelNode.asText());
                }
            }
            stats.setAiModels(aiModels);
        }
        
        return stats;
    }
    
    private AIStatus parseAIStatus(JsonNode statusNode) {
        AIStatus status = new AIStatus();
        
        status.setEnabled(statusNode.get("enabled").asBoolean());
        status.setMode(statusNode.get("mode").asText());
        
        if (statusNode.has("primary_model")) {
            status.setPrimaryModel(statusNode.get("primary_model").asText());
        }
        
        if (statusNode.has("quality_model")) {
            status.setQualityModel(statusNode.get("quality_model").asText());
        }
        
        if (statusNode.has("available_models")) {
            List<String> availableModels = new ArrayList<>();
            JsonNode modelsNode = statusNode.get("available_models");
            if (modelsNode.isArray()) {
                for (JsonNode modelNode : modelsNode) {
                    availableModels.add(modelNode.asText());
                }
            }
            status.setAvailableModels(availableModels);
        }
        
        return status;
    }
    
    // Classes de données
    
    public static class RagTimeSearchResponse {
        private boolean success;
        private String query;
        private String response;
        private String ragResponse;
        private String aiResponse;
        private List<Book> books;
        private double ragTime;
        private double aiTime;
        private double totalTime;
        private boolean aiUsed;
        private String aiModel;
        
        // Getters et setters
        public boolean isSuccess() { return success; }
        public void setSuccess(boolean success) { this.success = success; }
        
        public String getQuery() { return query; }
        public void setQuery(String query) { this.query = query; }
        
        public String getResponse() { return response; }
        public void setResponse(String response) { this.response = response; }
        
        public String getRagResponse() { return ragResponse; }
        public void setRagResponse(String ragResponse) { this.ragResponse = ragResponse; }
        
        public String getAiResponse() { return aiResponse; }
        public void setAiResponse(String aiResponse) { this.aiResponse = aiResponse; }
        
        public List<Book> getBooks() { return books; }
        public void setBooks(List<Book> books) { this.books = books; }
        
        public double getRagTime() { return ragTime; }
        public void setRagTime(double ragTime) { this.ragTime = ragTime; }
        
        public double getAiTime() { return aiTime; }
        public void setAiTime(double aiTime) { this.aiTime = aiTime; }
        
        public double getTotalTime() { return totalTime; }
        public void setTotalTime(double totalTime) { this.totalTime = totalTime; }
        
        public boolean isAiUsed() { return aiUsed; }
        public void setAiUsed(boolean aiUsed) { this.aiUsed = aiUsed; }
        
        public String getAiModel() { return aiModel; }
        public void setAiModel(String aiModel) { this.aiModel = aiModel; }
    }
    
    public static class Book {
        private int id;
        private String title;
        private String author;
        private String genre;
        private String description;
        private String language;
        private String city;
        private String status;
        private double score;
        private List<String> themes;
        private String summary;
        
        // Getters et setters
        public int getId() { return id; }
        public void setId(int id) { this.id = id; }
        
        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }
        
        public String getAuthor() { return author; }
        public void setAuthor(String author) { this.author = author; }
        
        public String getGenre() { return genre; }
        public void setGenre(String genre) { this.genre = genre; }
        
        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }
        
        public String getLanguage() { return language; }
        public void setLanguage(String language) { this.language = language; }
        
        public String getCity() { return city; }
        public void setCity(String city) { this.city = city; }
        
        public String getStatus() { return status; }
        public void setStatus(String status) { this.status = status; }
        
        public double getScore() { return score; }
        public void setScore(double score) { this.score = score; }
        
        public List<String> getThemes() { return themes; }
        public void setThemes(List<String> themes) { this.themes = themes; }
        
        public String getSummary() { return summary; }
        public void setSummary(String summary) { this.summary = summary; }
    }
    
    public static class RagTimeStatistics {
        private int totalBooks;
        private int totalSummaries;
        private boolean aiEnabled;
        private List<String> aiModels;
        
        // Getters et setters
        public int getTotalBooks() { return totalBooks; }
        public void setTotalBooks(int totalBooks) { this.totalBooks = totalBooks; }
        
        public int getTotalSummaries() { return totalSummaries; }
        public void setTotalSummaries(int totalSummaries) { this.totalSummaries = totalSummaries; }
        
        public boolean isAiEnabled() { return aiEnabled; }
        public void setAiEnabled(boolean aiEnabled) { this.aiEnabled = aiEnabled; }
        
        public List<String> getAiModels() { return aiModels; }
        public void setAiModels(List<String> aiModels) { this.aiModels = aiModels; }
    }
    
    public static class AIStatus {
        private boolean enabled;
        private String mode;
        private String primaryModel;
        private String qualityModel;
        private List<String> availableModels;
        
        // Getters et setters
        public boolean isEnabled() { return enabled; }
        public void setEnabled(boolean enabled) { this.enabled = enabled; }
        
        public String getMode() { return mode; }
        public void setMode(String mode) { this.mode = mode; }
        
        public String getPrimaryModel() { return primaryModel; }
        public void setPrimaryModel(String primaryModel) { this.primaryModel = primaryModel; }
        
        public String getQualityModel() { return qualityModel; }
        public void setQualityModel(String qualityModel) { this.qualityModel = qualityModel; }
        
        public List<String> getAvailableModels() { return availableModels; }
        public void setAvailableModels(List<String> availableModels) { this.availableModels = availableModels; }
    }
} 