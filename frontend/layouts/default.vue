<template>
  <div class="app-layout">
    <nav class="navbar">
      <NuxtLink to="/" class="navbar-brand">
        <img src="/shipping-converter-tool-icon.png" alt="Logo">
      </NuxtLink>
      <div class="navbar-links">
        <NuxtLink to="/">Home</NuxtLink>
        <NuxtLink to="/processor/unictron">詠業</NuxtLink>
        <NuxtLink to="/processor/unictron_2">詠業2</NuxtLink>
        <NuxtLink to="/processor/dtj_h">DTJ 宏美</NuxtLink>
        <NuxtLink to="/processor/yong_laing">詠聯</NuxtLink>
        <NuxtLink to="/processor/yong_laing_desc">詠聯-敘述</NuxtLink>
        <NuxtLink to="/processor/vli">威鋒</NuxtLink>
        <NuxtLink to="/processor/asecl">日月光</NuxtLink>
      </div>
    </nav>
    <main class="main-content">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: #333;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar-brand img {
  height: 40px;
  width: auto;
}

.navbar-links {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.navbar-links a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.navbar-links a:hover,
.navbar-links a.router-link-active {
  background-color: #555;
}

.main-content {
  flex: 1;
  padding: 2rem;
}
</style>
