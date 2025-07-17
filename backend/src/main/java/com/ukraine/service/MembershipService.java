package com.ukraine.service;

import com.ukraine.dto.MembershipCardRequest;
import com.ukraine.dto.MembershipCardResponse;
import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Map;
import java.util.HashMap;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Service pour la gestion des cartes d'adhésion
 * Gère la génération, le stockage et la validation des cartes
 */
@Service
public class MembershipService {

    @Value("${app.membership.cards.storage-path:./storage/cards}")
    private String storagePath;

    @Value("${app.membership.cards.base-url:http://localhost:8080/api/membership/cards}")
    private String baseUrl;

    private final AtomicInteger memberCounter = new AtomicInteger(1);

    /**
     * Génère une carte d'adhésion complète
     * @param request Données du membre et options
     * @return Réponse avec les URLs des images générées
     */
    public MembershipCardResponse generateMembershipCard(MembershipCardRequest request) {
        try {
            // Valider les données du membre
            Map<String, Object> validation = validateMemberData(request.getMemberData());
            if (!(Boolean) validation.get("valid")) {
                return MembershipCardResponse.error((String) validation.get("message"));
            }

            // Créer le dossier de stockage si nécessaire
            Path storageDir = Paths.get(storagePath);
            if (!Files.exists(storageDir)) {
                Files.createDirectories(storageDir);
            }

            // Générer les noms de fichiers
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            String memberNumber = request.getMemberData().getMemberNumber();
            String frontFileName = String.format("card_front_%s_%s.png", memberNumber, timestamp);
            String backFileName = String.format("card_back_%s_%s.png", memberNumber, timestamp);

            // Générer le recto de la carte
            String frontImageUrl = generateCardFront(request.getMemberData(), frontFileName);
            
            // Générer le verso de la carte
            String backImageUrl = generateCardBack(request.getMemberData(), backFileName);

            return MembershipCardResponse.success(memberNumber, frontImageUrl, backImageUrl);

        } catch (Exception e) {
            return MembershipCardResponse.error("Erreur lors de la génération de la carte: " + e.getMessage());
        }
    }

    /**
     * Génère le recto de la carte d'adhésion
     * @param memberData Données du membre
     * @param fileName Nom du fichier à générer
     * @return URL de l'image générée
     */
    private String generateCardFront(MembershipCardRequest.MemberData memberData, String fileName) throws IOException {
        // Ici, vous pouvez utiliser une bibliothèque comme iText, Apache PDFBox, ou une API externe
        // Pour l'instant, nous simulons la génération
        
        Path filePath = Paths.get(storagePath, fileName);
        
        // Créer une image simple (remplacer par votre logique de génération)
        createPlaceholderImage(filePath, "Recto - " + memberData.getFirstName() + " " + memberData.getName());
        
        return baseUrl + "/" + fileName;
    }

    /**
     * Génère le verso de la carte d'adhésion
     * @param memberData Données du membre
     * @param fileName Nom du fichier à générer
     * @return URL de l'image générée
     */
    private String generateCardBack(MembershipCardRequest.MemberData memberData, String fileName) throws IOException {
        Path filePath = Paths.get(storagePath, fileName);
        
        // Créer une image simple (remplacer par votre logique de génération)
        createPlaceholderImage(filePath, "Verso - " + memberData.getMemberNumber());
        
        return baseUrl + "/" + fileName;
    }

