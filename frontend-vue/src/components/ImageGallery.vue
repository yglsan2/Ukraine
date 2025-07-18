<template>
  <div class="image-gallery-container">
    <div class="gallery-header">
      <h3 class="gallery-title">{{ title }}</h3>
      <p class="gallery-subtitle">{{ subtitle }}</p>
    </div>
    
    <!-- Navigation -->
    <div class="gallery-nav">
      <button 
        @click="previousSlide"
        class="nav-btn prev-btn"
        :disabled="currentIndex === 0"
      >
        ←
      </button>
      
      <div class="gallery-indicators">
        <button
          v-for="(image, index) in images"
          :key="index"
          @click="goToSlide(index)"
          :class="[
            'indicator-btn',
            { 'active': index === currentIndex }
          ]"
        ></button>
      </div>
      
      <button 
        @click="nextSlide"
        class="nav-btn next-btn"
        :disabled="currentIndex === images.length - 1"
      >
        →
      </button>
    </div>
    
    <!-- Carrousel principal -->
    <div class="gallery-main">
      <div class="gallery-track" :style="trackStyle">
        <div
          v-for="(image, index) in images"
          :key="index"
          class="gallery-slide"
          @click="openLightbox(index)"
        >
          <div class="slide-image">
            <img :src="image.src" :alt="image.alt" class="image">
            <div class="slide-overlay">
              <div class="slide-content">
                <h4 class="slide-title">{{ image.title }}</h4>
                <p class="slide-description">{{ image.description }}</p>
                <button class="view-btn">Voir plus</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Miniatures -->
    <div class="gallery-thumbnails">
      <div class="thumbnails-track" :style="thumbnailsStyle">
        <div
          v-for="(image, index) in images"
          :key="index"
          class="thumbnail"
          :class="{ 'active': index === currentIndex }"
          @click="goToSlide(index)"
        >
          <img :src="image.src" :alt="image.alt" class="thumbnail-image">
        </div>
      </div>
    </div>
    
    <!-- Lightbox -->
    <div v-if="lightboxOpen" class="lightbox" @click="closeLightbox">
      <div class="lightbox-content" @click.stop>
        <button @click="closeLightbox" class="lightbox-close">×</button>
        
        <div class="lightbox-main">
          <button 
            @click="previousLightboxSlide"
            class="lightbox-nav prev"
            :disabled="lightboxIndex === 0"
          >
            ←
          </button>
          
          <div class="lightbox-image-container">
            <img 
              :src="images[lightboxIndex].src" 
              :alt="images[lightboxIndex].alt" 
              class="lightbox-image"
            >
            <div class="lightbox-info">
              <h3 class="lightbox-title">{{ images[lightboxIndex].title }}</h3>
              <p class="lightbox-description">{{ images[lightboxIndex].description }}</p>
            </div>
          </div>
          
          <button 
            @click="nextLightboxSlide"
            class="lightbox-nav next"
            :disabled="lightboxIndex === images.length - 1"
          >
            →
          </button>
        </div>
        
        <div class="lightbox-thumbnails">
          <div
            v-for="(image, index) in images"
            :key="index"
            class="lightbox-thumbnail"
            :class="{ 'active': index === lightboxIndex }"
            @click="lightboxIndex = index"
          >
            <img :src="image.src" :alt="image.alt" class="lightbox-thumbnail-image">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    default: () => []
  },
  title: {
    type: String,
    default: 'Galerie'
  },
  subtitle: {
    type: String,
    default: 'Découvrez nos plus belles images'
  },
  autoplay: {
    type: Boolean,
    default: true
  },
  autoplayInterval: {
    type: Number,
    default: 5000
  }
})

const currentIndex = ref(0)
const lightboxOpen = ref(false)
const lightboxIndex = ref(0)
let autoplayTimer = null

const trackStyle = computed(() => ({
  transform: `translateX(-${currentIndex.value * 100}%)`
}))

const thumbnailsStyle = computed(() => {
  const offset = Math.max(0, currentIndex.value - 2)
  return {
    transform: `translateX(-${offset * 80}px)`
  }
})

function nextSlide() {
  if (currentIndex.value < props.images.length - 1) {
    currentIndex.value++
  } else {
    currentIndex.value = 0
  }
}

function previousSlide() {
  if (currentIndex.value > 0) {
    currentIndex.value--
  } else {
    currentIndex.value = props.images.length - 1
  }
}

function goToSlide(index) {
  currentIndex.value = index
}

function openLightbox(index) {
  lightboxIndex.value = index
  lightboxOpen.value = true
  stopAutoplay()
}

function closeLightbox() {
  lightboxOpen.value = false
  if (props.autoplay) {
    startAutoplay()
  }
}

