# Magic Link Authentication API

This is a FastAPI-based authentication system that implements passwordless authentication using magic links.

## Features

- Request magic link authentication
- Verify magic link tokens
- Email-based authentication
- JWT token generation and verification
- Docker support for easy deployment

## Setup

### Using Docker (Recommended)

1. Configure environment variables:

   ```bash
   cp .env.example .env
   ```

   Update the following variables in `.env`:

   - `SECRET_KEY`: Your secret key for JWT tokens
   - `SMTP_USER`: Your email address
   - `SMTP_PASSWORD`: Your email app password
   - `SMTP_HOST`: SMTP server address
   - `SMTP_PORT`: SMTP server port

2. Build and run with Docker Compose:

   ```bash
   docker-compose up --build
   ```

   The API will be available at http://localhost:8000

### Manual Setup (Development)

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables as described above

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

- POST `/request-magic-link`: Request a magic link (requires email in request body)
- GET `/verify`: Verify magic link token (requires token query parameter)

## Usage

1. Send a POST request to `/request-magic-link` with an email:

```json
{
  "email": "user@example.com"
}
```

2. Check email for magic link
3. Click the magic link or use the token in the `/verify` endpoint

## Security Notes

- In production, update CORS settings to allow only specific origins
- Use strong SECRET_KEY
- Store sensitive information in environment variables
- Configure proper email settings
