# House of Cards - Backend API

Express.js backend for the House of Cards AI Orchestration System, powered by MongoDB and Mongoose.

## Setup & Running

1. **Install dependencies**:
   ```bash
   cd Backend
   npm install
   ```

2. **Configure Environment**:
   - Open `.env` and set your `MONGO_URI` (e.g., local MongoDB or MongoDB Atlas connection string):
     ```env
     PORT=5000
     MONGO_URI=mongodb://127.0.0.1:27017/house_of_cards
     JWT_SECRET=your_jwt_secret_key_here
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

- `POST /api/auth/signup` - Register a new operator (requires `name`, `email`, `password`)
- `POST /api/auth/login` - Authenticate operator and receive JWT token (requires `email`, `password`)
- `GET /api/auth/me` - Get operator profile (requires `Authorization: Bearer <token>` header)
- `GET /api/health` - System health check
