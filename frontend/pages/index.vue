<template>
  <div class="home-page">
    <img src="/shipping-converter-tool-icon.png" alt="Shipping Converter" class="big-icon">
    <h1>Shipping Converter</h1>
    <div class="button-container">
      <NuxtLink to="/processor/unictron" class="processor-button">詠業</NuxtLink>
      <NuxtLink to="/processor/unictron_2" class="processor-button">詠業2</NuxtLink>
      <NuxtLink to="/processor/dtj_h" class="processor-button">DTJ 宏美</NuxtLink>
      <NuxtLink to="/processor/yong_laing" class="processor-button">詠聯</NuxtLink>
      <NuxtLink to="/processor/yong_laing_desc" class="processor-button">詠聯-敘述</NuxtLink>
      <NuxtLink to="/processor/vli" class="processor-button">威鋒</NuxtLink>
      <NuxtLink to="/processor/asecl" class="processor-button">日月光</NuxtLink>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
}

.big-icon {
  width: 200px;
  height: 200px;
  margin-bottom: 2rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 3rem;
  color: #333;
}

.button-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  max-width: 800px;
  width: 100%;
}

.processor-button {
  padding: 1.5rem 2rem;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  transition: all 0.3s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.processor-button:hover {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
</style>
