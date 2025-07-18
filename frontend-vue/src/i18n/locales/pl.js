export default {
  meta: {
    languageName: 'Polski',
    nativeName: 'Polski',
    flag: '🇵🇱'
  },
  
  // Navigation
  nav: {
    home: 'Strona główna',
    books: 'Książki',
    events: 'Wydarzenia',
    association: 'Stowarzyszenie',
    chatbot: 'Chatbot',
    about: 'O nas',
    membership: 'Członkostwo',
    selectLanguage: 'Wybierz język'
  },
  
  // Home page
  home: {
    hero: {
      title: 'Światła Ukrainy',
      subtitle: 'Odkryj bogactwo kulturowe i piękno Ukrainy poprzez nasze książki, wydarzenia i pasjonującą społeczność',
      exploreButton: 'Eksploruj',
      joinButton: 'Dołącz'
    },
    features: {
      title: 'Nasze Usługi',
      subtitle: 'Unikalne doświadczenie kulturowe',
      virtualLibrary: {
        title: 'Wirtualna Biblioteka',
        description: 'Uzyskaj dostęp do naszej ekskluzywnej kolekcji ukraińskich książek'
      },
      culturalEvents: {
        title: 'Wydarzenia Kulturalne',
        description: 'Weź udział w naszych spotkaniach i przedstawieniach'
      },
      artExhibitions: {
        title: 'Wystawy Sztuki',
        description: 'Odkryj współczesnych ukraińskich artystów'
      },
      traditionalMusic: {
        title: 'Muzyka Tradycyjna',
        description: 'Słuchaj i ucz się ukraińskiej muzyki'
      },
      culturalExchange: {
        title: 'Wymiana Kulturalna',
        description: 'Połącz się z ukraińską społecznością'
      },
      learning: {
        title: 'Nauka',
        description: 'Kursy języka ukraińskiego i historii'
      }
    },
    stats: {
      members: 'Członkowie',
      books: 'Książki',
      events: 'Wydarzenia',
      artists: 'Artyści'
    },
    cta: {
      title: 'Gotowy odkryć Ukrainę?',
      subtitle: 'Dołącz do naszej społeczności i podziel się swoją pasją',
      button: 'Rozpocznij przygodę'
    }
  },
  
  // Books page
  books: {
    title: 'Ukraińska Biblioteka',
    subtitle: 'Odkryj naszą kolekcję ukraińskich książek udostępnionych przez społeczność',
    search: 'Szukaj książki...',
    addBook: 'Dodaj książkę',
    filters: {
      allCategories: 'Wszystkie kategorie',
      allLanguages: 'Wszystkie języki',
      categories: {
        novel: 'Powieść',
        poetry: 'Poezja',
        history: 'Historia',
        culture: 'Kultura',
        youth: 'Młodzież',
        politics: 'Polityka',
        art: 'Sztuka'
      },
      languages: {
        ukrainian: 'Ukraiński',
        french: 'Francuski',
        english: 'Angielski',
        german: 'Niemiecki'
      }
    },
    book: {
      reserve: 'Zarezerwuj',
      reserved: 'Zarezerwowane',
      view: 'Zobacz więcej',
      condition: {
        excellent: 'Doskonałe',
        veryGood: 'Bardzo dobre',
        good: 'Dobre',
        fair: 'Dostateczne'
      }
    },
    modal: {
      addBook: 'Dodaj książkę',
      bookDetails: 'Szczegóły książki',
      form: {
        title: 'Tytuł',
        author: 'Autor',
        category: 'Kategoria',
        language: 'Język',
        condition: 'Stan',
        year: 'Rok wydania',
        description: 'Opis',
        selectCategory: 'Wybierz kategorię',
        selectLanguage: 'Wybierz język',
        selectCondition: 'Wybierz stan',
        descriptionPlaceholder: 'Opis książki...',
        cancel: 'Anuluj',
        add: 'Dodaj książkę'
      }
    },
    notifications: {
      bookReserved: 'Książka zarezerwowana!',
      bookAdded: 'Książka dodana!',
      bookReservedMessage: 'została dodana do Twoich rezerwacji.',
      bookAddedMessage: 'została dodana do biblioteki.'
    }
  },
  
  // Events page
  events: {
    title: 'Ukraińskie Wydarzenia',
    subtitle: 'Odkryj i weź udział w kulturalnych, edukacyjnych i solidarnościowych wydarzeniach naszej społeczności',
    search: 'Szukaj wydarzenia...',
    addEvent: 'Dodaj wydarzenie',
    viewMode: {
      list: 'Lista',
      calendar: 'Kalendarz'
    },
    filters: {
      allCategories: 'Wszystkie kategorie',
      allLocations: 'Wszystkie lokalizacje',
      categories: {
        culture: 'Kultura',
        education: 'Edukacja',
        solidarity: 'Solidarność',
        festival: 'Festival',
        conference: 'Konferencja',
        exhibition: 'Wystawa'
      },
      locations: {
        nancy: 'Nancy',
        paris: 'Paryż',
        lyon: 'Lyon',
        marseille: 'Marsylia',
        online: 'Online'
      }
    },
    event: {
      register: 'Zarejestruj się',
      registered: 'Zarejestrowany',
      view: 'Zobacz więcej',
      attendees: 'uczestnik',
      attendeesPlural: 'uczestników'
    },
    modal: {
      addEvent: 'Dodaj wydarzenie',
      eventDetails: 'Szczegóły wydarzenia',
      form: {
        title: 'Tytuł',
        category: 'Kategoria',
        date: 'Data',
        time: 'Czas',
        location: 'Lokalizacja',
        organizer: 'Organizator',
        description: 'Opis',
        selectCategory: 'Wybierz kategorię',
        descriptionPlaceholder: 'Opis wydarzenia...',
        cancel: 'Anuluj',
        add: 'Dodaj wydarzenie'
      }
    },
    notifications: {
      eventRegistered: 'Rejestracja udana!',
      eventCreated: 'Wydarzenie utworzone!',
      eventRegisteredMessage: 'Jesteś zarejestrowany na',
      eventCreatedMessage: 'zostało dodane do kalendarza.'
    }
  },
  
  // Membership page
  membership: {
    title: 'Członkostwo',
    subtitle: 'Dołącz do naszego stowarzyszenia i wspieraj ukraińską kulturę',
    form: {
      personalInfo: 'Informacje osobiste',
      firstName: 'Imię',
      lastName: 'Nazwisko',
      email: 'Email',
      phone: 'Telefon',
      address: 'Adres',
      city: 'Miasto',
      postalCode: 'Kod pocztowy',
      country: 'Kraj',
      birthDate: 'Data urodzenia',
      membershipType: 'Typ członkostwa',
      types: {
        individual: 'Indywidualne',
        family: 'Rodzinne',
        student: 'Studenckie',
        senior: 'Senior',
        benefactor: 'Dobroczyńca'
      },
      submit: 'Złóż wniosek o członkostwo'
    },
    card: {
      title: 'Karta Członka',
      memberSince: 'Członek od',
      membershipNumber: 'Numer członkostwa',
      validUntil: 'Ważne do',
      download: 'Pobierz',
      print: 'Drukuj'
    }
  },
  
  // Association page
  association: {
    title: 'Nasze Stowarzyszenie',
    subtitle: 'Odkryj naszą misję i wartości',
    mission: {
      title: 'Nasza Misja',
      description: 'Promowanie ukraińskiej kultury we Francji i wspieranie wymiany kulturalnej między naszymi dwoma krajami.'
    },
    values: {
      title: 'Nasze Wartości',
      culturalHeritage: 'Dziedzictwo Kulturowe',
      solidarity: 'Solidarność',
      education: 'Edukacja',
      diversity: 'Różnorodność'
    },
    team: {
      title: 'Nasz Zespół',
      president: 'Prezes',
      vicePresident: 'Wiceprezes',
      secretary: 'Sekretarz',
      treasurer: 'Skarbnik'
    }
  },
  
  // About page
  about: {
    title: 'O Nas',
    subtitle: 'Dowiedz się więcej o naszym stowarzyszeniu',
    history: {
      title: 'Nasza Historia',
      description: 'Założone w 2020 roku, nasze stowarzyszenie zobowiązuje się do promowania ukraińskiej kultury we Francji.'
    },
    objectives: {
      title: 'Nasze Cele',
      culturalPromotion: 'Promowanie ukraińskiej kultury',
      languageLearning: 'Ułatwianie nauki języka ukraińskiego',
      culturalExchange: 'Organizowanie wymiany kulturalnej',
      solidarity: 'Wspieranie inicjatyw solidarnościowych'
    }
  },
  
  // Chatbot
  chatbot: {
    title: 'Asystent Wirtualny',
    subtitle: 'Zadaj pytania o ukraińską kulturę',
    placeholder: 'Wpisz swoją wiadomość...',
    send: 'Wyślij',
    thinking: 'Myślę...',
    error: 'Wystąpił błąd. Spróbuj ponownie.'
  },
  
  // Footer
  footer: {
    title: 'Światła Ukrainy',
    subtitle: 'Odkryj ukraińskie bogactwo kulturowe',
    description: 'Nasze stowarzyszenie poświęcone promowaniu ukraińskiej kultury poprzez literaturę, sztukę i wymianę kulturalną.',
    navigation: 'Nawigacja',
    resources: 'Zasoby',
    community: 'Społeczność',
    home: 'Strona główna',
    books: 'Książki',
    events: 'Wydarzenia',
    association: 'Stowarzyszenie',
    chatbot: 'Chatbot',
    library: 'Biblioteka',
    exhibitions: 'Wystawy',
    music: 'Muzyka',
    artists: 'Artyści',
    history: 'Historia',
    membership: 'Członkostwo',
    volunteering: 'Wolontariat',
    donations: 'Darowizny',
    partners: 'Partnerzy',
    contact: 'Kontakt',
    followUs: 'Śledź nas',
    allRightsReserved: 'Wszystkie prawa zastrzeżone',
    legalNotices: 'Informacje prawne',
    privacyPolicy: 'Polityka prywatności',
    termsOfUse: 'Warunki użytkowania'
  },
  
  // Notifications
  notifications: {
    success: 'Sukces',
    error: 'Błąd',
    warning: 'Ostrzeżenie',
    info: 'Informacja'
  },
  
  // Common actions
  actions: {
    save: 'Zapisz',
    cancel: 'Anuluj',
    delete: 'Usuń',
    edit: 'Edytuj',
    view: 'Zobacz',
    close: 'Zamknij',
    back: 'Wstecz',
    next: 'Dalej',
    previous: 'Poprzedni',
    loading: 'Ładowanie...',
    noResults: 'Nie znaleziono wyników',
    errorOccurred: 'Wystąpił błąd'
  }
} 
