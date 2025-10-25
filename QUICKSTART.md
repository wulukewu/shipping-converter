# Shipping Converter v2.0 - Quick Start

## Refactored Architecture

This repository has been refactored with:
- **Backend**: FastAPI (Python) - Modern async API
- **Frontend**: Nuxt 3 (Vue) - Modern SPA framework

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Start all services
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose -f docker-compose.yml logs -f

# Stop services
docker-compose -f docker-compose.yml down
```

### Option 2: Manual Setup

```bash
# Use the provided script
./start.sh

# Or manually:

# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

## Access

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## File Structure

```
shipping-converter/
├── backend/          # FastAPI backend
├── frontend/         # Nuxt 3 frontend
├── scripts/          # Processing scripts (shared)
├── uploads/          # Upload directory
└── docker-compose.yml
```

## Documentation

- **Full README**: See `README.v2.md`
- **Migration Guide**: See `MIGRATION.md`
- **Original README**: See `README.md`

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
# Edit .env with your settings
```

## Testing

Backend:
```bash
cd backend
# API is self-documenting at /docs
curl http://localhost:8000/health
```

Frontend:
```bash
cd frontend
npm run dev
# Visit http://localhost:3000
```

## Next Steps

1. ✅ Review the new architecture in `README.v2.md`
2. ✅ Check the migration guide in `MIGRATION.md`
3. ✅ Test the processors at http://localhost:3000
4. ✅ Explore API docs at http://localhost:8000/docs

## Support

For questions or issues, please refer to the documentation or open an issue.
