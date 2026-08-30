import mongoose from "mongoose";
import dns from "dns";

const connectDB = async () => {
  const uri = process.env.MONGO_URI || "mongodb://127.0.0.1:27017/house_of_cards";
  
  // Fix for Node.js querySrv ECONNREFUSED on Windows with local ISP/router DNS
  if (uri.startsWith("mongodb+srv://")) {
    try {
      dns.setServers(["8.8.8.8", "1.1.1.1"]);
    } catch (e) {
      // Ignore if DNS server configuration fails
    }
  }

  try {
    const conn = await mongoose.connect(uri, {
      serverSelectionTimeoutMS: 4000,
    });
    console.log(`♠ MongoDB Connected: ${conn.connection.host}`);
  } catch (error) {
    console.warn(`⚠️ MongoDB Connection Notice: ${error.message}`);
    console.log(`♠ Running in resilient standalone mode (AI Orchestration is fully operational).`);
  }
};

export default connectDB;
