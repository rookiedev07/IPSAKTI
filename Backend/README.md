# House of Cards - Backend API

Express.js backend for the House of Cards AI Orchestration System. Operating in frictionless, standalone mode without login/signup barriers.

## Setup & Running

1. **Install dependencies**:
   ```bash
   cd Backend
   npm install
   ```

2. **Configure Environment**:
   - Open `.env`:
     ```env
     PORT=5000
     HOC_KEY=your_nim_or_groq_api_key
     ```

3. **Start the server**:
   - Development mode (with nodemon):
     ```bash
     npm run dev
     ```
   - Production mode:
     ```bash
     npm start
     ```

## API Endpoints

- `POST /api/prompt/match` - Match user prompt to AI domain and retrieve agents
- `POST /api/prompt/orchestrate` - Run full 5-agent AI orchestration pipeline
- `GET /api/health` - System health check
