<template>
  <div class="processor-page">
    <h1>{{ processorName }}</h1>
    
    <FileUpload 
      :processor-type="processorType"
      @upload-success="handleUploadSuccess"
      @upload-error="handleUploadError"
    />

    <div v-if="message" class="message" :class="messageType">
      {{ message }}
    </div>

    <div v-if="downloadUrl" class="download-section">
      <a :href="downloadUrl" class="download-button" download>
        Download Processed File
      </a>
    </div>
  </div>
</template>

<script setup>
const route = useRoute()
const processorType = route.params.id

const processorNames = {
  'unictron': '詠業',
  'unictron_2': '詠業2',
  'dtj_h': 'DTJ 宏美',
  'yong_laing': '詠聯',
  'yong_laing_desc': '詠聯-敘述',
  'vli': '威鋒',
  'asecl': '日月光'
}

const processorName = processorNames[processorType] || processorType

const message = ref('')
const messageType = ref('success')
const downloadUrl = ref('')

const handleUploadSuccess = (data) => {
  message.value = data.message
  messageType.value = 'success'
  downloadUrl.value = data.download_url
}

const handleUploadError = (error) => {
  message.value = error
  messageType.value = 'error'
  downloadUrl.value = ''
}
</script>

<style scoped>
.processor-page {
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.message {
  margin: 2rem 0;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.download-section {
  text-align: center;
  margin-top: 2rem;
}

.download-button {
  display: inline-block;
  padding: 1rem 2rem;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.download-button:hover {
  background-color: #0056b3;
}
</style>
