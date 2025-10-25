<template>
  <div class="file-upload">
    <div 
      class="dropzone"
      :class="{ 'dragover': isDragOver, 'uploading': isUploading }"
      @drop.prevent="handleDrop"
      @dragover.prevent="isDragOver = true"
      @dragleave.prevent="isDragOver = false"
      @click="triggerFileInput"
    >
      <input
        ref="fileInput"
        type="file"
        accept=".xls,.xlsx,.xlsm"
        @change="handleFileSelect"
        style="display: none"
      />
      
      <div v-if="!isUploading" class="dropzone-content">
        <svg class="upload-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        <p class="dropzone-text">
          <span class="highlight">Click to upload</span> or drag and drop
        </p>
        <p class="dropzone-subtext">Excel files (.xls, .xlsx, .xlsm)</p>
        <p v-if="selectedFile" class="selected-file">Selected: {{ selectedFile.name }}</p>
      </div>
      
      <div v-else class="uploading-content">
        <div class="spinner"></div>
        <p>Processing...</p>
      </div>
    </div>

    <button 
      v-if="selectedFile && !isUploading"
      @click="uploadFile"
      class="upload-button"
    >
      Upload and Process
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  processorType: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['upload-success', 'upload-error'])

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const fileInput = ref(null)
const selectedFile = ref(null)
const isDragOver = ref(false)
const isUploading = ref(false)

const triggerFileInput = () => {
  if (!isUploading.value) {
    fileInput.value.click()
  }
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
  }
}

const handleDrop = (event) => {
  isDragOver.value = false
  const file = event.dataTransfer.files[0]
  if (file) {
    selectedFile.value = file
  }
}

const uploadFile = async () => {
  if (!selectedFile.value) return

  isUploading.value = true

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try {
    const response = await fetch(`${apiBase}/api/process/${props.processorType}`, {
      method: 'POST',
      body: formData
    })

    const data = await response.json()

    if (response.ok) {
      emit('upload-success', {
        message: data.message,
        download_url: `${apiBase}${data.download_url}`
      })
      selectedFile.value = null
    } else {
      emit('upload-error', data.detail || 'Upload failed')
    }
  } catch (error) {
    emit('upload-error', 'An error occurred during upload')
  } finally {
    isUploading.value = false
  }
}
</script>

<style scoped>
.file-upload {
  width: 100%;
}

.dropzone {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 3rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background-color: #fafafa;
}

.dropzone:hover {
  border-color: #4CAF50;
  background-color: #f0f8f0;
}

.dropzone.dragover {
  border-color: #4CAF50;
  background-color: #e8f5e9;
}

.dropzone.uploading {
  cursor: not-allowed;
  opacity: 0.7;
}

.dropzone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.upload-icon {
  width: 64px;
  height: 64px;
  color: #666;
}

.dropzone-text {
  font-size: 1.1rem;
  color: #333;
}

.highlight {
  color: #4CAF50;
  font-weight: bold;
}

.dropzone-subtext {
  font-size: 0.9rem;
  color: #666;
}

.selected-file {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #e3f2fd;
  border-radius: 4px;
  color: #1976d2;
  font-weight: 500;
}

.uploading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.upload-button {
  margin-top: 1.5rem;
  padding: 1rem 2rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
  width: 100%;
}

.upload-button:hover {
  background-color: #45a049;
}
</style>
