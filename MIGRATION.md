# Shipping Converter v2.0 - Migration Guide

## Overview

The Shipping Converter has been refactored from a Flask monolith to a modern architecture with:
- **Backend**: FastAPI (Python)
- **Frontend**: Nuxt 3 (Vue 3)

## What's New

### Architecture Changes

1. **Separation of Concerns**
   - Backend API (FastAPI) handles all business logic and file processing
   - Frontend (Nuxt 3) provides a modern, reactive UI
   - Clear API contract between frontend and backend

2. **Modern Tech Stack**
   - **FastAPI**: High-performance async API with automatic OpenAPI documentation
   - **Nuxt 3**: Vue 3 with Composition API, auto-imports, and file-based routing
   - **Docker**: Containerized deployment for both services

3. **Improved Developer Experience**
   - Type safety with Pydantic (backend) and TypeScript support (frontend)
   - Hot module replacement in development
   - Automatic API documentation at `/docs`
   - Better code organization and maintainability

### File Structure Comparison

#### Old Structure (Flask)
```
shipping-converter/
├── app.py                 # Monolithic Flask app
├── templates/             # Jinja2 templates
├── static/                # Static files
├── scripts/               # Processing scripts
└── requirements.txt
```

#### New Structure (FastAPI + Nuxt)
```
shipping-converter/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Configuration
│   │   ├── models/       # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utilities
│   └── requirements.txt
├── frontend/
│   ├── pages/            # Auto-routed pages
│   ├── components/       # Reusable components
│   ├── layouts/          # Layout templates
│   └── nuxt.config.ts    # Configuration
└── scripts/              # Processing scripts (shared)
```

## API Changes

### Old Flask Endpoints
```
GET  /                     -> Renders index.html
GET  /Unictron            -> Renders Unictron.html
POST /Unictron            -> Processes file
GET  /uploads/<filename>  -> Downloads file
```

### New FastAPI Endpoints
```
GET  /                           -> API info
GET  /health                     -> Health check
GET  /api/processors             -> List processors
POST /api/process/{type}         -> Process file
GET  /api/download/{filename}    -> Download file
```

## Running the Application

### Development

#### Old Way (Flask)
```bash
flask run
```

#### New Way

Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

### Production

#### Old Way
```bash
docker build -t shipping-converter .
docker run -p 5000:5000 shipping-converter
```

#### New Way
```bash
docker-compose -f docker-compose.new.yml up -d
```

## Code Migration Examples

### Request Handling

#### Old (Flask)
```python
@app.route('/Unictron', methods=['GET', 'POST'])
def upload_file_unictron():
    if request.method == 'POST':
        file = request.files['file']
        # Process file...
        return redirect(url_for('download_file'))
    return render_template('Unictron.html')
```

#### New (FastAPI)
```python
@router.post("/process/unictron")
async def process_unictron(file: UploadFile = File(...)):
    result = await process_file(file, "unictron")
    return result
```

### Frontend

#### Old (Jinja2 Template)
```html
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="file">
    <button type="submit">Upload</button>
</form>
```

#### New (Vue Component)
```vue
<template>
  <FileUpload 
    :processor-type="processorType"
    @upload-success="handleSuccess"
  />
</template>

<script setup>
const handleSuccess = (data) => {
  // Handle success
}
</script>
```

## Configuration Changes

### Old (.env)
```env
DISCORD_WEBHOOK_URL=...
DISCORD_TOKEN=...
```

### New (.env)
```env
# Backend uses same variables
DISCORD_WEBHOOK_URL=...

# Frontend adds
NUXT_PUBLIC_API_BASE=http://localhost:8000
```

## Benefits of New Architecture

1. **Performance**
   - FastAPI is significantly faster than Flask
   - Nuxt provides optimal frontend performance with SSR/SSG
   - Async operations for better concurrency

2. **Developer Experience**
   - Hot reload in both frontend and backend
   - Automatic API documentation
   - Better error messages and debugging
   - Type safety

3. **Scalability**
   - Frontend and backend can scale independently
   - Easy to add new processors
   - Clear API boundaries

4. **Modern UX**
   - Drag-and-drop file upload
   - Real-time feedback
   - Responsive design
   - No page reloads

5. **Maintainability**
   - Clearer code organization
   - Separation of concerns
   - Easier to test
   - Better code reusability

## Backward Compatibility

- All existing processing scripts (`scripts/`) remain unchanged
- Same Discord notification functionality
- Same file upload limits and validations
- Same processor types and outputs

## Testing

### Backend
```bash
cd backend
# Install test dependencies
pip install pytest httpx
# Run tests
pytest
```

### Frontend
```bash
cd frontend
# Run tests
npm run test
```

## Deployment Notes

1. **Environment Variables**: Ensure all required env vars are set
2. **Volumes**: Mount `uploads/` and `scripts/` directories
3. **Ports**: Backend (8000), Frontend (3000)
4. **CORS**: Configured automatically for local development

## Migration Checklist

- [ ] Install Python 3.11+ and Node.js 20+
- [ ] Install backend dependencies
- [ ] Install frontend dependencies
- [ ] Copy environment variables
- [ ] Test processors individually
- [ ] Test Docker deployment
- [ ] Update CI/CD pipelines if applicable
- [ ] Update monitoring/logging configurations

## Troubleshooting

### Common Issues

1. **CORS errors**: Check `ALLOWED_ORIGINS` in backend config
2. **File upload fails**: Verify `UPLOAD_FOLDER` exists and has permissions
3. **API not found**: Ensure backend is running on correct port
4. **Frontend can't connect**: Check `NUXT_PUBLIC_API_BASE` environment variable

## Support

For questions or issues with the migration:
1. Check the API documentation at `/docs`
2. Review the README.v2.md
3. Open an issue on GitHub