function nextLightboxSlide() {
  if (lightboxIndex.value < props.images.length - 1) {
    lightboxIndex.value++
  } else {
    lightboxIndex.value = 0
  }
}

function previousLightboxSlide() {
  if (lightboxIndex.value > 0) {
    lightboxIndex.value--
  } else {
    lightboxIndex.value = props.images.length - 1
  }
}

function startAutoplay() {
  if (props.autoplay && !autoplayTimer) {
    autoplayTimer = setInterval(() => {
      nextSlide()
    }, props.autoplayInterval)
  }
}

function stopAutoplay() {
  if (autoplayTimer) {
    clearInterval(autoplayTimer)
    autoplayTimer = null
  }
}

// Gestion des touches clavier
function handleKeydown(event) {
  if (lightboxOpen.value) {
    switch (event.key) {
      case 'Escape':
        closeLightbox()
        break
      case 'ArrowLeft':
        previousLightboxSlide()
        break
      case 'ArrowRight':
        nextLightboxSlide()
        break
    }
  } else {
    switch (event.key) {
      case 'ArrowLeft':
        previousSlide()
        break
      case 'ArrowRight':
        nextSlide()
        break
    }
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
  startAutoplay()
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  stopAutoplay()
})
</script>

<style scoped>
.image-gallery-container {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.gallery-header {
  text-align: center;
  margin-bottom: 24px;
}

.gallery-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e3c72;
  margin-bottom: 8px;
}

.gallery-subtitle {
  color: #6b7280;
  font-size: 16px;
}

.gallery-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.nav-btn {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 18px;
  color: #374151;
}

.nav-btn:hover:not(:disabled) {
  background: #0056b3;
  color: white;
  border-color: #0056b3;
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.gallery-indicators {
  display: flex;
  gap: 8px;
}

.indicator-btn {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e2e8f0;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.indicator-btn.active {
  background: #0056b3;
  transform: scale(1.2);
}

.gallery-main {
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  margin-bottom: 20px;
}

.gallery-track {
  display: flex;
  transition: transform 0.5s ease;
}

.gallery-slide {
  flex: 0 0 100%;
  cursor: pointer;
}

.slide-image {
  position: relative;
  aspect-ratio: 16/9;
  overflow: hidden;
}

.image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.gallery-slide:hover .image {
  transform: scale(1.05);
}

.slide-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  display: flex;
  align-items: flex-end;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.gallery-slide:hover .slide-overlay {
  opacity: 1;
}

.slide-content {
  padding: 24px;
  color: white;
}

.slide-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
}

.slide-description {
  font-size: 14px;
  margin-bottom: 12px;
  opacity: 0.9;
}

.view-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.gallery-thumbnails {
  overflow: hidden;
}

.thumbnails-track {
  display: flex;
  gap: 12px;
  transition: transform 0.3s ease;
}

.thumbnail {
  flex: 0 0 80px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s ease;
}

.thumbnail.active {
  border-color: #0056b3;
}

.thumbnail:hover {
  transform: scale(1.05);
}

.thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Lightbox */
.lightbox {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
}

.lightbox-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  background: white;
  border-radius: 12px;
  overflow: hidden;
}

.lightbox-close {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 24px;
  cursor: pointer;
  z-index: 10;
  transition: all 0.2s ease;
}

.lightbox-close:hover {
  background: rgba(0, 0, 0, 0.7);
}

.lightbox-main {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
}

