export default {
  meta: {
    languageName: 'Українська',
    nativeName: 'Українська',
    flag: '🇺🇦',
  },

  // Navigation
  nav: {
    home: 'Головна',
    books: 'Книги',
    events: 'Події',
    association: 'Асоціація',
    chatbot: 'Чат-бот',
    about: 'Про нас',
    membership: 'Членство',
    selectLanguage: 'Вибрати мову',
  },

  // Home page
  home: {
    hero: {
      title: 'Світла України',
      subtitle:
        'Відкрийте культурне багатство та красу України через наші книги, події та пристрасну спільноту',
      exploreButton: 'Дослідити',
      joinButton: 'Приєднатися',
    },
    features: {
      title: 'Наші Послуги',
      subtitle: 'Унікальний культурний досвід',
      virtualLibrary: {
        title: 'Віртуальна Бібліотека',
        description: 'Отримайте доступ до нашої ексклюзивної колекції українських книг',
      },
      culturalEvents: {
        title: 'Культурні Події',
        description: 'Беріть участь у наших зустрічах та виставах',
      },
      artExhibitions: {
        title: 'Художні Виставки',
        description: 'Відкрийте сучасних українських митців',
      },
      traditionalMusic: {
        title: 'Традиційна Музика',
        description: 'Слухайте та вивчайте українську музику',
      },
      culturalExchange: {
        title: 'Культурний Обмін',
        description: "З'єднайтеся з українською спільнотою",
      },
      learning: {
        title: 'Навчання',
        description: 'Курси української мови та історії',
      },
    },
    stats: {
      members: 'Члени',
      books: 'Книги',
      events: 'Події',
      artists: 'Митці',
    },
    cta: {
      title: 'Готові відкрити Україну?',
      subtitle: 'Приєднуйтесь до нашої спільноти та поділіться своєю пристрастю',
      button: 'Почати пригоду',
    },
  },

  // Books page
  books: {
    title: 'Українська Бібліотека',
    subtitle: 'Відкрийте нашу колекцію українських книг, поділену спільнотою',
    search: 'Пошук книги...',
    addBook: 'Додати книгу',
    filters: {
      allCategories: 'Всі категорії',
      allLanguages: 'Всі мови',
      categories: {
        novel: 'Роман',
        poetry: 'Поезія',
        history: 'Історія',
        culture: 'Культура',
        youth: 'Молодь',
        politics: 'Політика',
        art: 'Мистецтво',
      },
      languages: {
        ukrainian: 'Українська',
        french: 'Французька',
        english: 'Англійська',
        german: 'Німецька',
      },
    },
    book: {
      reserve: 'Забронювати',
      reserved: 'Заброньовано',
      view: 'Детальніше',
      condition: {
        excellent: 'Відмінно',
        veryGood: 'Дуже добре',
        good: 'Добре',
        fair: 'Задовільно',
      },
    },
    modal: {
      addBook: 'Додати книгу',
      bookDetails: 'Деталі книги',
      form: {
        title: 'Назва',
        author: 'Автор',
        category: 'Категорія',
        language: 'Мова',
        condition: 'Стан',
        year: 'Рік публікації',
        description: 'Опис',
        selectCategory: 'Виберіть категорію',
        selectLanguage: 'Виберіть мову',
        selectCondition: 'Виберіть стан',
        descriptionPlaceholder: 'Опис книги...',
        cancel: 'Скасувати',
        add: 'Додати книгу',
      },
    },
    notifications: {
      bookReserved: 'Книгу заброньовано!',
      bookAdded: 'Книгу додано!',
      bookReservedMessage: 'додано до ваших бронювань.',
      bookAddedMessage: 'додано до бібліотеки.',
    },
  },

  // Events page
  events: {
    title: 'Українські Події',
    subtitle:
      'Відкрийте та беріть участь у культурних, освітніх та солідарних подіях нашої спільноти',
    search: 'Пошук події...',
    addEvent: 'Додати подію',
    viewMode: {
      list: 'Список',
      calendar: 'Календар',
    },
    filters: {
      allCategories: 'Всі категорії',
      allLocations: 'Всі місця',
      categories: {
        culture: 'Культура',
        education: 'Освіта',
        solidarity: 'Солідарність',
        festival: 'Фестиваль',
        conference: 'Конференція',
        exhibition: 'Виставка',
      },
      locations: {
        nancy: 'Нансі',
        paris: 'Париж',
        lyon: 'Ліон',
        marseille: 'Марсель',
        online: 'Онлайн',
      },
    },
    event: {
      register: 'Зареєструватися',
      registered: 'Зареєстровано',
      view: 'Детальніше',
      attendees: 'учасник',
      attendeesPlural: 'учасників',
    },
    modal: {
      addEvent: 'Додати подію',
      eventDetails: 'Деталі події',
      form: {
        title: 'Назва',
        category: 'Категорія',
        date: 'Дата',
        time: 'Час',
        location: 'Місце',
        organizer: 'Організатор',
        description: 'Опис',
        selectCategory: 'Виберіть категорію',
        descriptionPlaceholder: 'Опис події...',
        cancel: 'Скасувати',
        add: 'Додати подію',
      },
    },
    notifications: {
      eventRegistered: 'Реєстрація успішна!',
      eventCreated: 'Подію створено!',
      eventRegisteredMessage: 'Ви зареєстровані на',
      eventCreatedMessage: 'додано до календаря.',
    },
  },

  // Membership page
  membership: {
    title: 'Членство',
    subtitle: 'Приєднуйтесь до нашої асоціації та підтримуйте українську культуру',
    form: {
      personalInfo: 'Особиста інформація',
      firstName: "Ім'я",
      lastName: 'Прізвище',
      email: 'Електронна пошта',
      phone: 'Телефон',
      address: 'Адреса',
      city: 'Місто',
      postalCode: 'Поштовий індекс',
      country: 'Країна',
      birthDate: 'Дата народження',
      membershipType: 'Тип членства',
      types: {
        individual: 'Індивідуальний',
        family: 'Сімейний',
        student: 'Студентський',
        senior: 'Старший',
        benefactor: 'Благодійник',
      },
      submit: 'Подати заявку на членство',
    },
    card: {
      title: 'Картка Члена',
      memberSince: 'Член з',
      membershipNumber: 'Номер членства',
      validUntil: 'Дійсна до',
      download: 'Завантажити',
      print: 'Друкувати',
    },
  },

  // Association page
  association: {
    title: 'Наша Асоціація',
    subtitle: 'Дізнайтеся про нашу місію та цінності',
    mission: {
      title: 'Наша Місія',
      description:
        'Сприяти українській культурі у Франції та забезпечувати культурний обмін між нашими двома країнами.',
    },
    values: {
      title: 'Наші Цінності',
      culturalHeritage: 'Культурна Спадщина',
      solidarity: 'Солідарність',
      education: 'Освіта',
      diversity: 'Різноманітність',
    },
    team: {
      title: 'Наша Команда',
      president: 'Президент',
      vicePresident: 'Віце-президент',
      secretary: 'Секретар',
      treasurer: 'Скарбник',
    },
  },

  // About page
  about: {
    title: 'Про Нас',
    subtitle: 'Дізнайтеся більше про нашу асоціацію',
    history: {
      title: 'Наша Історія',
      description:
        "Заснована в 2020 році, наша асоціація зобов'язується сприяти українській культурі у Франції.",
    },
    objectives: {
      title: 'Наші Цілі',
      culturalPromotion: 'Сприяти українській культурі',
      languageLearning: 'Сприяти вивченню української мови',
      culturalExchange: 'Організовувати культурний обмін',
      solidarity: 'Підтримувати ініціативи солідарності',
    },
  },

  // Chatbot
  chatbot: {
    title: 'Віртуальний Помічник',
    subtitle: 'Задайте свої питання про українську культуру',
    placeholder: 'Введіть ваше повідомлення...',
    send: 'Надіслати',
    thinking: 'Думаю...',
    error: 'Сталася помилка. Спробуйте ще раз.',
  },

  // Footer
  footer: {
    title: 'Світла України',
    subtitle: 'Відкрийте українське культурне багатство',
    description:
      'Наша асоціація, присвячена просуванню української культури через літературу, мистецтво та культурний обмін.',
    navigation: 'Навігація',
    resources: 'Ресурси',
    community: 'Спільнота',
    home: 'Головна',
    books: 'Книги',
    events: 'Події',
    association: 'Асоціація',
    chatbot: 'Чатбот',
    library: 'Бібліотека',
    exhibitions: 'Виставки',
    music: 'Музика',
    artists: 'Митці',
    history: 'Історія',
    membership: 'Членство',
    volunteering: 'Волонтерство',
    donations: 'Пожертви',
    partners: 'Партнери',
    contact: 'Контакт',
    followUs: 'Слідкуйте за нами',
    allRightsReserved: 'Всі права захищені',
    legalNotices: 'Правові повідомлення',
    privacyPolicy: 'Політика конфіденційності',
    termsOfUse: 'Умови використання',
  },

  // Notifications
  notifications: {
    success: 'Успіх',
    error: 'Помилка',
    warning: 'Попередження',
    info: 'Інформація',
  },

  // Common actions
  actions: {
    save: 'Зберегти',
    cancel: 'Скасувати',
    delete: 'Видалити',
    edit: 'Редагувати',
    view: 'Переглянути',
    close: 'Закрити',
    back: 'Назад',
    next: 'Далі',
    previous: 'Попередній',
    loading: 'Завантаження...',
    noResults: 'Результатів не знайдено',
    errorOccurred: 'Сталася помилка',
  },
}
