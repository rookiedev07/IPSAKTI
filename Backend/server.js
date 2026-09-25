import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import promptRoutes from "./Routes/promptRoutes.js";

// Load environment variables
dotenv.config();

// Initialize Express
const app = express();

// Middlewares
app.use(
  cors({
    origin: "*",
    methods: ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allowedHeaders: ["Content-Type", "Authorization", "X-Requested-With"],
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
