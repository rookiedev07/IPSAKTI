import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import connectDB from "./DB/connectDB.js";
import authRoutes from "./Routes/authRoutes.js";
import promptRoutes from "./Routes/promptRoutes.js";

// Load environment variables
dotenv.config();

// Initialize Express
const app = express();

// Connect to MongoDB
connectDB();

// Middlewares
app.use(cors());
app.use(express.json());

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/prompt", promptRoutes);

// Health check endpoint
app.get("/api/health", (req, res) => {
  res.status(200).json({
    status: "ok",
    message: "House of Cards AI Orchestration API is operational ♠",
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
  console.log(`♠ House of Cards Backend running on port ${PORT}`);
  console.log(`♠ Health Check: http://localhost:${PORT}/api/health`);
});
