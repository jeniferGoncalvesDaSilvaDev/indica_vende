# IndicaVende SaaS

## Overview

IndicaVende is a lead management and sales tracking SaaS platform with role-based access control. The system enables three types of users (Gestor/Manager, Vendedor/Seller, Indicador/Referrer) to collaborate on lead generation, assignment, and conversion tracking. Built with FastAPI backend and Streamlit frontend, it provides real-time dashboards, lead status tracking, and automated email notifications.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Structure

**Monorepo Design**: The application uses a clear separation between frontend and backend:
- `backend/` - FastAPI REST API service
- `frontend/` - Streamlit web interface
- Independent deployment of frontend and backend services

**Port Configuration**:
- Backend API: Port 8000
- Frontend UI: Port 5000

### Backend Architecture

**Framework**: FastAPI with Uvicorn ASGI server

**Database Layer**:
- ORM: SQLAlchemy with declarative base models
- Default: SQLite for development (`indicavende.db`)
- Production-ready: PostgreSQL support via environment variables
- Connection pooling configured for both SQLite and PostgreSQL

**Authentication**:
- Password hashing: bcrypt library
- Session management: Custom header-based authentication (`X-User-Email`)
- No JWT tokens - relies on email-based session headers
- Password verification on login endpoint

**Data Models**:
- `User`: Supports three roles (gestor, vendedor, indicador) with enum enforcement
- `Lead`: Tracks client information, status progression, and relationships to users
- Five lead statuses: novo, em_contato, em_negociacao, fechado, perdido
- Foreign key relationships: Lead -> Indicador (creator), Lead -> Vendedor (assignee)

**API Design**:
- RESTful endpoints with Pydantic schema validation
- Role-based data filtering at query level
- CORS enabled for all origins (should be restricted in production)
- Automatic timestamp tracking (created_at, updated_at)

**External Services**:
- Email notifications via SMTP (SMTP2Go configured as default provider)
- Welcome emails sent on user registration
- Environment-based SMTP configuration for multiple deployment scenarios

### Frontend Architecture

**Framework**: Streamlit for rapid dashboard development

**Authentication Flow**:
- Login credentials sent to backend `/auth/login` endpoint
- User session stored in `st.session_state`
- Email header (`X-User-Email`) included in all authenticated requests
- Dynamic backend URL resolution based on deployment environment

**Environment Detection**:
- Streamlit Cloud: Uses `BACKEND_URL` environment variable
- Replit Deployment: Connects to localhost:8000
- Local Development: Configurable via environment variables

**Role-Based Interfaces**:
- `gestor.py`: Executive dashboard with analytics, full lead management, user administration
- `vendedor.py`: Seller interface with assigned leads and status updates
- `indicador.py`: Referrer interface for creating new leads and tracking submissions

**UI Components**:
- Custom CSS styling for lead cards with status-based color coding
- Responsive column layouts for forms and data display
- Real-time dashboard with auto-refresh capability
- Statistical analysis with scipy for conversion metrics

### Data Flow

1. **Lead Creation**: Indicador creates lead → Assigns to Vendedor → Stored in database
2. **Lead Management**: Vendedor updates status/observations → Changes reflected in all dashboards
3. **Monitoring**: Gestor views aggregated metrics and manages all system entities

### Security Considerations

**Current Implementation**:
- Passwords hashed with bcrypt before storage
- Session validation on protected endpoints
- Role-based access control in API layer

**Production Recommendations**:
- Implement proper JWT token authentication
- Restrict CORS to specific origins
- Use HTTPS for all communications
- Rotate SECRET_KEY regularly
- Implement rate limiting on auth endpoints

## External Dependencies

### Third-Party Services

**Email Service (SMTP2Go)**:
- Purpose: Transactional emails (welcome messages, notifications)
- Configuration: Environment variables (SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD)
- Fallback: Silent failure in development when credentials missing

### Databases

**Primary Database**:
- Development: SQLite (file-based at `./indicavende.db`)
- Production: PostgreSQL (configurable via `DATABASE_URL` environment variable)
- Migration path: Same SQLAlchemy models work with both databases

### Python Package Dependencies

**Backend** (`backend/requirements.txt`):
- `fastapi==0.104.1` - Web framework
- `uvicorn==0.24.0` - ASGI server
- `sqlalchemy==2.0.23` - ORM
- `bcrypt==4.1.2` - Password hashing
- `python-multipart==0.0.6` - Form data parsing
- `pydantic[email]==2.5.0` - Data validation with email support
- `python-dotenv==1.0.0` - Environment variable management
- `psycopg2-binary==2.9.9` - PostgreSQL adapter

**Frontend** (`frontend/requirements.txt`):
- `streamlit>=1.32.0` - Web UI framework
- `requests>=2.31.0` - HTTP client for API calls
- `pandas>=2.1.0` - Data manipulation for dashboards
- `matplotlib` - Visualization library
- `scipy` - Statistical analysis

### Deployment Platforms

**Render.com**:
- Configured via `render.yaml` blueprint
- Automatic deployment from GitHub
- Environment variables managed through Render dashboard
- Python 3.10 runtime specified
- Dynamic PORT assignment via `$PORT` environment variable
- Database flexibility: supports both SQLite (default) and PostgreSQL (via DATABASE_URL override)
- Complete deployment guide available in `DEPLOY.md`

**Replit**:
- Development and deployment platform
- Automatic environment detection in codebase
- Backend runs on localhost:8000 during deployment

### Environment Variables

**Required**:
- `DATABASE_URL` - Database connection string (defaults to SQLite)
- `SECRET_KEY` - Session secret (defaults to development key)

**Optional**:
- `BACKEND_URL` - Frontend-to-backend connection URL
- `SMTP_SERVER`, `SMTP_PORT`, `SENDER_EMAIL`, `SENDER_PASSWORD` - Email service configuration
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Session timeout (default: 60)
- `PYTHON_VERSION` - Runtime version for deployment