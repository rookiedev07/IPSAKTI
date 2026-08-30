import express from "express";
import { matchPromptHandler, orchestrateHandler } from "../Controllers/promptController.js";

const router = express.Router();

// Match & Orchestration routes
router.post("/match", matchPromptHandler);
router.post("/orchestrate", orchestrateHandler);

export default router;