    /**
     * Crée une image placeholder (à remplacer par votre logique de génération)
     * @param filePath Chemin du fichier
     * @param text Texte à afficher
     */
    private void createPlaceholderImage(Path filePath, String text) throws IOException {
        // Pour l'instant, nous créons un fichier texte simple
        // En production, utilisez une bibliothèque comme iText, Apache PDFBox, ou une API externe
        String content = String.format("""
            Carte d'Adhésion - Les Lumières d'Ukraine
            %s
            Généré le: %s
            """, text, LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm")));
        
        Files.write(filePath, content.getBytes());
    }

    /**
     * Génère un PDF avec les deux faces de la carte
     * @param request Données du membre
     * @return Bytes du PDF généré
     */
    public byte[] generateMembershipCardPDF(MembershipCardRequest request) throws IOException {
        // Ici, vous pouvez utiliser iText ou Apache PDFBox pour générer un vrai PDF
        // Pour l'instant, nous retournons un PDF simple
        
        String pdfContent = String.format("""
            %PDF-1.4
            1 0 obj
            <<
            /Type /Catalog
            /Pages 2 0 R
            >>
            endobj
            
            2 0 obj
            <<
            /Type /Pages
            /Kids [3 0 R 4 0 R]
            /Count 2
            >>
            endobj
            
            3 0 obj
            <<
            /Type /Page
            /Parent 2 0 R
            /MediaBox [0 0 595 842]
            /Contents 5 0 R
            >>
            endobj
            
            4 0 obj
            <<
            /Type /Page
            /Parent 2 0 R
            /MediaBox [0 0 595 842]
            /Contents 6 0 R
            >>
            endobj
            
            5 0 obj
            <<
            /Length 100
            >>
            stream
            BT
            /F1 12 Tf
            50 750 Td
            (Carte d'Adhésion - Recto) Tj
            50 720 Td
            (Membre: %s %s) Tj
            50 690 Td
            (Numéro: %s) Tj
            ET
            endstream
            endobj
            
            6 0 obj
            <<
            /Length 100
            >>
            stream
            BT
            /F1 12 Tf
            50 750 Td
            (Carte d'Adhésion - Verso) Tj
            50 720 Td
            (Détails du membre) Tj
            ET
            endstream
            endobj
            
            xref
            0 7
            0000000000 65535 f 
            0000000009 00000 n 
            0000000058 00000 n 
            0000000115 00000 n 
            0000000172 00000 n 
            0000000229 00000 n 
            0000000365 00000 n 
            trailer
            <<
            /Size 7
            /Root 1 0 R
            >>
            startxref
            472
            %%EOF
            """, 
            request.getMemberData().getFirstName(),
            request.getMemberData().getName(),
            request.getMemberData().getMemberNumber()
        );
        
        return pdfContent.getBytes();
    }

    /**
     * Valide les données d'un membre
     * @param memberData Données à valider
     * @return Résultat de la validation
     */
    public Map<String, Object> validateMemberData(MembershipCardRequest.MemberData memberData) {
        Map<String, Object> result = new HashMap<>();
        
        if (memberData == null) {
            result.put("valid", false);
            result.put("message", "Les données du membre sont requises");
            return result;
        }
        
        if (memberData.getName() == null || memberData.getName().trim().isEmpty()) {
            result.put("valid", false);
            result.put("message", "Le nom est requis");
            return result;
        }
        
        if (memberData.getFirstName() == null || memberData.getFirstName().trim().isEmpty()) {
            result.put("valid", false);
            result.put("message", "Le prénom est requis");
            return result;
        }
        
        if (memberData.getMemberNumber() == null || memberData.getMemberNumber().trim().isEmpty()) {
            result.put("valid", false);
            result.put("message", "Le numéro d'adhésion est requis");
            return result;
        }
        
        if (memberData.getEmail() == null || memberData.getEmail().trim().isEmpty()) {
            result.put("valid", false);
            result.put("message", "L'email est requis");
            return result;
        }
        
        // Validation basique de l'email
        if (!memberData.getEmail().contains("@")) {
            result.put("valid", false);
            result.put("message", "L'email n'est pas valide");
            return result;
        }
        
        result.put("valid", true);
        result.put("message", "Données valides");
        return result;
    }

    /**
     * Génère un numéro d'adhésion unique
     * @return Numéro d'adhésion unique
     */
    public String generateUniqueMembershipNumber() {
        int year = LocalDateTime.now().getYear();
        int counter = memberCounter.getAndIncrement();
        return String.format("%d-%03d", year, counter);
    }

    /**
     * Récupère une carte d'adhésion par son nom de fichier
     * @param fileName Nom du fichier
     * @return Resource du fichier
     * @throws IOException Si le fichier n'existe pas
     */
    public Resource getCardFile(String fileName) throws IOException {
        Path filePath = Paths.get(storagePath, fileName);
        if (!Files.exists(filePath)) {
            throw new IOException("Fichier non trouvé: " + fileName);
        }
        return new UrlResource(filePath.toUri());
    }
} 