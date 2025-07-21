<template>
  <div class="ragtime-chatbot">
    <!-- Bouton flottant pour ouvrir le chatbot -->
    <div 
      v-if="!isOpen" 
      class="chatbot-toggle"
      @click="openChatbot"
      :class="{ 'pulse': hasNewMessage }"
    >
      <div class="toggle-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
      </div>
      <div class="toggle-badge" v-if="unreadCount > 0">{{ unreadCount }}</div>
    </div>

    <!-- Interface du chatbot -->
    <div v-if="isOpen" class="chatbot-container" :class="{ 'minimized': isMinimized }">
      <!-- Header -->
      <div class="chatbot-header">
        <div class="header-content">
          <div class="status-indicator" :class="{ 'online': isApiOnline }"></div>
          <h3>🤖 RagTime Assistant</h3>
          <p>Découvrez notre bibliothèque ukrainienne</p>
        </div>
        <div class="header-actions">
          <button class="minimize-btn" @click="toggleMinimize">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
          </button>
          <button class="close-btn" @click="closeChatbot">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>

      <!-- Messages -->
      <div v-if="!isMinimized" class="chat-messages" ref="messagesContainer">
        <div class="welcome-message" v-if="messages.length === 0">
          <div class="welcome-icon">👋</div>
          <h4>Bonjour !</h4>
          <p>Je suis RagTime, votre assistant pour découvrir la littérature ukrainienne.</p>
          <p>Posez-moi vos questions sur nos livres !</p>
        </div>

        <div 
          v-for="(message, index) in messages" 
          :key="index"
          class="message"
          :class="message.sender"
        >
          <div class="message-avatar">
            {{ message.sender === 'user' ? '👤' : '🤖' }}
          </div>
          <div class="message-content">
            <div class="message-text" v-html="formatMessage(message.content)"></div>
            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          </div>
        </div>

        <!-- Indicateur de frappe -->
        <div v-if="isTyping" class="typing-indicator">
          <div class="typing-dots">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div v-if="!isMinimized" class="chat-input-container">
        <div class="input-wrapper">
          <input 
            v-model="currentMessage"
            @keyup.enter="sendMessage"
            @keyup.ctrl.enter="sendMessage"
            type="text"
            class="chat-input"
            placeholder="Posez votre question..."
            :disabled="isTyping"
            maxlength="500"
          />
          <button 
            @click="sendMessage"
            class="send-button"
            :disabled="!currentMessage.trim() || isTyping"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22,2 15,22 11,13 2,9"></polygon>
            </svg>
          </button>
        </div>
        
        <!-- Toggle IA -->
        <div class="ai-toggle">
          <span>IA enrichie</span>
          <div 
            class="toggle-switch"
            :class="{ 'active': aiEnabled }"
            @click="toggleAI"
          >
            <div class="toggle-slider"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RagTimeChatbot',
  data() {
    return {
      isOpen: false,
      isMinimized: false,
      isTyping: false,
      isApiOnline: false,
      aiEnabled: true,
      currentMessage: '',
      messages: [],
      unreadCount: 0,
      hasNewMessage: false,
      apiUrl: 'http://localhost:5000/api'
    }
  },
  mounted() {
    this.checkApiHealth();
    // Vérifier la santé de l'API toutes les 30 secondes
    setInterval(this.checkApiHealth, 30000);
  },
  methods: {
    async checkApiHealth() {
      try {
        const response = await fetch(`${this.apiUrl}/health`);
        this.isApiOnline = response.ok;
      } catch (error) {
        this.isApiOnline = false;
        console.error('Erreur connexion API:', error);
      }
    },

    openChatbot() {
      this.isOpen = true;
      this.isMinimized = false;
      this.unreadCount = 0;
      this.hasNewMessage = false;
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    },

    closeChatbot() {
      this.isOpen = false;
      this.isMinimized = false;
    },

    toggleMinimize() {
      this.isMinimized = !this.isMinimized;
      if (!this.isMinimized) {
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },

    toggleAI() {
      this.aiEnabled = !this.aiEnabled;
    },

    async sendMessage() {
      const message = this.currentMessage.trim();
      if (!message || this.isTyping) return;

      // Ajouter le message utilisateur
      this.addMessage(message, 'user');
      this.currentMessage = '';
      this.isTyping = true;

      try {
        const response = await this.callRagTimeAPI(message);
        this.addBotResponse(response);
      } catch (error) {
        this.addMessage('Désolé, une erreur s\'est produite. Veuillez réessayer.', 'bot');
        console.error('Erreur API:', error);
      }

      this.isTyping = false;
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    },

    async callRagTimeAPI(query) {
      const response = await fetch(`${this.apiUrl}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          useAI: this.aiEnabled,
          maxResults: 5
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      return await response.json();
    },

    addMessage(content, sender) {
      this.messages.push({
        content,
        sender,
        timestamp: new Date()
      });

      // Incrémenter le compteur de messages non lus si le chatbot est fermé
      if (!this.isOpen && sender === 'bot') {
        this.unreadCount++;
        this.hasNewMessage = true;
      }
    },

    addBotResponse(apiResponse) {
      if (!apiResponse.success) {
        this.addMessage('Désolé, je n\'ai pas pu traiter votre demande.', 'bot');
        return;
      }

      // Ajouter la réponse principale
      if (apiResponse.response) {
        this.addMessage(apiResponse.response, 'bot');
      }

      // Ajouter les livres trouvés
      if (apiResponse.books && apiResponse.books.length > 0) {
        const booksMessage = this.formatBooksMessage(apiResponse.books);
        this.addMessage(booksMessage, 'bot');
      }

      // Ajouter les informations de timing
      if (apiResponse.timing) {
        const timingMessage = `⏱️ Réponse générée en ${apiResponse.timing.total_time.toFixed(2)}s${apiResponse.ai_used ? ' (avec IA)' : ''}`;
        this.addMessage(timingMessage, 'bot');
      }
    },

    formatBooksMessage(books) {
      let message = '<strong>📚 Livres trouvés :</strong><br><br>';
      
      books.forEach((book, index) => {
        message += `<strong>${index + 1}. ${book.title}</strong><br>`;
        if (book.author) message += `   Auteur: ${book.author}<br>`;
        if (book.genre) message += `   Genre: ${book.genre}<br>`;
        if (book.language) message += `   Langue: ${book.language}<br>`;
        if (book.score) message += `   Pertinence: ${(book.score * 100).toFixed(1)}%<br>`;
        message += '<br>';
      });

      return message;
    },

    formatMessage(content) {
      // Convertir les retours à la ligne en <br>
      return content.replace(/\n/g, '<br>');
    },

    formatTime(timestamp) {
      return timestamp.toLocaleTimeString('fr-FR', { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    },

    scrollToBottom() {
      if (this.$refs.messagesContainer) {
        this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
      }
    }
  }
}
</script>

<style scoped>
.ragtime-chatbot {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Bouton flottant */
.chatbot-toggle {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  transition: transform 0.3s, box-shadow 0.3s;
  position: relative;
}

.chatbot-toggle:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 25px rgba(0,0,0,0.2);
}

.chatbot-toggle.pulse {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.toggle-icon {
  color: white;
}

.toggle-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #e74c3c;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

/* Container du chatbot */
.chatbot-container {
  width: 350px;
  height: 500px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.3s;
}

.chatbot-container.minimized {
  height: 60px;
}

/* Header */
.chatbot-header {
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  color: white;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content {
  flex: 1;
}

.header-content h3 {
  margin: 0 0 5px 0;
  font-size: 16px;
}

.header-content p {
  margin: 0;
  font-size: 12px;
  opacity: 0.9;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e74c3c;
  margin-right: 10px;
  display: inline-block;
}

.status-indicator.online {
  background: #2ecc71;
  animation: pulse 2s infinite;
}

.header-actions {
  display: flex;
  gap: 5px;
}

.minimize-btn, .close-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 5px;
  border-radius: 5px;
  transition: background 0.3s;
}

.minimize-btn:hover, .close-btn:hover {
  background: rgba(255,255,255,0.2);
}

/* Messages */
.chat-messages {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  background: #f8f9fa;
}

.welcome-message {
  text-align: center;
  color: #666;
  padding: 20px;
}

.welcome-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.welcome-message h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.welcome-message p {
  margin: 0 0 5px 0;
  font-size: 14px;
}

.message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
}

.message.user {
  justify-content: flex-end;
}

.message.bot {
  justify-content: flex-start;
}

.message-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  margin: 0 8px;
}

.message.user .message-avatar {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.message.bot .message-avatar {
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  color: white;
}

.message-content {
  max-width: 70%;
}

.message.user .message-content {
  text-align: right;
}

.message-text {
  padding: 10px 15px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.4;
  word-wrap: break-word;
}

.message.user .message-text {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-bottom-right-radius: 5px;
}

.message.bot .message-text {
  background: white;
  color: #333;
  border: 1px solid #e9ecef;
  border-bottom-left-radius: 5px;
}

.message-time {
  font-size: 11px;
  color: #999;
  margin-top: 5px;
  text-align: right;
}

.message.user .message-time {
  text-align: right;
}

.message.bot .message-time {
  text-align: left;
}

/* Indicateur de frappe */
.typing-indicator {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
}

.typing-dots {
  display: flex;
  gap: 4px;
  padding: 10px 15px;
  background: white;
  border-radius: 18px;
  border: 1px solid #e9ecef;
  border-bottom-left-radius: 5px;
}

.typing-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #ccc;
  animation: typing 1.4s infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-8px); }
}

/* Input */
.chat-input-container {
  padding: 15px;
  background: white;
  border-top: 1px solid #e9ecef;
}

.input-wrapper {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 10px;
}

.chat-input {
  flex: 1;
  padding: 10px 15px;
  border: 2px solid #e9ecef;
  border-radius: 20px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.chat-input:focus {
  border-color: #667eea;
}

.chat-input:disabled {
  background: #f8f9fa;
  cursor: not-allowed;
}

.send-button {
  width: 35px;
  height: 35px;
  border: none;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}

.send-button:hover:not(:disabled) {
  transform: scale(1.1);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* Toggle IA */
.ai-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: #666;
}

.toggle-switch {
  position: relative;
  width: 35px;
  height: 18px;
  background: #ccc;
  border-radius: 9px;
  cursor: pointer;
  transition: background 0.3s;
}

.toggle-switch.active {
  background: #667eea;
}

.toggle-slider {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 14px;
  height: 14px;
  background: white;
  border-radius: 50%;
  transition: transform 0.3s;
}

.toggle-switch.active .toggle-slider {
  transform: translateX(17px);
}

/* Responsive */
@media (max-width: 480px) {
  .chatbot-container {
    width: calc(100vw - 40px);
    height: calc(100vh - 120px);
    position: fixed;
    top: 20px;
    left: 20px;
    right: 20px;
    bottom: 20px;
  }
  
  .chatbot-toggle {
    width: 50px;
    height: 50px;
  }
}
</style> 