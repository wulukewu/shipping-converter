# Architecture Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                            │
│                     http://localhost:3000                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (Nuxt 3)                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Pages                                                    │  │
│  │  ├── index.vue         (Home)                            │  │
│  │  └── processor/[id].vue (Dynamic Processor Pages)        │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Components                                               │  │
│  │  └── FileUpload.vue    (Drag & Drop Upload)              │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Layouts                                                  │  │
│  │  └── default.vue       (Navigation & Structure)          │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP/REST API
                           │ (JSON)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                            │
│                   http://localhost:8000                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Layer (routes.py)                                    │  │
│  │  ├── GET  /api/processors                                │  │
│  │  ├── POST /api/process/{type}                            │  │
│  │  └── GET  /api/download/{filename}                       │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────▼───────────────────────────────┐  │
│  │  Service Layer (processor_service.py)                    │  │
│  │  └── File Processing Logic                               │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────▼───────────────────────────────┐  │
│  │  Utils                                                    │  │
│  │  ├── file_utils.py      (File handling)                  │  │
│  │  └── discord_utils.py   (Discord notifications)          │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────┬──────────────────────────┬──────────────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────────┐  ┌──────────────────────────────┐
│  Processing Scripts      │  │  Discord Integration         │
│  (/scripts)              │  │                              │
│  ├── Unictron.py         │  │  ├── Webhook (Primary)       │
│  ├── Unictron_2.py       │  │  └── Bot (Fallback)          │
│  ├── DTJ_H.py            │  │                              │
│  ├── YONG_LAING.py       │  └──────────────────────────────┘
│  ├── YONG_LAING_desc.py  │
│  ├── VLI.py              │
│  └── ASECL.py            │
└──────────────┬────────────┘
               │
               ▼
┌──────────────────────────┐
│  File System             │
│  (/uploads)              │
│  └── Processed files     │
└──────────────────────────┘
```

## Data Flow

### 1. File Upload Flow
```
User Browser
    │
    │ 1. Drag & drop or select file
    ▼
Nuxt Frontend (FileUpload.vue)
    │
    │ 2. POST /api/process/{type}
    │    FormData with file
    ▼
FastAPI Backend (routes.py)
    │
    │ 3. Validate & process
    ▼
Processor Service
    │
    │ 4. Call appropriate script
    ▼
Processing Script
    │
    │ 5. Transform data
    ▼
File System (/uploads)
    │
    │ 6. Return download URL
    ▼
User Browser
    │
    └─ 7. Download button appears
```

### 2. Request/Response Format

#### Upload Request
```http
POST /api/process/unictron HTTP/1.1
Host: localhost:8000
Content-Type: multipart/form-data

file: [binary data]
```

#### Upload Response
```json
{
  "success": true,
  "message": "File processed successfully",
  "filename": "20241025_120000_data_processed.xlsx",
  "download_url": "/api/download/20241025_120000_data_processed.xlsx"
}
```

## Technology Stack

### Frontend Stack
```
┌─────────────────┐
│   Nuxt 3        │  Framework
│   Vue 3         │  UI Library
│   Composition    │  API Style
│   Auto-routing  │  File-based
│   TypeScript    │  (Optional)
└─────────────────┘
```

### Backend Stack
```
┌─────────────────┐
│   FastAPI       │  Framework
│   Pydantic      │  Validation
│   Uvicorn       │  Server
│   Python 3.11+  │  Language
│   Async/Await   │  Concurrency
└─────────────────┘
```

### Processing Stack
```
┌─────────────────┐
│   Pandas        │  Data processing
│   Openpyxl      │  Excel handling
│   xlrd          │  Old Excel format
│   Custom Logic  │  Business rules
└─────────────────┘
```

## Deployment Architecture

### Development
```
┌─────────────────┐     ┌─────────────────┐
│  Frontend       │     │  Backend        │
│  npm run dev    │────▶│  uvicorn --reload│
│  Port 3000      │     │  Port 8000      │
└─────────────────┘     └─────────────────┘
```

### Production (Docker)
```
┌──────────────────────────────────────────┐
│         Docker Compose                   │
│                                          │
│  ┌─────────────┐    ┌─────────────┐    │
│  │  Frontend   │    │  Backend    │    │
│  │  Container  │───▶│  Container  │    │
│  │  Port 3000  │    │  Port 8000  │    │
│  └─────────────┘    └─────────────┘    │
│         │                   │           │
│         └───────┬───────────┘           │
│                 │                       │
│         ┌───────▼───────┐              │
│         │  Volumes      │              │
│         │  - uploads/   │              │
│         │  - scripts/   │              │
│         └───────────────┘              │
└──────────────────────────────────────────┘
```

## Key Design Decisions

1. **Separation of Concerns**
   - Frontend handles UI/UX
   - Backend handles business logic
   - Scripts handle data transformation

2. **RESTful API**
   - Clear endpoints
   - Standard HTTP methods
   - JSON responses

3. **Async Operations**
   - FastAPI's async support
   - Non-blocking file operations
   - Better performance

4. **Type Safety**
   - Pydantic models for validation
   - Automatic API documentation
   - Fewer runtime errors

5. **File-based Routing**
   - Nuxt's auto-routing
   - Dynamic routes with [id]
   - Cleaner code structure

6. **Component Composition**
   - Reusable Vue components
   - Single responsibility
   - Easy to maintain

## Security Considerations

- ✅ File type validation
- ✅ File size limits (16MB)
- ✅ Secure filename handling
- ✅ CORS configuration
- ✅ Environment variables for secrets
- ⚠️  Add authentication (future)
- ⚠️  Add rate limiting (future)

## Performance Optimizations

- ✅ Async operations (FastAPI)
- ✅ Lazy loading (Nuxt)
- ✅ Component caching
- ✅ Static file serving
- ✅ Optimized Docker images
- ⚠️  Add Redis cache (future)
- ⚠️  Add CDN (future)

## Monitoring & Logging

Current:
- Console logs (development)
- Discord notifications (errors)

Future considerations:
- Structured logging
- Error tracking (Sentry)
- Performance monitoring
- Usage analytics

---

**Version**: 2.0.0
**Last Updated**: 2024-10-25