.lightbox-nav {
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.lightbox-nav:hover:not(:disabled) {
  background: rgba(0, 0, 0, 0.7);
}

.lightbox-nav:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.lightbox-image-container {
  flex: 1;
  text-align: center;
}

.lightbox-image {
  max-width: 100%;
  max-height: 60vh;
  object-fit: contain;
  border-radius: 8px;
}

.lightbox-info {
  margin-top: 16px;
  text-align: center;
}

.lightbox-title {
  font-size: 20px;
  font-weight: 600;
  color: #1e3c72;
  margin-bottom: 8px;
}

.lightbox-description {
  color: #6b7280;
  font-size: 14px;
}

.lightbox-thumbnails {
  display: flex;
  gap: 8px;
  padding: 16px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}

.lightbox-thumbnail {
  flex: 0 0 60px;
  height: 45px;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s ease;
}

.lightbox-thumbnail.active {
  border-color: #0056b3;
}

.lightbox-thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@media (max-width: 768px) {
  .gallery-nav {
    flex-direction: column;
    gap: 16px;
  }
  
  .lightbox-main {
    flex-direction: column;
    gap: 16px;
  }
  
  .lightbox-nav {
    width: 40px;
    height: 40px;
    font-size: 16px;
  }
}
</style> 
  <div class="image-gallery-container">
    <div class="gallery-header">
      <h3 class="gallery-title">{{ title }}</h3>
      <p class="gallery-subtitle">{{ subtitle }}</p>
    </div>
    
    <!-- Navigation -->
    <div class="gallery-nav">
      <button 
        @click="previousSlide"
        class="nav-btn prev-btn"
        :disabled="currentIndex === 0"
      >
        ←
      </button>
      
      <div class="gallery-indicators">
        <button
          v-for="(image, index) in images"
          :key="index"
          @click="goToSlide(index)"
          :class="[
            'indicator-btn',
            { 'active': index === currentIndex }
          ]"
        ></button>
      </div>
      
      <button 
        @click="nextSlide"
        class="nav-btn next-btn"
        :disabled="currentIndex === images.length - 1"
      >
        →
      </button>
    </div>
    
    <!-- Carrousel principal -->
    <div class="gallery-main">
      <div class="gallery-track" :style="trackStyle">
        <div
          v-for="(image, index) in images"
          :key="index"
          class="gallery-slide"
          @click="openLightbox(index)"
        >
          <div class="slide-image">
            <img :src="image.src" :alt="image.alt" class="image">
            <div class="slide-overlay">
              <div class="slide-content">
                <h4 class="slide-title">{{ image.title }}</h4>
                <p class="slide-description">{{ image.description }}</p>
                <button class="view-btn">Voir plus</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Miniatures -->
    <div class="gallery-thumbnails">
      <div class="thumbnails-track" :style="thumbnailsStyle">
        <div
          v-for="(image, index) in images"
          :key="index"
          class="thumbnail"
          :class="{ 'active': index === currentIndex }"
          @click="goToSlide(index)"
        >
          <img :src="image.src" :alt="image.alt" class="thumbnail-image">
        </div>
      </div>
    </div>
    
    <!-- Lightbox -->
    <div v-if="lightboxOpen" class="lightbox" @click="closeLightbox">
      <div class="lightbox-content" @click.stop>
        <button @click="closeLightbox" class="lightbox-close">×</button>
        
        <div class="lightbox-main">
          <button 
            @click="previousLightboxSlide"
            class="lightbox-nav prev"
            :disabled="lightboxIndex === 0"
          >
            ←
          </button>
          
          <div class="lightbox-image-container">
            <img 
              :src="images[lightboxIndex].src" 
              :alt="images[lightboxIndex].alt" 
              class="lightbox-image"
            >
            <div class="lightbox-info">
              <h3 class="lightbox-title">{{ images[lightboxIndex].title }}</h3>
              <p class="lightbox-description">{{ images[lightboxIndex].description }}</p>
            </div>
          </div>
          
          <button 
            @click="nextLightboxSlide"
            class="lightbox-nav next"
            :disabled="lightboxIndex === images.length - 1"
          >
            →
          </button>
        </div>
        
        <div class="lightbox-thumbnails">
          <div
            v-for="(image, index) in images"
            :key="index"
            class="lightbox-thumbnail"
            :class="{ 'active': index === lightboxIndex }"
            @click="lightboxIndex = index"
          >
            <img :src="image.src" :alt="image.alt" class="lightbox-thumbnail-image">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    default: () => []
  },
  title: {
    type: String,
    default: 'Galerie'
  },
  subtitle: {
    type: String,
    default: 'Découvrez nos plus belles images'
  },
  autoplay: {
    type: Boolean,
    default: true
  },
  autoplayInterval: {
    type: Number,
    default: 5000
  }
})

const currentIndex = ref(0)
const lightboxOpen = ref(false)
const lightboxIndex = ref(0)
let autoplayTimer = null

const trackStyle = computed(() => ({
  transform: `translateX(-${currentIndex.value * 100}%)`
}))

const thumbnailsStyle = computed(() => {
  const offset = Math.max(0, currentIndex.value - 2)
  return {
    transform: `translateX(-${offset * 80}px)`
  }
})

function nextSlide() {
  if (currentIndex.value < props.images.length - 1) {
    currentIndex.value++
  } else {
    currentIndex.value = 0
  }
}

function previousSlide() {
  if (currentIndex.value > 0) {
    currentIndex.value--
  } else {
    currentIndex.value = props.images.length - 1
  }
}

function goToSlide(index) {
  currentIndex.value = index
}

function openLightbox(index) {
  lightboxIndex.value = index
  lightboxOpen.value = true
  stopAutoplay()
}

function closeLightbox() {
  lightboxOpen.value = false
  if (props.autoplay) {
    startAutoplay()
  }
}

