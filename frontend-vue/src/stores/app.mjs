import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  // État réactif
  const user = ref(null)
  const books = ref([])
  const favorites = ref([])
  const messages = ref([])
  const notifications = ref([])
  const isLoading = ref(false)
  const isOnline = ref(navigator.onLine)

  // Computed properties
  const isAuthenticated = computed(() => !!user.value)
  const userRole = computed(() => user.value?.role || 'VISITEUR')
  const totalBooks = computed(() => books.value.length)
  const totalFavorites = computed(() => favorites.value.length)
  const unreadMessages = computed(() => messages.value.filter(m => !m.read).length)
  const unreadNotifications = computed(() => notifications.value.filter(n => !n.read).length)
  
  // Nouvelles statistiques réelles
  const totalUsers = computed(() => {
    // Compte les utilisateurs uniques basés sur les propriétaires des livres
    const uniqueOwners = new Set(books.value.map(book => book.owner.id))
    return uniqueOwners.size + 1 // +1 pour l'utilisateur actuel
  })
  
  const totalExchanges = computed(() => {
    // Simulation basée sur les livres disponibles et les favoris
    return Math.floor(totalBooks.value * 0.3) + totalFavorites.value
  })
  
  const booksByGenre = computed(() => {
    const genres = {}
    books.value.forEach(book => {
      genres[book.genre] = (genres[book.genre] || 0) + 1
    })
    return genres
  })
  
  const booksByLanguage = computed(() => {
    const languages = {}
    books.value.forEach(book => {
      languages[book.language] = (languages[book.language] || 0) + 1
    })
    return languages
  })
  
  const recentBooks = computed(() => {
    return books.value
      .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
      .slice(0, 6)
  })
  
  const popularBooks = computed(() => {
    return books.value
      .sort((a, b) => (b.owner.rating || 0) - (a.owner.rating || 0))
      .slice(0, 6)
  })

  // Actions
  const login = async (email) => {
    try {
      isLoading.value = true
      
      // Simulation d'une API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const mockUser = {
        id: 1,
        email,
        name: 'Utilisateur Test',
        role: 'UTILISATEUR',
        avatar: '/avatars/default.png',
        city: 'Nancy',
        rating: 4.5,
        booksDonated: 12,
        booksReceived: 8,
        badges: ['Super donneur', 'Lecteur actif'],
        createdAt: new Date().toISOString()
      }
      
      user.value = mockUser
      localStorage.setItem('user', JSON.stringify(mockUser))
      
      return { success: true, user: mockUser }
    } catch (error) {
      console.error('Erreur de connexion:', error)
      return { success: false, error: 'Erreur de connexion' }
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    user.value = null
    localStorage.removeItem('user')
    favorites.value = []
    messages.value = []
    notifications.value = []
  }

  const register = async (userData) => {
    try {
      isLoading.value = true
      
      // Simulation d'une API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const newUser = {
        id: Date.now(),
        email: userData.email,
        name: userData.name,
        role: 'UTILISATEUR',
        avatar: '/avatars/default.png',
        city: userData.city || 'Non spécifié',
        rating: 0,
        booksDonated: 0,
        booksReceived: 0,
        badges: [],
        createdAt: new Date().toISOString()
      }
      
      user.value = newUser
      localStorage.setItem('user', JSON.stringify(newUser))
      
      return { success: true, user: newUser }
    } catch (error) {
      console.error('Erreur d\'inscription:', error)
      return { success: false, error: 'Erreur d\'inscription' }
    } finally {
      isLoading.value = false
    }
  }

  const loadBooks = async () => {
    try {
      isLoading.value = true
      
      // Simulation d'une API call
      await new Promise(resolve => setTimeout(resolve, 800))
      
      const mockBooks = [
        {
          id: 1,
          title: "Les Champs de Blé",
          author: "Taras Chevtchenko",
          genre: "POESIE",
          language: "ukrainien",
          ageGroup: "ADULTE",
          availability: "disponible",
          city: "Nancy",
          description: "Recueil de poèmes célèbres du poète national ukrainien.",
          isbn: "978-2-123456-78-9",
          photo: "/books/livre1.jpg",
          owner: {
            id: 2,
            name: "Marie Dubois",
            rating: 4.8
          },
          condition: "EXCELLENT",
          createdAt: new Date().toISOString()
        },
        {
          id: 2,
          title: "L'Histoire de l'Ukraine",
          author: "Mykhailo Hrushevsky",
          genre: "HISTOIRE",
          language: "français",
          ageGroup: "ADULTE",
          availability: "disponible",
          city: "Paris",
          description: "Histoire complète de l'Ukraine des origines à nos jours.",
          isbn: "978-2-123456-79-6",
          photo: "/books/livre2.jpg",
          owner: {
            id: 3,
            name: "Pierre Martin",
            rating: 4.2
          },
          condition: "BON",
          createdAt: new Date().toISOString()
        },
        {
          id: 3,
          title: "Les Contes Ukrainiens",
          author: "Ivan Franko",
          genre: "JEUNESSE",
          language: "ukrainien",
          ageGroup: "ENFANT",
          availability: "disponible",
          city: "Lyon",
          description: "Contes traditionnels ukrainiens pour enfants.",
          isbn: "978-2-123456-80-2",
          photo: "/books/livre3.jpg",
          owner: {
            id: 4,
            name: "Sophie Laurent",
            rating: 4.6
          },
          condition: "EXCELLENT",
          createdAt: new Date().toISOString()
        },
        {
          id: 4,
          title: "La Forteresse de Kiev",
          author: "Oles Honchar",
          genre: "ROMAN",
          language: "ukrainien",
          ageGroup: "ADULTE",
          availability: "disponible",
          city: "Marseille",
          description: "Roman historique sur la défense de Kiev.",
          isbn: "978-2-123456-81-9",
          photo: "/books/livre4.jpg",
          owner: {
            id: 5,
            name: "Jean Dupont",
            rating: 4.4
          },
          condition: "BON",
          createdAt: new Date().toISOString()
        },
        {
          id: 5,
          title: "Poèmes de la Liberté",
          author: "Lesya Ukrainka",
          genre: "POESIE",
          language: "ukrainien",
          ageGroup: "ADULTE",
          availability: "disponible",
          city: "Nancy",
          description: "Poèmes engagés pour la liberté ukrainienne.",
          isbn: "978-2-123456-82-6",
          photo: "/books/livre5.jpg",
          owner: {
            id: 6,
            name: "Anne Moreau",
            rating: 4.7
          },
          condition: "EXCELLENT",
          createdAt: new Date().toISOString()
        },
        {
          id: 6,
          title: "L'Art de la Broderie Ukrainienne",
          author: "Maria Prymachenko",
          genre: "ESSAI",
          language: "français",
          ageGroup: "ADULTE",
          availability: "disponible",
          city: "Paris",
          description: "Guide complet de la broderie traditionnelle ukrainienne.",
          isbn: "978-2-123456-83-3",
          photo: "/books/livre6.jpg",
          owner: {
            id: 7,
            name: "Claire Bernard",
            rating: 4.3
          },
          condition: "BON",
          createdAt: new Date().toISOString()
        }
      ]
      
      books.value = mockBooks
      return mockBooks
    } catch (error) {
      console.error('Erreur lors du chargement des livres:', error)
      return []
    } finally {
      isLoading.value = false
    }
  }

  const addToFavorites = (book) => {
    if (!favorites.value.find(f => f.id === book.id)) {
      favorites.value.push(book)
      localStorage.setItem('favorites', JSON.stringify(favorites.value))
    }
  }

  const removeFromFavorites = (bookId) => {
    favorites.value = favorites.value.filter(f => f.id !== bookId)
    localStorage.setItem('favorites', JSON.stringify(favorites.value))
  }

  const isFavorite = (bookId) => {
    return favorites.value.some(f => f.id === bookId)
  }

  const addBook = async (bookData) => {
    try {
      isLoading.value = true
      
      // Simulation d'une API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const newBook = {
        id: Date.now(),
        title: bookData.title,
        author: bookData.author,
        genre: bookData.genre,
        language: bookData.language,
        ageGroup: bookData.ageGroup,
        availability: "disponible",
        city: user.value?.city || "Non spécifié",
        description: bookData.description || "",
        isbn: bookData.isbn || "",
        photo: bookData.photo || "/books/default.jpg",
        owner: {
          id: user.value?.id || 0,
          name: user.value?.name || "Anonyme",
          rating: user.value?.rating || 0
        },
        condition: bookData.condition || "BON",
        createdAt: new Date().toISOString()
      }
      
      books.value.unshift(newBook)
      return { success: true, book: newBook }
    } catch (error) {
      console.error('Erreur lors de l\'ajout du livre:', error)
      return { success: false, error: 'Erreur lors de l\'ajout du livre' }
    } finally {
      isLoading.value = false
    }
  }

  const sendMessage = async (recipientId, content) => {
    try {
      const message = {
        id: Date.now(),
        senderId: user.value?.id || 0,
        recipientId,
        content,
        read: false,
        createdAt: new Date().toISOString()
      }
      
      messages.value.push(message)
      return { success: true, message }
    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error)
      return { success: false, error: 'Erreur lors de l\'envoi du message' }
    }
  }

  const addNotification = (notification) => {
    const newNotification = {
      id: Date.now(),
      ...notification,
      createdAt: new Date().toISOString()
    }
    
    notifications.value.unshift(newNotification)
  }

  const markNotificationAsRead = (notificationId) => {
    const notification = notifications.value.find(n => n.id === notificationId)
    if (notification) {
      notification.read = true
    }
  }

  const markMessageAsRead = (messageId) => {
    const message = messages.value.find(m => m.id === messageId)
    if (message) {
      message.read = true
    }
  }

  // Initialisation
  const initialize = () => {
    // Restaurer l'utilisateur depuis localStorage
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      user.value = JSON.parse(savedUser)
    }
    
    // Restaurer les favoris depuis localStorage
    const savedFavorites = localStorage.getItem('favorites')
    if (savedFavorites) {
      favorites.value = JSON.parse(savedFavorites)
    }
    
    // Écouter les changements de connectivité
    window.addEventListener('online', () => {
      isOnline.value = true
    })
    
    window.addEventListener('offline', () => {
      isOnline.value = false
    })
  }

  return {
    // État
    user,
    books,
    favorites,
    messages,
    notifications,
    isLoading,
    isOnline,
    
    // Computed
    isAuthenticated,
    userRole,
    totalBooks,
    totalFavorites,
    unreadMessages,
    unreadNotifications,
    totalUsers,
    totalExchanges,
    booksByGenre,
    booksByLanguage,
    recentBooks,
    popularBooks,
    
    // Actions
    login,
    logout,
    register,
    loadBooks,
    addToFavorites,
    removeFromFavorites,
    isFavorite,
    addBook,
    sendMessage,
    addNotification,
    markNotificationAsRead,
    markMessageAsRead,
    initialize
  }
}) 