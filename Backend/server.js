import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import promptRoutes from "./Routes/promptRoutes.js";

// Load environment variables
dotenv.config();

// Initialize Express
const app = express();

// Middlewares
// Allowed origins: production Vercel URL + any Vercel preview deployments
const ALLOWED_ORIGINS = [
  process.env.FRONTEND_URL,           // e.g. https://ipsakti-two.vercel.app
  "https://ipsakti-two.vercel.app",   // production fallback (no trailing slash)
].filter(Boolean);

app.use(
  cors({
    origin: (origin, callback) => {
      // Allow requests with no origin (e.g. curl, Postman, server-to-server)
      if (!origin) return callback(null, true);
      // Allow any *.vercel.app preview URL or exact production match
      if (
        ALLOWED_ORIGINS.includes(origin) ||
        origin.endsWith(".vercel.app")
      ) {
        return callback(null, true);
      }
      return callback(new Error(`CORS blocked: ${origin}`));
    },
    methods: ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allowedHeaders: ["Content-Type", "Authorization", "X-Requested-With"],
    credentials: true,
  })
);
app.use(express.json());

// Routes
app.use("/api/prompt", promptRoutes);

// Health check endpoint
app.get("/api/health", (req, res) => {
  res.status(200).json({
    status: "ok",
    message: "IP-SAKTI Problem Solver API is operational",
    timestamp: new Date().toISOString(),
  });
});

// Fallback 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: "Endpoint not found",
  });
});

// Start Server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`[OK] IP-SAKTI Backend running on port ${PORT}`);
  console.log(`[OK] Health Check: http://localhost:${PORT}/api/health`);
});
