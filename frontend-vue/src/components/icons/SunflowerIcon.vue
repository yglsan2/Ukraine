<template>
  <div class="sunflower-container" :class="sizeClass" :style="customStyle">
    <img 
      :src="sunflowerSrc" 
      :alt="alt" 
      class="sunflower-image"
      :class="{ 'animated': animated }"
    />
  </div>
</template>

<script>
export default {
  name: 'SunflowerIcon',
  props: {
    size: {
      type: String,
      default: 'medium',
      validator: value => ['small', 'medium', 'large', 'xlarge'].includes(value)
    },
    animated: {
      type: Boolean,
      default: true
    },
    alt: {
      type: String,
      default: 'Tournesol'
    },
    variant: {
      type: String,
      default: 'full',
      validator: value => ['full', 'icon'].includes(value)
    }
  },
  computed: {
    sizeClass() {
      return `sunflower-${this.size}`
    },
    sunflowerSrc() {
      return this.variant === 'full' 
        ? '/images/sunflower-new.png' 
        : '/images/sunflower-new.png'
    },
    customStyle() {
      const sizes = {
        small: { width: '30px', height: '30px' },
        medium: { width: '50px', height: '50px' },
        large: { width: '100px', height: '100px' },
        xlarge: { width: '150px', height: '150px' }
      }
      return sizes[this.size] || sizes.medium
    }
  }
}
</script>

<style scoped>
.sunflower-container {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.sunflower-image {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
  transition: all 0.3s ease;
}

.sunflower-container:hover .sunflower-image {
  filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.4));
  transform: scale(1.05);
}

.sunflower-image.animated {
  animation: sunflowerRotate 30s linear infinite;
}

@keyframes sunflowerRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Tailles spécifiques */
.sunflower-small .sunflower-image {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.sunflower-large .sunflower-image,
.sunflower-xlarge .sunflower-image {
  filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.3));
}
</style> 