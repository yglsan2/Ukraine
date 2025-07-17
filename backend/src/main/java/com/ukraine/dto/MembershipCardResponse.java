package com.ukraine.dto;

import java.time.LocalDateTime;

/**
 * DTO pour les réponses de génération de cartes d'adhésion
 */
public class MembershipCardResponse {
    
    private String memberNumber;
    private String frontImageUrl;
    private String backImageUrl;
    private String pdfUrl;
    private LocalDateTime generatedAt;
    private String status;
    private String message;
    
    // Constructeurs
    public MembershipCardResponse() {
        this.generatedAt = LocalDateTime.now();
        this.status = "success";
    }
    
    public MembershipCardResponse(String memberNumber, String frontImageUrl, String backImageUrl) {
        this();
        this.memberNumber = memberNumber;
        this.frontImageUrl = frontImageUrl;
        this.backImageUrl = backImageUrl;
    }
    
    // Getters et Setters
    public String getMemberNumber() {
        return memberNumber;
    }
    
    public void setMemberNumber(String memberNumber) {
        this.memberNumber = memberNumber;
    }
    
    public String getFrontImageUrl() {
        return frontImageUrl;
    }
    
    public void setFrontImageUrl(String frontImageUrl) {
        this.frontImageUrl = frontImageUrl;
    }
    
    public String getBackImageUrl() {
        return backImageUrl;
    }
    
    public void setBackImageUrl(String backImageUrl) {
        this.backImageUrl = backImageUrl;
    }
    
    public String getPdfUrl() {
        return pdfUrl;
    }
    
    public void setPdfUrl(String pdfUrl) {
        this.pdfUrl = pdfUrl;
    }
    
    public LocalDateTime getGeneratedAt() {
        return generatedAt;
    }
    
    public void setGeneratedAt(LocalDateTime generatedAt) {
        this.generatedAt = generatedAt;
    }
    
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
    
    public String getMessage() {
        return message;
    }
    
    public void setMessage(String message) {
        this.message = message;
    }
    
    /**
     * Méthode utilitaire pour créer une réponse d'erreur
     */
    public static MembershipCardResponse error(String message) {
        MembershipCardResponse response = new MembershipCardResponse();
        response.setStatus("error");
        response.setMessage(message);
        return response;
    }
    
    /**
     * Méthode utilitaire pour créer une réponse de succès
     */
    public static MembershipCardResponse success(String memberNumber, String frontImageUrl, String backImageUrl) {
        return new MembershipCardResponse(memberNumber, frontImageUrl, backImageUrl);
    }
} 