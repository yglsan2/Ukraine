export default {
  meta: {
    languageName: 'Deutsch',
    nativeName: 'Deutsch',
    flag: '🇩🇪',
  },

  // Navigation
  nav: {
    home: 'Startseite',
    books: 'Bücher',
    events: 'Veranstaltungen',
    association: 'Verein',
    chatbot: 'Chatbot',
    about: 'Über uns',
    membership: 'Mitgliedschaft',
    selectLanguage: 'Sprache auswählen',
  },

  // Home page
  home: {
    hero: {
      title: 'Lichter der Ukraine',
      subtitle:
        'Entdecken Sie den kulturellen Reichtum und die Schönheit der Ukraine durch unsere Bücher, Veranstaltungen und leidenschaftliche Gemeinschaft',
      exploreButton: 'Entdecken',
      joinButton: 'Beitreten',
    },
    features: {
      title: 'Unsere Dienstleistungen',
      subtitle: 'Eine einzigartige kulturelle Erfahrung',
      virtualLibrary: {
        title: 'Virtuelle Bibliothek',
        description: 'Zugang zu unserer exklusiven Sammlung ukrainischer Bücher',
      },
      culturalEvents: {
        title: 'Kulturelle Veranstaltungen',
        description: 'Nehmen Sie an unseren Treffen und Shows teil',
      },
      artExhibitions: {
        title: 'Kunstausstellungen',
        description: 'Entdecken Sie zeitgenössische ukrainische Künstler',
      },
      traditionalMusic: {
        title: 'Traditionelle Musik',
        description: 'Hören und lernen Sie ukrainische Musik',
      },
      culturalExchange: {
        title: 'Kulturaustausch',
        description: 'Verbinden Sie sich mit der ukrainischen Gemeinschaft',
      },
      learning: {
        title: 'Lernen',
        description: 'Ukrainische Sprach- und Geschichtskurse',
      },
    },
    stats: {
      members: 'Mitglieder',
      books: 'Bücher',
      events: 'Veranstaltungen',
      artists: 'Künstler',
    },
    cta: {
      title: 'Bereit, die Ukraine zu entdecken?',
      subtitle: 'Treten Sie unserer Gemeinschaft bei und teilen Sie Ihre Leidenschaft',
      button: 'Abenteuer beginnen',
    },
  },

  // Books page
  books: {
    title: 'Ukrainische Bibliothek',
    subtitle: 'Entdecken Sie unsere Sammlung ukrainischer Bücher, geteilt von der Gemeinschaft',
    search: 'Nach einem Buch suchen...',
    addBook: 'Buch hinzufügen',
    filters: {
      allCategories: 'Alle Kategorien',
      allLanguages: 'Alle Sprachen',
      categories: {
        novel: 'Roman',
        poetry: 'Poesie',
        history: 'Geschichte',
        culture: 'Kultur',
        youth: 'Jugend',
        politics: 'Politik',
        art: 'Kunst',
      },
      languages: {
        ukrainian: 'Ukrainisch',
        french: 'Französisch',
        english: 'Englisch',
        german: 'Deutsch',
      },
    },
    book: {
      reserve: 'Reservieren',
      reserved: 'Reserviert',
      view: 'Mehr anzeigen',
      condition: {
        excellent: 'Ausgezeichnet',
        veryGood: 'Sehr gut',
        good: 'Gut',
        fair: 'Befriedigend',
      },
    },
    modal: {
      addBook: 'Buch hinzufügen',
      bookDetails: 'Buchdetails',
      form: {
        title: 'Titel',
        author: 'Autor',
        category: 'Kategorie',
        language: 'Sprache',
        condition: 'Zustand',
        year: 'Erscheinungsjahr',
        description: 'Beschreibung',
        selectCategory: 'Kategorie auswählen',
        selectLanguage: 'Sprache auswählen',
        selectCondition: 'Zustand auswählen',
        descriptionPlaceholder: 'Buchbeschreibung...',
        cancel: 'Abbrechen',
        add: 'Buch hinzufügen',
      },
    },
    notifications: {
      bookReserved: 'Buch reserviert!',
      bookAdded: 'Buch hinzugefügt!',
      bookReservedMessage: 'wurde zu Ihren Reservierungen hinzugefügt.',
      bookAddedMessage: 'wurde zur Bibliothek hinzugefügt.',
    },
  },

  // Events page
  events: {
    title: 'Ukrainische Veranstaltungen',
    subtitle:
      'Entdecken und nehmen Sie an kulturellen, pädagogischen und solidarischen Veranstaltungen unserer Gemeinschaft teil',
    search: 'Nach einer Veranstaltung suchen...',
    addEvent: 'Veranstaltung hinzufügen',
    viewMode: {
      list: 'Liste',
      calendar: 'Kalender',
    },
    filters: {
      allCategories: 'Alle Kategorien',
      allLocations: 'Alle Orte',
      categories: {
        culture: 'Kultur',
        education: 'Bildung',
        solidarity: 'Solidarität',
        festival: 'Festival',
        conference: 'Konferenz',
        exhibition: 'Ausstellung',
      },
      locations: {
        nancy: 'Nancy',
        paris: 'Paris',
        lyon: 'Lyon',
        marseille: 'Marseille',
        online: 'Online',
      },
    },
    event: {
      register: 'Registrieren',
      registered: 'Registriert',
      view: 'Mehr anzeigen',
      attendees: 'Teilnehmer',
      attendeesPlural: 'Teilnehmer',
    },
    modal: {
      addEvent: 'Veranstaltung hinzufügen',
      eventDetails: 'Veranstaltungsdetails',
      form: {
        title: 'Titel',
        category: 'Kategorie',
        date: 'Datum',
        time: 'Zeit',
        location: 'Ort',
        organizer: 'Veranstalter',
        description: 'Beschreibung',
        selectCategory: 'Kategorie auswählen',
        descriptionPlaceholder: 'Veranstaltungsbeschreibung...',
        cancel: 'Abbrechen',
        add: 'Veranstaltung hinzufügen',
      },
    },
    notifications: {
      eventRegistered: 'Registrierung erfolgreich!',
      eventCreated: 'Veranstaltung erstellt!',
      eventRegisteredMessage: 'Sie sind registriert für',
      eventCreatedMessage: 'wurde zum Kalender hinzugefügt.',
    },
  },

  // Membership page
  membership: {
    title: 'Mitgliedschaft',
    subtitle: 'Treten Sie unserem Verein bei und unterstützen Sie die ukrainische Kultur',
    form: {
      personalInfo: 'Persönliche Informationen',
      firstName: 'Vorname',
      lastName: 'Nachname',
      email: 'E-Mail',
      phone: 'Telefon',
      address: 'Adresse',
      city: 'Stadt',
      postalCode: 'Postleitzahl',
      country: 'Land',
      birthDate: 'Geburtsdatum',
      membershipType: 'Mitgliedschaftstyp',
      types: {
        individual: 'Einzelperson',
        family: 'Familie',
        student: 'Student',
        senior: 'Senior',
        benefactor: 'Wohltäter',
      },
      submit: 'Mitgliedschaft einreichen',
    },
    card: {
      title: 'Mitgliedskarte',
      memberSince: 'Mitglied seit',
      membershipNumber: 'Mitgliedsnummer',
      validUntil: 'Gültig bis',
      download: 'Herunterladen',
      print: 'Drucken',
    },
  },

  // Association page
  association: {
    title: 'Unser Verein',
    subtitle: 'Entdecken Sie unsere Mission und Werte',
    mission: {
      title: 'Unsere Mission',
      description:
        'Förderung der ukrainischen Kultur in Frankreich und Förderung des kulturellen Austauschs zwischen unseren beiden Ländern.',
    },
    values: {
      title: 'Unsere Werte',
      culturalHeritage: 'Kulturerbe',
      solidarity: 'Solidarität',
      education: 'Bildung',
      diversity: 'Vielfalt',
    },
    team: {
      title: 'Unser Team',
      president: 'Präsident',
      vicePresident: 'Vizepräsident',
      secretary: 'Sekretär',
      treasurer: 'Schatzmeister',
    },
  },

  // About page
  about: {
    title: 'Über uns',
    subtitle: 'Erfahren Sie mehr über unseren Verein',
    history: {
      title: 'Unsere Geschichte',
      description:
        'Gegründet im Jahr 2020, setzt sich unser Verein für die Förderung der ukrainischen Kultur in Frankreich ein.',
    },
    objectives: {
      title: 'Unsere Ziele',
      culturalPromotion: 'Förderung der ukrainischen Kultur',
      languageLearning: 'Erleichterung des ukrainischen Spracherwerbs',
      culturalExchange: 'Organisation kultureller Austausche',
      solidarity: 'Unterstützung solidarischer Initiativen',
    },
  },

  // Chatbot
  chatbot: {
    title: 'Virtueller Assistent',
    subtitle: 'Stellen Sie Ihre Fragen zur ukrainischen Kultur',
    placeholder: 'Geben Sie Ihre Nachricht ein...',
    send: 'Senden',
    thinking: 'Denke nach...',
    error: 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.',
  },

  // Footer
  footer: {
    description:
      'Unser Verein widmet sich der Förderung der ukrainischen Kultur durch Literatur, Kunst und kulturellen Austausch.',
    navigation: 'Navigation',
    resources: 'Ressourcen',
    community: 'Gemeinschaft',
    library: 'Bibliothek',
    exhibitions: 'Ausstellungen',
    music: 'Musik',
    artists: 'Künstler',
    history: 'Geschichte',
    membership: 'Mitgliedschaft',
    volunteering: 'Freiwilligenarbeit',
    donations: 'Spenden',
    partners: 'Partner',
    contact: 'Kontakt',
    followUs: 'Folgen Sie uns',
    copyright: '© 2024 Lichter der Ukraine. Alle Rechte vorbehalten.',
    legal: 'Rechtliche Hinweise',
    privacy: 'Datenschutzrichtlinie',
    terms: 'Nutzungsbedingungen',
  },

  // Notifications
  notifications: {
    success: 'Erfolg',
    error: 'Fehler',
    warning: 'Warnung',
    info: 'Information',
  },

  // Common actions
  actions: {
    save: 'Speichern',
    cancel: 'Abbrechen',
    delete: 'Löschen',
    edit: 'Bearbeiten',
    view: 'Anzeigen',
    close: 'Schließen',
    back: 'Zurück',
    next: 'Weiter',
    previous: 'Vorherige',
    loading: 'Laden...',
    noResults: 'Keine Ergebnisse gefunden',
    errorOccurred: 'Ein Fehler ist aufgetreten',
  },
}
