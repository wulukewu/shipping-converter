export default defineNuxtConfig({
  devtools: { enabled: true },
  
  app: {
    head: {
      title: 'Shipping Converter',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Shipping data converter tool' }
      ],
      link: [
        { rel: 'icon', type: 'image/png', href: '/shipping-converter-tool-icon.png' }
      ]
    }
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
    }
  },

  css: ['~/assets/css/main.css'],

  compatibilityDate: '2024-10-25'
})
