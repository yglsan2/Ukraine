export default {
  meta: {
    languageName: 'Français',
    nativeName: 'Français',
    flag: '🇫🇷',
  },

  // Navigation
  nav: {
    home: 'Accueil',
    books: 'Livres',
    events: 'Événements',
    association: 'Association',
    chatbot: 'Chatbot',
    about: 'À propos',
    membership: 'Adhésion',
    selectLanguage: 'Choisir la langue',
  },

  // Page d'accueil
  home: {
    hero: {
      title: "Lumières d'Ukraine",
      subtitle:
        "Découvrez la richesse culturelle et la beauté de l'Ukraine à travers nos livres, nos événements et notre communauté passionnée",
      exploreButton: 'Explorer',
      joinButton: 'Rejoindre',
    },
    features: {
      title: 'Nos Services',
      subtitle: 'Une expérience culturelle unique',
      virtualLibrary: {
        title: 'Bibliothèque Virtuelle',
        description: 'Accédez à notre collection exclusive de livres ukrainiens',
      },
      culturalEvents: {
        title: 'Événements Culturels',
        description: 'Participez à nos rencontres et spectacles',
      },
      artExhibitions: {
        title: "Expositions d'Art",
        description: 'Découvrez les artistes ukrainiens contemporains',
      },
      traditionalMusic: {
        title: 'Musique Traditionnelle',
        description: 'Écoutez et apprenez la musique ukrainienne',
      },
      culturalExchange: {
        title: 'Échanges Culturels',
        description: 'Connectez-vous avec la communauté ukrainienne',
      },
      learning: {
        title: 'Apprentissage',
        description: "Cours de langue et d'histoire ukrainienne",
      },
    },
    stats: {
      members: 'Membres',
      books: 'Livres',
      events: 'Événements',
      artists: 'Artistes',
    },
    cta: {
      title: "Prêt à découvrir l'Ukraine ?",
      subtitle: 'Rejoignez notre communauté et partagez votre passion',
      button: "Commencer l'aventure",
    },
  },

  // Page des livres
  books: {
    title: 'Bibliothèque Ukrainienne',
    subtitle: 'Découvrez notre collection de livres ukrainiens partagés par la communauté',
    search: 'Rechercher un livre...',
    addBook: 'Ajouter un livre',
    filters: {
      allCategories: 'Toutes les catégories',
      allLanguages: 'Toutes les langues',
      categories: {
        novel: 'Roman',
        poetry: 'Poésie',
        history: 'Histoire',
        culture: 'Culture',
        youth: 'Jeunesse',
        politics: 'Politique',
        art: 'Art',
      },
      languages: {
        ukrainian: 'Ukrainien',
        french: 'Français',
        english: 'Anglais',
        german: 'Allemand',
      },
    },
    book: {
      reserve: 'Réserver',
      reserved: 'Réservé',
      view: 'Voir plus',
      condition: {
        excellent: 'Excellent',
        veryGood: 'Très bon',
        good: 'Bon',
        fair: 'Moyen',
      },
    },
    modal: {
      addBook: 'Ajouter un livre',
      bookDetails: 'Détails du livre',
      form: {
        title: 'Titre',
        author: 'Auteur',
        category: 'Catégorie',
        language: 'Langue',
        condition: 'État',
        year: 'Année de publication',
        description: 'Description',
        selectCategory: 'Sélectionner une catégorie',
        selectLanguage: 'Sélectionner une langue',
        selectCondition: "Sélectionner l'état",
        descriptionPlaceholder: 'Description du livre...',
        cancel: 'Annuler',
        add: 'Ajouter le livre',
      },
    },
    notifications: {
      bookReserved: 'Livre réservé !',
      bookAdded: 'Livre ajouté !',
      bookReservedMessage: 'a été ajouté à vos réservations.',
      bookAddedMessage: 'a été ajouté à la bibliothèque.',
    },
  },

  // Page des événements
  events: {
    title: 'Événements Ukrainiens',
    subtitle:
      'Découvrez et participez aux événements culturels, éducatifs et solidaires de notre communauté',
    search: 'Rechercher un événement...',
    addEvent: 'Ajouter un événement',
    filters: {
      allCategories: 'Toutes les catégories',
      allLocations: 'Tous les lieux',
      categories: {
        culture: 'Culture',
        education: 'Éducation',
        solidarite: 'Solidarité',
        festival: 'Festival',
        conference: 'Conférence',
        exposition: 'Exposition',
      },
      locations: {
        nancy: 'Nancy',
        paris: 'Paris',
        lyon: 'Lyon',
        marseille: 'Marseille',
        online: 'En ligne',
      },
    },
    view: {
      list: '📋 Liste',
      calendar: '📅 Calendrier',
    },
    event: {
      register: "S'inscrire",
      registered: 'Inscrit',
      view: 'Voir plus',
      date: 'Date',
      time: 'Heure',
      location: 'Lieu',
      participants: 'Participants',
    },
    modal: {
      addEvent: 'Ajouter un événement',
      eventDetails: "Détails de l'événement",
      form: {
        title: 'Titre',
        description: 'Description',
        category: 'Catégorie',
        date: 'Date',
        time: 'Heure',
        location: 'Lieu',
        maxParticipants: 'Nombre maximum de participants',
        selectCategory: 'Sélectionner une catégorie',
        selectLocation: 'Sélectionner un lieu',
        cancel: 'Annuler',
        add: "Ajouter l'événement",
      },
    },
    notifications: {
      eventRegistered: 'Inscription réussie !',
      eventAdded: 'Événement ajouté !',
      eventRegisteredMessage: 'Vous êtes inscrit à cet événement.',
      eventAddedMessage: "L'événement a été ajouté au calendrier.",
    },
  },

  // Page d'adhésion
  membership: {
    title: 'Adhésion',
    subtitle: 'Rejoignez notre association et soutenez la culture ukrainienne',
    form: {
      personalInfo: 'Informations personnelles',
      firstName: 'Prénom',
      lastName: 'Nom',
      email: 'Email',
      phone: 'Téléphone',
      address: 'Adresse',
      city: 'Ville',
      postalCode: 'Code postal',
      country: 'Pays',
      birthDate: 'Date de naissance',
      membershipType: "Type d'adhésion",
      types: {
        individual: 'Individuel',
        family: 'Famille',
        student: 'Étudiant',
        senior: 'Senior',
        benefactor: 'Bienfaiteur',
      },
      submit: "Soumettre l'adhésion",
    },
    card: {
      title: "Carte d'Adhésion",
      memberSince: 'Membre depuis',
      membershipNumber: "Numéro d'adhésion",
      validUntil: "Valide jusqu'au",
      download: 'Télécharger',
      print: 'Imprimer',
    },
  },

  // Page de l'association
  association: {
    title: 'Notre Association',
    subtitle: 'Découvrez notre mission et nos valeurs',
    mission: {
      title: 'Notre Mission',
      description:
        'Promouvoir la culture ukrainienne en France et favoriser les échanges culturels entre nos deux pays.',
    },
    values: {
      title: 'Nos Valeurs',
      culturalHeritage: 'Patrimoine Culturel',
      solidarity: 'Solidarité',
      education: 'Éducation',
      diversity: 'Diversité',
    },
    team: {
      title: 'Notre Équipe',
      president: 'Président',
      vicePresident: 'Vice-Président',
      secretary: 'Secrétaire',
      treasurer: 'Trésorier',
    },
  },

  // Page À propos
  about: {
    title: 'À Propos',
    subtitle: 'En savoir plus sur notre association',
    history: {
      title: 'Notre Histoire',
      description:
        "Fondée en 2020, notre association s'engage à promouvoir la culture ukrainienne en France.",
    },
    objectives: {
      title: 'Nos Objectifs',
      culturalPromotion: 'Promouvoir la culture ukrainienne',
      languageLearning: "Faciliter l'apprentissage de la langue ukrainienne",
      culturalExchange: 'Organiser des échanges culturels',
      solidarity: 'Soutenir les initiatives de solidarité',
    },
  },

  // Chatbot
  chatbot: {
    title: 'Assistant Virtuel',
    subtitle: 'Posez vos questions sur la culture ukrainienne',
    placeholder: 'Tapez votre message...',
    send: 'Envoyer',
    thinking: 'Réflexion...',
    error: "Une erreur s'est produite. Veuillez réessayer.",
  },

  // Footer
  footer: {
    title: "Lumières d'Ukraine",
    subtitle: 'Promotion de la culture ukrainienne',
    description:
      "Notre association se consacre à la promotion de la culture ukrainienne à travers la littérature, l'art et les échanges culturels.",
    navigation: 'Navigation',
    resources: 'Ressources',
    community: 'Communauté',
    home: 'Accueil',
    books: 'Livres',
    events: 'Événements',
    association: 'Association',
    chatbot: 'Chatbot',
    library: 'Bibliothèque',
    exhibitions: 'Expositions',
    music: 'Musique',
    artists: 'Artistes',
    history: 'Histoire',
    membership: 'Adhésion',
    volunteering: 'Bénévolat',
    donations: 'Dons',
    partners: 'Partenaires',
    contact: 'Contact',
    followUs: 'Suivez-nous',
    allRightsReserved: 'Tous droits réservés',
    legalNotices: 'Mentions légales',
    privacyPolicy: 'Politique de confidentialité',
    termsOfUse: "Conditions d'utilisation",
  },

  // Notifications
  notifications: {
    success: 'Succès',
    error: 'Erreur',
    warning: 'Attention',
    info: 'Information',
  },

  // Actions communes
  actions: {
    save: 'Enregistrer',
    cancel: 'Annuler',
    delete: 'Supprimer',
    edit: 'Modifier',
    view: 'Voir',
    close: 'Fermer',
    back: 'Retour',
    next: 'Suivant',
    previous: 'Précédent',
    loading: 'Chargement...',
    noResults: 'Aucun résultat trouvé',
    errorOccurred: "Une erreur s'est produite",
  },

  // Éléments communs
  common: {
    book: 'livre',
    books: 'livres',
    found: 'trouvé',
    foundPlural: 'trouvés',
    event: 'événement',
    events: 'événements',
    by: 'par',
    description: 'Description',
    language: 'Langue',
    condition: 'État',
    publicationYear: 'Année de publication',
    selectLanguage: 'Sélectionner une langue',
    selectCondition: "Sélectionner l'état",
    excellent: 'Excellent',
    veryGood: 'Très bon',
    good: 'Bon',
    average: 'Moyen',
    ukrainien: 'Ukrainien',
    francais: 'Français',
    anglais: 'Anglais',
    allemand: 'Allemand',
    roman: 'Roman',
    poesie: 'Poésie',
    histoire: 'Histoire',
    culture: 'Culture',
    jeunesse: 'Jeunesse',
    politique: 'Politique',
    art: 'Art',
    alreadyReserved: 'Déjà réservé',
    reserveThisBook: 'Réserver ce livre',
    addedOn: 'Ajouté le',
    bookReserved: 'Livre réservé',
    addedToReservations: 'ajouté à vos réservations',
    bookAdded: 'Livre ajouté',
    addedToLibrary: 'ajouté à la bibliothèque',
  },
}
