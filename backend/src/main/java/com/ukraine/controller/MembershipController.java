package com.ukraine.controller;

import com.ukraine.dto.MembershipCardRequest;
import com.ukraine.dto.MembershipCardResponse;
import com.ukraine.service.MembershipService;
import com.ukraine.service.EmailService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.core.io.Resource;

import java.util.Map;
import java.io.IOException;

/**
 * Contrôleur pour la gestion des cartes d'adhésion
 * Gère la génération, le téléchargement et l'envoi des cartes d'adhésion
 */
@RestController
@RequestMapping("/api/membership")
@CrossOrigin(origins = "*")
public class MembershipController {

    @Autowired
    private MembershipService membershipService;

    @Autowired
    private EmailService emailService;

    /**
     * Génère une carte d'adhésion pour un membre
     * @param request Données du membre et paramètres de la carte
     * @return Réponse avec les URLs des images générées
     */
    @PostMapping("/generate-card")
    public ResponseEntity<MembershipCardResponse> generateMembershipCard(
            @RequestBody MembershipCardRequest request) {
        try {
            MembershipCardResponse response = membershipService.generateMembershipCard(request);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    /**
     * Envoie une carte d'adhésion par email
     * @param request Données de l'email et de la carte
     * @return Confirmation de l'envoi
     */
    @PostMapping("/send-card")
    public ResponseEntity<Map<String, String>> sendMembershipCard(
            @RequestBody MembershipCardRequest request) {
        try {
            // Générer la carte
            MembershipCardResponse cardResponse = membershipService.generateMembershipCard(request);
            
            // Envoyer par email
            emailService.sendMembershipCard(
                request.getEmailData().getTo(),
                request.getEmailData().getSubject(),
                request.getEmailData().getMessage(),
                cardResponse.getFrontImageUrl(),
                cardResponse.getBackImageUrl(),
                request.getMemberData()
            );
            
            return ResponseEntity.ok(Map.of(
                "message", "Carte d'adhésion envoyée avec succès",
                "memberNumber", request.getMemberData().getMemberNumber()
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "error", "Erreur lors de l'envoi de la carte: " + e.getMessage()
            ));
        }
    }

    /**
     * Télécharge une carte d'adhésion au format PDF
     * @param request Données du membre
     * @return Fichier PDF à télécharger
     */
    @PostMapping("/download-pdf")
    public ResponseEntity<byte[]> downloadMembershipCardPDF(
            @RequestBody MembershipCardRequest request) {
        try {
            byte[] pdfBytes = membershipService.generateMembershipCardPDF(request);
            return ResponseEntity.ok()
                .header("Content-Disposition", 
                    "attachment; filename=carte-adhesion-" + request.getMemberData().getMemberNumber() + ".pdf")
                .header("Content-Type", "application/pdf")
                .body(pdfBytes);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    /**
     * Valide les données d'un membre avant génération de carte
     * @param request Données du membre à valider
     * @return Résultat de la validation
     */
    @PostMapping("/validate-member")
    public ResponseEntity<Map<String, Object>> validateMemberData(
            @RequestBody MembershipCardRequest request) {
        try {
            Map<String, Object> validationResult = membershipService.validateMemberData(request.getMemberData());
            return ResponseEntity.ok(validationResult);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "valid", false,
                "error", e.getMessage()
            ));
        }
    }

    /**
     * Génère un numéro d'adhésion unique
     * @return Nouveau numéro d'adhésion
     */
    @GetMapping("/generate-number")
    public ResponseEntity<Map<String, String>> generateMembershipNumber() {
        try {
            String memberNumber = membershipService.generateUniqueMembershipNumber();
            return ResponseEntity.ok(Map.of("memberNumber", memberNumber));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "error", "Erreur lors de la génération du numéro: " + e.getMessage()
            ));
        }
    }

    /**
     * Sert un fichier de carte d'adhésion
     * @param fileName Nom du fichier à servir
     * @return Fichier demandé
     */
    @GetMapping("/cards/{fileName:.+}")
    public ResponseEntity<Resource> getCardFile(@PathVariable String fileName) {
        try {
            Resource file = membershipService.getCardFile(fileName);
            return ResponseEntity.ok()
                .header("Content-Disposition", "inline; filename=\"" + fileName + "\"")
                .body(file);
        } catch (IOException e) {
            return ResponseEntity.notFound().build();
        }
    }
} 