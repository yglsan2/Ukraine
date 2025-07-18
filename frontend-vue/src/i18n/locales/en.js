export default {
  meta: {
    languageName: 'English',
    nativeName: 'English',
    flag: '🇬🇧'
  },
  
  // Navigation
  nav: {
    home: 'Home',
    books: 'Books',
    events: 'Events',
    association: 'Association',
    chatbot: 'Chatbot',
    about: 'About',
    membership: 'Membership',
    selectLanguage: 'Select language'
  },
  
  // Home page
  home: {
    hero: {
      title: 'Lights of Ukraine',
      subtitle: 'Discover the cultural richness and beauty of Ukraine through our books, events and passionate community',
      exploreButton: 'Explore',
      joinButton: 'Join'
    },
    features: {
      title: 'Our Services',
      subtitle: 'A unique cultural experience',
      virtualLibrary: {
        title: 'Virtual Library',
        description: 'Access our exclusive collection of Ukrainian books'
      },
      culturalEvents: {
        title: 'Cultural Events',
        description: 'Participate in our meetings and shows'
      },
      artExhibitions: {
        title: 'Art Exhibitions',
        description: 'Discover contemporary Ukrainian artists'
      },
      traditionalMusic: {
        title: 'Traditional Music',
        description: 'Listen and learn Ukrainian music'
      },
      culturalExchange: {
        title: 'Cultural Exchange',
        description: 'Connect with the Ukrainian community'
      },
      learning: {
        title: 'Learning',
        description: 'Ukrainian language and history courses'
      }
    },
    stats: {
      members: 'Members',
      books: 'Books',
      events: 'Events',
      artists: 'Artists'
    },
    cta: {
      title: 'Ready to discover Ukraine?',
      subtitle: 'Join our community and share your passion',
      button: 'Start the adventure'
    }
  },
  
  // Books page
  books: {
    title: 'Ukrainian Library',
    subtitle: 'Discover our collection of Ukrainian books shared by the community',
    search: 'Search for a book...',
    addBook: 'Add a book',
    filters: {
      allCategories: 'All categories',
      allLanguages: 'All languages',
      categories: {
        novel: 'Novel',
        poetry: 'Poetry',
        history: 'History',
        culture: 'Culture',
        youth: 'Youth',
        politics: 'Politics',
        art: 'Art'
      },
      languages: {
        ukrainian: 'Ukrainian',
        french: 'French',
        english: 'English',
        german: 'German'
      }
    },
    book: {
      reserve: 'Reserve',
      reserved: 'Reserved',
      view: 'View more',
      condition: {
        excellent: 'Excellent',
        veryGood: 'Very good',
        good: 'Good',
        fair: 'Fair'
      }
    },
    modal: {
      addBook: 'Add a book',
      bookDetails: 'Book details',
      form: {
        title: 'Title',
        author: 'Author',
        category: 'Category',
        language: 'Language',
        condition: 'Condition',
        year: 'Publication year',
        description: 'Description',
        selectCategory: 'Select a category',
        selectLanguage: 'Select a language',
        selectCondition: 'Select condition',
        descriptionPlaceholder: 'Book description...',
        cancel: 'Cancel',
        add: 'Add book'
      }
    },
    notifications: {
      bookReserved: 'Book reserved!',
      bookAdded: 'Book added!',
      bookReservedMessage: 'has been added to your reservations.',
      bookAddedMessage: 'has been added to the library.'
    }
  },
  
  // Events page
  events: {
    title: 'Ukrainian Events',
    subtitle: 'Discover and participate in cultural, educational and solidarity events of our community',
    search: 'Search for an event...',
    addEvent: 'Add an event',
    filters: {
      allCategories: 'All categories',
      allLocations: 'All locations',
      categories: {
        culture: 'Culture',
        education: 'Education',
        solidarity: 'Solidarity',
        festival: 'Festival',
        conference: 'Conference',
        exhibition: 'Exhibition'
      },
      locations: {
        nancy: 'Nancy',
        paris: 'Paris',
        lyon: 'Lyon',
        marseille: 'Marseille',
        online: 'Online'
      }
    },
    view: {
      list: '📋 List',
      calendar: '📅 Calendar'
    },
    event: {
      register: 'Register',
      registered: 'Registered',
      view: 'View more',
      date: 'Date',
      time: 'Time',
      location: 'Location',
      participants: 'Participants'
    },
    modal: {
      addEvent: 'Add an event',
      eventDetails: 'Event details',
      form: {
        title: 'Title',
        description: 'Description',
        category: 'Category',
        date: 'Date',
        time: 'Time',
        location: 'Location',
        maxParticipants: 'Maximum number of participants',
        selectCategory: 'Select a category',
        selectLocation: 'Select a location',
        cancel: 'Cancel',
        add: 'Add event'
      }
    },
    notifications: {
      eventRegistered: 'Registration successful!',
      eventAdded: 'Event added!',
      eventRegisteredMessage: 'You are registered for this event.',
      eventAddedMessage: 'The event has been added to the calendar.'
    }
  },
  
  // Membership page
  membership: {
    title: 'Membership',
    subtitle: 'Join our association and support Ukrainian culture',
    form: {
      personalInfo: 'Personal information',
      firstName: 'First name',
      lastName: 'Last name',
      email: 'Email',
      phone: 'Phone',
      address: 'Address',
      city: 'City',
      postalCode: 'Postal code',
      country: 'Country',
      birthDate: 'Birth date',
      membershipType: 'Membership type',
      types: {
        individual: 'Individual',
        family: 'Family',
        student: 'Student',
        senior: 'Senior',
        benefactor: 'Benefactor'
      },
      submit: 'Submit membership'
    },
    card: {
      title: 'Membership Card',
      memberSince: 'Member since',
      membershipNumber: 'Membership number',
      validUntil: 'Valid until',
      download: 'Download',
      print: 'Print'
    }
  },
  
  // Association page
  association: {
    title: 'Our Association',
    subtitle: 'Discover our mission and values',
    mission: {
      title: 'Our Mission',
      description: 'Promote Ukrainian culture in France and foster cultural exchanges between our two countries.'
    },
    values: {
      title: 'Our Values',
      culturalHeritage: 'Cultural Heritage',
      solidarity: 'Solidarity',
      education: 'Education',
      diversity: 'Diversity'
    },
    team: {
      title: 'Our Team',
      president: 'President',
      vicePresident: 'Vice-President',
      secretary: 'Secretary',
      treasurer: 'Treasurer'
    }
  },
  
  // About page
  about: {
    title: 'About',
    subtitle: 'Learn more about our association',
    history: {
      title: 'Our History',
      description: 'Founded in 2020, our association is committed to promoting Ukrainian culture in France.'
    },
    objectives: {
      title: 'Our Objectives',
      culturalPromotion: 'Promote Ukrainian culture',
      languageLearning: 'Facilitate Ukrainian language learning',
      culturalExchange: 'Organize cultural exchanges',
      solidarity: 'Support solidarity initiatives'
    }
  },
  
  // Chatbot
  chatbot: {
    title: 'Virtual Assistant',
    subtitle: 'Ask your questions about Ukrainian culture',
    placeholder: 'Type your message...',
    send: 'Send',
    thinking: 'Thinking...',
    error: 'An error occurred. Please try again.'
  },
  
  // Footer
  footer: {
    title: 'Lights of Ukraine',
    subtitle: 'Discover Ukrainian cultural richness',
    description: 'Our association dedicated to promoting Ukrainian culture through literature, arts and cultural exchanges.',
    navigation: 'Navigation',
    resources: 'Resources',
    community: 'Community',
    home: 'Home',
    books: 'Books',
    events: 'Events',
    association: 'Association',
    chatbot: 'Chatbot',
    library: 'Library',
    exhibitions: 'Exhibitions',
    music: 'Music',
    artists: 'Artists',
    history: 'History',
    membership: 'Membership',
    volunteering: 'Volunteering',
    donations: 'Donations',
    partners: 'Partners',
    contact: 'Contact',
    followUs: 'Follow us',
    allRightsReserved: 'All rights reserved',
    legalNotices: 'Legal notice',
    privacyPolicy: 'Privacy policy',
    termsOfUse: 'Terms of use'
  },
  
  // Notifications
  notifications: {
    success: 'Success',
    error: 'Error',
    warning: 'Warning',
    info: 'Information'
  },
  
  // Common actions
  actions: {
    save: 'Save',
    cancel: 'Cancel',
    delete: 'Delete',
    edit: 'Edit',
    view: 'View',
    close: 'Close',
    back: 'Back',
    next: 'Next',
    previous: 'Previous',
    loading: 'Loading...',
    noResults: 'No results found',
    errorOccurred: 'An error occurred'
  }
} 