package com.ukraine.service;

import com.ukraine.dto.MembershipCardRequest;
import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;

import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import java.io.IOException;
import java.net.URL;

/**
 * Service pour l'envoi d'emails avec les cartes d'adhésion
 */
@Service
public class EmailService {

    @Value("${spring.mail.username:admin@leslumieresdukraine.fr}")
    private String fromEmail;

    @Value("${spring.mail.properties.mail.smtp.auth:false}")
    private boolean smtpAuth;

    private final JavaMailSender mailSender;

    public EmailService(JavaMailSender mailSender) {
        this.mailSender = mailSender;
    }

    /**
     * Envoie une carte d'adhésion par email
     * @param to Email du destinataire
     * @param subject Sujet de l'email
     * @param message Contenu du message
     * @param frontImageUrl URL de l'image du recto
     * @param backImageUrl URL de l'image du verso
     * @param memberData Données du membre
     */
    public void sendMembershipCard(String to, String subject, String message, 
                                 String frontImageUrl, String backImageUrl, 
                                 MembershipCardRequest.MemberData memberData) {
        try {
            MimeMessage mimeMessage = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(mimeMessage, true, "UTF-8");

            helper.setFrom(fromEmail);
            helper.setTo(to);
            helper.setSubject(subject);
            
            // Créer le contenu HTML du message
            String htmlContent = createEmailHtmlContent(message, memberData);
            helper.setText(htmlContent, true);

            // Ajouter les pièces jointes
            if (frontImageUrl != null && !frontImageUrl.isEmpty()) {
                try {
                    Resource frontResource = new UrlResource(new URL(frontImageUrl));
                    helper.addAttachment("carte-recto.png", frontResource);
                } catch (IOException e) {
                    // Log l'erreur mais continue
                    System.err.println("Erreur lors de l'ajout du recto: " + e.getMessage());
                }
            }

            if (backImageUrl != null && !backImageUrl.isEmpty()) {
                try {
                    Resource backResource = new UrlResource(new URL(backImageUrl));
                    helper.addAttachment("carte-verso.png", backResource);
                } catch (IOException e) {
                    // Log l'erreur mais continue
                    System.err.println("Erreur lors de l'ajout du verso: " + e.getMessage());
                }
            }

            // Envoyer l'email
            mailSender.send(mimeMessage);
            
        } catch (MessagingException e) {
            throw new RuntimeException("Erreur lors de l'envoi de l'email: " + e.getMessage(), e);
        }
    }

    /**
     * Crée le contenu HTML de l'email
     * @param message Message personnalisé
     * @param memberData Données du membre
     * @return Contenu HTML
     */
    private String createEmailHtmlContent(String message, MembershipCardRequest.MemberData memberData) {
        return String.format("""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Votre carte d'adhésion - Les Lumières d'Ukraine</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    .header {
                        background: linear-gradient(135deg, #0057B8, #1e3c72);
                        color: white;
                        padding: 30px;
                        text-align: center;
                        border-radius: 10px 10px 0 0;
                    }
                    .header h1 {
                        margin: 0;
                        font-size: 24px;
                    }
                    .content {
                        background: #f9f9f9;
                        padding: 30px;
                        border-radius: 0 0 10px 10px;
                    }
                    .member-info {
                        background: white;
                        padding: 20px;
                        border-radius: 8px;
                        margin: 20px 0;
                        border-left: 4px solid #0057B8;
                    }
                    .member-info h3 {
                        margin: 0 0 15px 0;
                        color: #0057B8;
                    }
                    .member-detail {
                        margin: 8px 0;
                    }
                    .member-detail strong {
                        color: #0057B8;
                    }
                    .footer {
                        text-align: center;
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #ddd;
                        color: #666;
                        font-size: 14px;
                    }
                    .ukraine-colors {
                        background: linear-gradient(135deg, #0057B8 50%%, #FFD700 50%%);
                        height: 4px;
                        border-radius: 2px;
                        margin: 20px 0;
                    }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🌻 Les Lumières d'Ukraine</h1>
                    <p>Votre carte d'adhésion est prête !</p>
                </div>
                
                <div class="content">
                    <div class="ukraine-colors"></div>
                    
                    <p>%s</p>
                    
                    <div class="member-info">
                        <h3>📋 Informations de votre adhésion</h3>
                        <div class="member-detail">
                            <strong>Nom complet:</strong> %s %s
                        </div>
                        <div class="member-detail">
                            <strong>Numéro d'adhésion:</strong> %s
                        </div>
                        <div class="member-detail">
                            <strong>Email:</strong> %s
                        </div>
                        <div class="member-detail">
                            <strong>Adresse:</strong> %s, %s %s
                        </div>
                    </div>
                    
                    <p><strong>Votre carte d'adhésion recto-verso est jointe à cet email.</strong></p>
                    
                    <p>Vous pouvez l'imprimer et la plastifier pour une utilisation quotidienne.</p>
                    
                    <div class="ukraine-colors"></div>
                </div>
                
                <div class="footer">
                    <p><strong>Les Lumières d'Ukraine</strong></p>
                    <p>Association de soutien à l'Ukraine</p>
                    <p>Email: contact@leslumieresdukraine.fr</p>
                    <p>Merci de votre soutien ! 🇺🇦</p>
                </div>
            </body>
            </html>
            """,
            message.replace("\n", "<br>"),
            memberData.getFirstName(),
            memberData.getName(),
            memberData.getMemberNumber(),
            memberData.getEmail(),
            memberData.getAddress(),
            memberData.getPostalCode(),
            memberData.getCity()
        );
    }

    /**
     * Envoie un email de confirmation d'adhésion
     * @param memberData Données du membre
     */
    public void sendMembershipConfirmation(MembershipCardRequest.MemberData memberData) {
        String subject = "Confirmation d'adhésion - Les Lumières d'Ukraine";
        String message = String.format("""
            Bonjour %s %s,
            
            Nous avons le plaisir de vous confirmer votre adhésion à l'association "Les Lumières d'Ukraine".
            
            Votre numéro d'adhésion est : %s
            
            Votre carte d'adhésion vous sera envoyée dans un email séparé.
            
            Bienvenue dans notre association !
            
            L'équipe des Lumières d'Ukraine
            """,
            memberData.getFirstName(),
            memberData.getName(),
            memberData.getMemberNumber()
        );

        sendMembershipCard(memberData.getEmail(), subject, message, null, null, memberData);
    }

    /**
     * Envoie un email de rappel pour les cartes non récupérées
     * @param memberData Données du membre
     * @param daysSinceCreation Nombre de jours depuis la création
     */
    public void sendMembershipReminder(MembershipCardRequest.MemberData memberData, int daysSinceCreation) {
        String subject = "Rappel - Votre carte d'adhésion vous attend";
        String message = String.format("""
            Bonjour %s %s,
            
            Il y a %d jour(s) que votre adhésion a été créée, mais vous n'avez pas encore téléchargé votre carte d'adhésion.
            
            Votre numéro d'adhésion est : %s
            
            N'hésitez pas à nous contacter si vous rencontrez des difficultés.
            
            L'équipe des Lumières d'Ukraine
            """,
            memberData.getFirstName(),
            memberData.getName(),
            daysSinceCreation,
            memberData.getMemberNumber()
        );

        sendMembershipCard(memberData.getEmail(), subject, message, null, null, memberData);
    }
} 