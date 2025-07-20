<template>
  <div class="realistic-book" :style="bookStyle">
    <img
      :src="bookImageSrc"
      :alt="`Livre ${index + 1}`"
      @load="onImageLoad"
      @error="onImageError"
      class="book-image"
    />
    <div v-if="showFallback" class="book-fallback">
      {{ book.emoji }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  book: { type: Object, required: true },
  style: { type: Object, default: () => ({}) },
  index: { type: Number, default: 0 },
})

const showFallback = ref(false)
const imageLoaded = ref(false)

console.log('🔧 RealisticBook component created with props:', props)

const bookImages = [
  '/images/books/realistic/bookRed1.jpg',
  '/images/books/realistic/bookBlue1.png',
  '/images/books/realistic/bookBrown1.png',
  '/images/books/realistic/bookBlack1.png',
  '/images/books/realistic/bookWhite1.png',
  '/images/books/realistic/bookWood1.png',
  '/images/books/realistic/bookSet1.png',
  '/images/books/realistic/bookStack1.png',
]

console.log('📚 Available book images:', bookImages)

const bookImageSrc = computed(() => {
  const randomIndex = Math.floor(Math.random() * bookImages.length)
  const selectedImage = bookImages[randomIndex]
  console.log(`🎲 Selected image ${randomIndex}:`, selectedImage)
  return selectedImage
})

const bookStyle = computed(() => ({
  ...props.style,
  opacity: 0,
  transform: `${props.style.transform || ''} translateY(20px)`,
  transition: 'opacity 0.8s ease, transform 0.8s ease',
  width: '80px',
  height: '100px',
}))

const onImageLoad = (event) => {
  console.log('✅ Image chargée avec succès:', event.target.src)
  imageLoaded.value = true
  showFallback.value = false
}

const onImageError = (event) => {
  console.log('❌ Erreur de chargement pour:', event.target.src)
  showFallback.value = true
  imageLoaded.value = false
}

onMounted(() => {
  console.log('🚀 RealisticBook mounted, index:', props.index)
  setTimeout(() => {
    const bookElement = document.querySelector('.realistic-book')
    if (bookElement) {
      console.log('🎬 Starting animation for book')
      bookElement.style.opacity = '1'
      bookElement.style.transform = bookElement.style.transform.replace(' translateY(20px)', '')
    }
  }, 100)
})
</script>

<style scoped>
.realistic-book {
  position: absolute;
  z-index: 10;
  cursor: pointer;
  transition: all 0.3s ease;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
  width: 80px;
  height: 100px;
}

.realistic-book:hover {
  transform: scale(1.1) rotate(5deg) !important;
  filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.4));
  z-index: 20;
}

.book-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 2px solid red;
}

.book-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 100px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 8px;
  font-size: 2rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border: 2px solid #e0e0e0;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px) rotate(var(--rotation));
  }
  50% {
    transform: translateY(-10px) rotate(var(--rotation));
  }
}

.realistic-book {
  animation: float 3s ease-in-out infinite;
  animation-delay: var(--delay, 0s);
}

@media (max-width: 768px) {
  .realistic-book {
    transform: scale(0.7) !important;
  }
  .book-fallback {
    width: 60px;
    height: 80px;
    font-size: 1.5rem;
  }
}
</style>
