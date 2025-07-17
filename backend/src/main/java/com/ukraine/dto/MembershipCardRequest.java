package com.ukraine.dto;

import java.util.List;

/**
 * DTO pour les requêtes de génération de cartes d'adhésion
 */
public class MembershipCardRequest {
    
    private MemberData memberData;
    private EmailData emailData;
    private CardOptions cardOptions;
    
    // Constructeurs
    public MembershipCardRequest() {}
    
    public MembershipCardRequest(MemberData memberData) {
        this.memberData = memberData;
    }
    
    // Getters et Setters
    public MemberData getMemberData() {
        return memberData;
    }
    
    public void setMemberData(MemberData memberData) {
        this.memberData = memberData;
    }
    
    public EmailData getEmailData() {
        return emailData;
    }
    
    public void setEmailData(EmailData emailData) {
        this.emailData = emailData;
    }
    
    public CardOptions getCardOptions() {
        return cardOptions;
    }
    
    public void setCardOptions(CardOptions cardOptions) {
        this.cardOptions = cardOptions;
    }
    
    /**
     * DTO pour les données du membre
     */
    public static class MemberData {
        private String name;
        private String firstName;
        private String memberNumber;
        private String joinDate;
        private String birthDate;
        private String address;
        private String postalCode;
        private String city;
        private String phone;
        private String email;
        
        // Constructeurs
        public MemberData() {}
        
        // Getters et Setters
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        
        public String getFirstName() { return firstName; }
        public void setFirstName(String firstName) { this.firstName = firstName; }
        
        public String getMemberNumber() { return memberNumber; }
        public void setMemberNumber(String memberNumber) { this.memberNumber = memberNumber; }
        
        public String getJoinDate() { return joinDate; }
        public void setJoinDate(String joinDate) { this.joinDate = joinDate; }
        
        public String getBirthDate() { return birthDate; }
        public void setBirthDate(String birthDate) { this.birthDate = birthDate; }
        
        public String getAddress() { return address; }
        public void setAddress(String address) { this.address = address; }
        
        public String getPostalCode() { return postalCode; }
        public void setPostalCode(String postalCode) { this.postalCode = postalCode; }
        
        public String getCity() { return city; }
        public void setCity(String city) { this.city = city; }
        
        public String getPhone() { return phone; }
        public void setPhone(String phone) { this.phone = phone; }
        
        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }
    }
    
    /**
     * DTO pour les données d'email
     */
    public static class EmailData {
        private String to;
        private String subject;
        private String message;
        private List<String> attachments;
        
        // Constructeurs
        public EmailData() {}
        
        // Getters et Setters
        public String getTo() { return to; }
        public void setTo(String to) { this.to = to; }
        
        public String getSubject() { return subject; }
        public void setSubject(String subject) { this.subject = subject; }
        
        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
        
        public List<String> getAttachments() { return attachments; }
        public void setAttachments(List<String> attachments) { this.attachments = attachments; }
    }
    
    /**
     * DTO pour les options de la carte
     */
    public static class CardOptions {
        private String format; // "pdf", "png", "jpg"
        private String quality; // "high", "medium", "low"
        private boolean includeBarcode;
        private String cardTemplate; // "default", "premium", "standard"
        
        // Constructeurs
        public CardOptions() {
            this.format = "pdf";
            this.quality = "high";
            this.includeBarcode = true;
            this.cardTemplate = "default";
        }
        
        // Getters et Setters
        public String getFormat() { return format; }
        public void setFormat(String format) { this.format = format; }
        
        public String getQuality() { return quality; }
        public void setQuality(String quality) { this.quality = quality; }
        
        public boolean isIncludeBarcode() { return includeBarcode; }
        public void setIncludeBarcode(boolean includeBarcode) { this.includeBarcode = includeBarcode; }
        
        public String getCardTemplate() { return cardTemplate; }
        public void setCardTemplate(String cardTemplate) { this.cardTemplate = cardTemplate; }
    }
} 