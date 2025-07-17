package com.ukraine;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * Application principale Spring Boot pour Lumières d'Ukraine.
 * 
 * <p>Cette application gère le système de prêt de livres entre particuliers
 * pour la communauté ukrainienne en France. Elle fournit les fonctionnalités
 * suivantes :</p>
 * 
 * <ul>
 *   <li>Gestion des utilisateurs et authentification sécurisée</li>
 *   <li>Gestion des livres avec photos et géolocalisation</li>
 *   <li>Système de réservation avec délais automatiques</li>
 *   <li>Gestion des événements communautaires</li>
 *   <li>Système de paiement sécurisé pour les adhésions</li>
 *   <li>Génération automatique de cartes d'adhésion</li>
 *   <li>Interface multilingue (5 langues)</li>
 *   <li>Tableau de bord administrateur</li>
 * </ul>
 * 
 * <p>L'application utilise les technologies suivantes :</p>
 * <ul>
 *   <li>Spring Boot 3.2.0</li>
 *   <li>Spring Security avec JWT</li>
 *   <li>Spring Data JPA avec PostgreSQL</li>
 *   <li>Stripe pour les paiements</li>
 *   <li>Logback pour le logging</li>
 *   <li>OpenAPI pour la documentation</li>
 * </ul>
 * 
 * @author Équipe Lumières d'Ukraine
 * @version 1.0.0
 * @since 2024-01-01
 */
@SpringBootApplication
@EnableCaching
@EnableAsync
@EnableScheduling
public class LumieresUkraineApplication {

    /**
     * Point d'entrée principal de l'application.
     * 
     * <p>Cette méthode démarre l'application Spring Boot et configure
     * automatiquement tous les composants nécessaires.</p>
     * 
     * @param args Arguments de ligne de commande passés à l'application
     */
    public static void main(String[] args) {
        SpringApplication.run(LumieresUkraineApplication.class, args);
    }
} 