function nextLightboxSlide() {
  if (lightboxIndex.value < props.images.length - 1) {
    lightboxIndex.value++
  } else {
    lightboxIndex.value = 0
  }
}

function previousLightboxSlide() {
  if (lightboxIndex.value > 0) {
    lightboxIndex.value--
  } else {
    lightboxIndex.value = props.images.length - 1
  }
}

function startAutoplay() {
  if (props.autoplay && !autoplayTimer) {
    autoplayTimer = setInterval(() => {
      nextSlide()
    }, props.autoplayInterval)
  }
}

function stopAutoplay() {
  if (autoplayTimer) {
    clearInterval(autoplayTimer)
    autoplayTimer = null
  }
}

// Gestion des touches clavier
function handleKeydown(event) {
  if (lightboxOpen.value) {
    switch (event.key) {
      case 'Escape':
        closeLightbox()
        break
      case 'ArrowLeft':
        previousLightboxSlide()
        break
      case 'ArrowRight':
        nextLightboxSlide()
        break
    }
  } else {
    switch (event.key) {
      case 'ArrowLeft':
        previousSlide()
        break
      case 'ArrowRight':
        nextSlide()
        break
    }
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
  startAutoplay()
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  stopAutoplay()
})
</script>

<style scoped>
.image-gallery-container {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.gallery-header {
  text-align: center;
  margin-bottom: 24px;
}

.gallery-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e3c72;
  margin-bottom: 8px;
}

.gallery-subtitle {
  color: #6b7280;
  font-size: 16px;
}

.gallery-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.nav-btn {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 18px;
  color: #374151;
}

.nav-btn:hover:not(:disabled) {
  background: #0056b3;
  color: white;
  border-color: #0056b3;
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.gallery-indicators {
  display: flex;
  gap: 8px;
}

.indicator-btn {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e2e8f0;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.indicator-btn.active {
  background: #0056b3;
  transform: scale(1.2);
}

.gallery-main {
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  margin-bottom: 20px;
}

.gallery-track {
  display: flex;
  transition: transform 0.5s ease;
}

.gallery-slide {
  flex: 0 0 100%;
  cursor: pointer;
}

.slide-image {
  position: relative;
  aspect-ratio: 16/9;
  overflow: hidden;
}

.image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.gallery-slide:hover .image {
  transform: scale(1.05);
}

.slide-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  display: flex;
  align-items: flex-end;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.gallery-slide:hover .slide-overlay {
  opacity: 1;
}

.slide-content {
  padding: 24px;
  color: white;
}

.slide-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
}

.slide-description {
  font-size: 14px;
  margin-bottom: 12px;
  opacity: 0.9;
}

.view-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.gallery-thumbnails {
  overflow: hidden;
}

.thumbnails-track {
  display: flex;
  gap: 12px;
  transition: transform 0.3s ease;
}

.thumbnail {
  flex: 0 0 80px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s ease;
}

.thumbnail.active {
  border-color: #0056b3;
}

.thumbnail:hover {
  transform: scale(1.05);
}

.thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Lightbox */
.lightbox {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
}

.lightbox-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  background: white;
  border-radius: 12px;
  overflow: hidden;
}

.lightbox-close {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 24px;
  cursor: pointer;
  z-index: 10;
  transition: all 0.2s ease;
}

.lightbox-close:hover {
  background: rgba(0, 0, 0, 0.7);
}

.lightbox-main {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
}

.lightbox-nav {
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.lightbox-nav:hover:not(:disabled) {
  background: rgba(0, 0, 0, 0.7);
}

.lightbox-nav:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.lightbox-image-container {
  flex: 1;
  text-align: center;
}

.lightbox-image {
  max-width: 100%;
  max-height: 60vh;
  object-fit: contain;
  border-radius: 8px;
}

.lightbox-info {
  margin-top: 16px;
  text-align: center;
}

.lightbox-title {
  font-size: 20px;
  font-weight: 600;
  color: #1e3c72;
  margin-bottom: 8px;
}

.lightbox-description {
  color: #6b7280;
  font-size: 14px;
}

.lightbox-thumbnails {
  display: flex;
  gap: 8px;
  padding: 16px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}

.lightbox-thumbnail {
  flex: 0 0 60px;
  height: 45px;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s ease;
}

.lightbox-thumbnail.active {
  border-color: #0056b3;
}

.lightbox-thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@media (max-width: 768px) {
  .gallery-nav {
    flex-direction: column;
    gap: 16px;
  }
  
  .lightbox-main {
    flex-direction: column;
    gap: 16px;
  }
  
  .lightbox-nav {
    width: 40px;
    height: 40px;
    font-size: 16px;
  }
}
</style> 