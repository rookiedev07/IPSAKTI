import express from "express";
import { signup, login, getMe } from "../Controllers/authController.js";

const router = express.Router();

// Routes
router.post("/signup", signup);
router.post("/login", login);
router.get("/me", getMe);

export default router;
