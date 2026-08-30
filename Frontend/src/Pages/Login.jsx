import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();
  const [isSignUp, setIsSignUp] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    rememberMe: true,
    agreeTerms: false,
  });

  const [errors, setErrors] = useState({});

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));

    // Clear error on change
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (isSignUp && !formData.name.trim()) {
      newErrors.name = "Operator name is required";
    }

    if (!formData.email.trim()) {
      newErrors.email = "Workspace email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Enter a valid email address";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 6) {
      newErrors.password = "Must be at least 6 characters";
    }

    if (isSignUp) {
      if (!formData.confirmPassword) {
        newErrors.confirmPassword = "Confirm your password";
      } else if (formData.password !== formData.confirmPassword) {
        newErrors.confirmPassword = "Passwords do not match";
      }

      if (!formData.agreeTerms) {
        newErrors.agreeTerms = "Accept terms and agent guidelines to continue";
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    setIsLoading(true);
    setSuccessMessage("");
    setErrors((prev) => ({ ...prev, server: "" }));

    const endpoint = isSignUp ? "/api/auth/signup" : "/api/auth/login";
    const payload = isSignUp
      ? { name: formData.name, email: formData.email, password: formData.password }
      : { email: formData.email, password: formData.password };

    try {
      const response = await fetch(`http://localhost:5000${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.message || "Authentication failed");
      }

      // Save token and operator info to localStorage
      if (data.token) {
        localStorage.setItem("hoc_token", data.token);
      }
      if (data.user) {
        localStorage.setItem("hoc_operator", JSON.stringify(data.user));
      }

      setIsLoading(false);
      setSuccessMessage(
        isSignUp
          ? "OPERATOR REGISTERED! INITIALIZING ORCHESTRATOR..."
          : "AUTHENTICATED! ACCESSING AGENT CONSOLE..."
      );

      setTimeout(() => {
        navigate("/main");
      }, 1000);
    } catch (err) {
      setIsLoading(false);
      setErrors((prev) => ({
        ...prev,
        server: err.message || "Unable to connect to backend server. Ensure backend is running.",
      }));
    }
  };

  const toggleMode = (signUpState) => {
    setIsSignUp(signUpState);
    setErrors({});
    setSuccessMessage("");
  };

  return (
    <div className="min-h-screen bg-[#F6F3EA] text-[#171717] flex flex-col justify-between relative overflow-hidden px-4 py-6 sm:px-6 sm:py-8">
      {/* Background decorative elements */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden select-none">
        {/* Soft atmospheric glows */}
        <div className="absolute top-[-120px] left-[-120px] w-[380px] h-[380px] bg-red-200/30 blur-[100px] rounded-full" />
        <div className="absolute bottom-[-120px] right-[-120px] w-[380px] h-[380px] bg-gray-300/40 blur-[100px] rounded-full" />

        {/* Ambient card suits representing agent orchestration */}
        <div className="absolute top-16 left-8 text-black/10 text-6xl sm:text-7xl rotate-12">
          ♠
        </div>
        <div className="absolute bottom-16 right-8 text-red-300/35 text-6xl sm:text-7xl -rotate-12">
          ♥
        </div>
        <div className="absolute top-1/2 right-12 text-red-300/25 text-5xl rotate-12 hidden md:block">
          ♦
        </div>
        <div className="absolute top-1/3 left-12 text-black/10 text-5xl -rotate-12 hidden md:block">
          ♣
        </div>
      </div>

      {/* Top Bar / Navigation */}
      <header className="relative z-10 flex items-center justify-between max-w-4xl mx-auto w-full mb-4">
        <button
          onClick={() => navigate("/")}
          className="
            flex items-center gap-2
            px-3 py-1.5
            text-[10px] sm:text-[11px]
            tracking-[0.18em]
            uppercase
            font-bold
            bg-[#FFF8E7]
            text-[#171717]
            border-[2px]
            border-[#171717]
            rounded
            shadow-[3px_3px_0px_rgba(23,23,23,0.15)]
            hover:-translate-y-0.5
            hover:shadow-[4px_5px_0px_rgba(23,23,23,0.2)]
            active:translate-y-0
            active:shadow-[1px_1px_0px_rgba(23,23,23,0.15)]
            transition-all
          "
          style={{ fontFamily: "'Press Start 2P', monospace" }}
        >
          <span>←</span> Back to Home
        </button>

        <div
          className="text-[9px] sm:text-[10px] tracking-[0.25em] text-black/40 uppercase text-right"
          style={{ fontFamily: "'Press Start 2P', monospace" }}
        >
          AI ORCHESTRATION SYSTEM
        </div>
      </header>

      {/* Main Authentication Card */}
      <main className="relative z-10 flex-1 flex items-center justify-center py-2">
        <div
          className="
            relative
            w-full
            max-w-[440px]
            bg-[#FFF8E7]
            border-[4px]
            border-[#171717]
            rounded-lg
            shadow-[8px_10px_0px_rgba(23,23,23,0.18)]
            p-5 sm:p-7
            transition-all
            duration-300
          "
        >
          {/* Retro paper texture */}
          <div
            className="
              absolute inset-0 pointer-events-none
              opacity-[0.07]
              bg-[radial-gradient(#171717_0.8px,transparent_0.8px)]
              bg-[size:6px_6px]
              rounded-lg
            "
          />

          {/* Vintage top highlight */}
          <div className="absolute top-0 left-0 w-full h-10 bg-white/35 rounded-t pointer-events-none" />

          {/* Card Corner Symbol - Top Left */}
          <div className="absolute top-3 left-3 select-none pointer-events-none flex flex-col items-center leading-none">
            <span
              className="text-xs font-black text-[#171717]"
              style={{ fontFamily: "monospace" }}
            >
              {isSignUp ? "S" : "A"}
            </span>
            <span className={isSignUp ? "text-[#C93636] text-xs" : "text-[#171717] text-xs"}>
              {isSignUp ? "♥" : "♠"}
            </span>
          </div>

          {/* Card Corner Symbol - Bottom Right */}
          <div className="absolute bottom-3 right-3 select-none pointer-events-none flex flex-col items-center leading-none rotate-180">
            <span
              className="text-xs font-black text-[#171717]"
              style={{ fontFamily: "monospace" }}
            >
              {isSignUp ? "S" : "A"}
            </span>
            <span className={isSignUp ? "text-[#C93636] text-xs" : "text-[#171717] text-xs"}>
              {isSignUp ? "♥" : "♠"}
            </span>
          </div>

          {/* Header Title */}
          <div className="text-center mb-5 relative z-10">
            <div className="inline-block mb-1">
              <span className="text-xs font-black text-red-600 tracking-widest uppercase">
                {isSignUp ? "♠ NEW OPERATOR ♠" : "♠ ORCHESTRATOR ACCESS ♠"}
              </span>
            </div>
            <h2
              className="text-lg sm:text-xl font-black tracking-tight uppercase text-[#171717]"
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              {isSignUp ? "CREATE ACCOUNT" : "OPERATOR SIGN IN"}
            </h2>
            <p className="text-[10px] text-black/50 tracking-wider uppercase mt-1">
              {isSignUp
                ? "Register workspace to orchestrate agent teams"
                : "Authenticate credentials to access agent console"}
            </p>
          </div>

          {/* Mode Switcher Tabs */}
          <div className="relative z-10 grid grid-cols-2 gap-2 p-1 bg-[#171717]/5 border-2 border-[#171717] rounded-md mb-5">
            <button
              type="button"
              onClick={() => toggleMode(false)}
              className={`
                py-2 text-[10px] tracking-wider uppercase font-black rounded transition-all
                ${
                  !isSignUp
                    ? "bg-[#171717] text-[#FFF8E7] shadow-[2px_2px_0px_rgba(23,23,23,0.2)]"
                    : "text-black/60 hover:text-black hover:bg-black/5"
                }
              `}
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              ♠ Sign In
            </button>
            <button
              type="button"
              onClick={() => toggleMode(true)}
              className={`
                py-2 text-[10px] tracking-wider uppercase font-black rounded transition-all
                ${
                  isSignUp
                    ? "bg-[#C93636] text-[#FFF8E7] shadow-[2px_2px_0px_rgba(201,54,54,0.3)]"
                    : "text-black/60 hover:text-black hover:bg-black/5"
                }
              `}
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              ♥ Sign Up
            </button>
          </div>

          {/* Success Banner */}
          {successMessage && (
            <div
              className="relative z-10 mb-4 p-2.5 bg-green-100 border-2 border-green-700 text-green-900 rounded text-center text-[10px] font-bold uppercase tracking-wider animate-pulse"
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              {successMessage}
            </div>
          )}

          {/* Server Error Banner */}
          {errors.server && (
            <div
              className="relative z-10 mb-4 p-2.5 bg-red-100 border-2 border-red-600 text-red-900 rounded text-center text-[10px] font-bold uppercase tracking-wider"
              style={{ fontFamily: "'Press Start 2P', monospace" }}
            >
              ⚠ {errors.server}
            </div>
          )}

          {/* Auth Form */}
          <form onSubmit={handleSubmit} className="relative z-10 space-y-3.5">
            {/* Name Field (Sign Up Only) */}
            {isSignUp && (
              <div>
                <label className="block text-[9px] font-black uppercase tracking-widest text-[#171717] mb-1">
                  Operator Handle / Alias
                </label>
                <div className="relative">
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    placeholder="e.g. Architect_01"
                    className={`
                      w-full px-3 py-2 text-xs bg-white text-[#171717]
                      border-2 rounded font-mono outline-none
                      transition-colors placeholder:text-black/30
                      ${
                        errors.name
                          ? "border-red-600 bg-red-50/50"
                          : "border-[#171717] focus:border-red-600 focus:ring-1 focus:ring-red-600"
                      }
                    `}
                  />
                  <span className="absolute right-3 top-2 text-xs opacity-30 select-none">
                    ♣
                  </span>
                </div>
                {errors.name && (
                  <p className="mt-1 text-[9px] text-red-600 font-bold tracking-wide">
                    ⚠ {errors.name}
                  </p>
                )}
              </div>
            )}

            {/* Email Field */}
            <div>
              <label className="block text-[9px] font-black uppercase tracking-widest text-[#171717] mb-1">
                Workspace Email
              </label>
              <div className="relative">
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="operator@houseofcards.ai"
                  className={`
                    w-full px-3 py-2 text-xs bg-white text-[#171717]
                    border-2 rounded font-mono outline-none
                    transition-colors placeholder:text-black/30
                    ${
                      errors.email
                        ? "border-red-600 bg-red-50/50"
                        : "border-[#171717] focus:border-red-600 focus:ring-1 focus:ring-red-600"
                    }
                  `}
                />
                <span className="absolute right-3 top-2 text-xs opacity-30 select-none">
                  ♠
                </span>
              </div>
              {errors.email && (
                <p className="mt-1 text-[9px] text-red-600 font-bold tracking-wide">
                  ⚠ {errors.email}
                </p>
              )}
            </div>

            {/* Password Field */}
            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-[9px] font-black uppercase tracking-widest text-[#171717]">
                  Password / Keyphrase
                </label>
                {!isSignUp && (
                  <button
                    type="button"
                    onClick={() => alert("Password reset link sent to your registered email.")}
                    className="text-[9px] text-red-600 hover:underline uppercase font-bold tracking-wider"
                  >
                    Reset Key?
                  </button>
                )}
              </div>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder="••••••••"
                  className={`
                    w-full px-3 py-2 text-xs bg-white text-[#171717]
                    border-2 rounded font-mono outline-none
                    transition-colors placeholder:text-black/30 pr-16
                    ${
                      errors.password
                        ? "border-red-600 bg-red-50/50"
                        : "border-[#171717] focus:border-red-600 focus:ring-1 focus:ring-red-600"
                    }
                  `}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-2 top-1.5 px-2 py-0.5 text-[9px] font-mono font-bold bg-[#171717]/10 hover:bg-[#171717]/20 rounded text-[#171717] select-none"
                >
                  {showPassword ? "HIDE" : "SHOW"}
                </button>
              </div>
              {errors.password && (
                <p className="mt-1 text-[9px] text-red-600 font-bold tracking-wide">
                  ⚠ {errors.password}
                </p>
              )}
            </div>

            {/* Confirm Password Field (Sign Up Only) */}
            {isSignUp && (
              <div>
                <label className="block text-[9px] font-black uppercase tracking-widest text-[#171717] mb-1">
                  Confirm Password
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    placeholder="••••••••"
                    className={`
                      w-full px-3 py-2 text-xs bg-white text-[#171717]
                      border-2 rounded font-mono outline-none
                      transition-colors placeholder:text-black/30
                      ${
                        errors.confirmPassword
                          ? "border-red-600 bg-red-50/50"
                          : "border-[#171717] focus:border-red-600 focus:ring-1 focus:ring-red-600"
                      }
                    `}
                  />
                  <span className="absolute right-3 top-2 text-xs text-red-500/40 select-none">
                    ♥
                  </span>
                </div>
                {errors.confirmPassword && (
                  <p className="mt-1 text-[9px] text-red-600 font-bold tracking-wide">
                    ⚠ {errors.confirmPassword}
                  </p>
                )}
              </div>
            )}

            {/* Options Checkbox */}
            <div className="pt-1">
              {isSignUp ? (
                <label className="flex items-start gap-2 cursor-pointer select-none">
                  <input
                    type="checkbox"
                    name="agreeTerms"
                    checked={formData.agreeTerms}
                    onChange={handleInputChange}
                    className="mt-0.5 accent-[#C93636] cursor-pointer"
                  />
                  <span className="text-[10px] text-black/70 leading-tight">
                    I agree to the Platform Terms & AI Safety Guidelines
                  </span>
                </label>
              ) : (
                <label className="flex items-center gap-2 cursor-pointer select-none">
                  <input
                    type="checkbox"
                    name="rememberMe"
                    checked={formData.rememberMe}
                    onChange={handleInputChange}
                    className="accent-[#171717] cursor-pointer"
                  />
                  <span className="text-[10px] text-black/70">
                    Remember orchestrator session on this machine
                  </span>
                </label>
              )}
              {errors.agreeTerms && (
                <p className="mt-1 text-[9px] text-red-600 font-bold tracking-wide">
                  ⚠ {errors.agreeTerms}
                </p>
              )}
            </div>

            {/* Submit Action Button */}
            <div className="pt-2">
              <button
                type="submit"
                disabled={isLoading}
                className={`
                  w-full py-3 px-4
                  ${isSignUp ? "bg-[#C93636] hover:bg-[#a82525]" : "bg-[#171717] hover:bg-red-600"}
                  text-[#FFF8E7]
                  text-[11px] sm:text-[12px]
                  tracking-[0.2em]
                  uppercase
                  font-black
                  rounded
                  border-[3px]
                  ${isSignUp ? "border-[#C93636] hover:border-[#a82525]" : "border-[#171717] hover:border-red-600"}
                  shadow-[4px_5px_0px_rgba(23,23,23,0.18)]
                  transition-all
                  duration-200
                  hover:-translate-y-0.5
                  hover:shadow-[5px_7px_0px_rgba(23,23,23,0.22)]
                  active:translate-y-0
                  active:shadow-[2px_2px_0px_rgba(23,23,23,0.18)]
                  disabled:opacity-60 disabled:cursor-not-allowed
                `}
                style={{ fontFamily: "'Press Start 2P', monospace" }}
              >
                {isLoading ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="animate-spin">♠</span> INITIALIZING...
                  </span>
                ) : isSignUp ? (
                  <span className="flex items-center justify-center gap-2">
                    <span>♥</span> DEPLOY WORKSPACE <span>♥</span>
                  </span>
                ) : (
                  <span className="flex items-center justify-center gap-2">
                    <span>♠</span> ACCESS CONSOLE <span>♠</span>
                  </span>
                )}
              </button>
            </div>
          </form>

          {/* Switch mode footer link */}
          <div className="text-center mt-5 text-[10px] text-black/60">
            {isSignUp ? (
              <p>
                Already have an operator account?{" "}
                <button
                  type="button"
                  onClick={() => toggleMode(false)}
                  className="text-red-600 font-bold hover:underline ml-1"
                >
                  Sign In Here
                </button>
              </p>
            ) : (
              <p>
                Need to set up a new workspace?{" "}
                <button
                  type="button"
                  onClick={() => toggleMode(true)}
                  className="text-red-600 font-bold hover:underline ml-1"
                >
                  Create Account
                </button>
              </p>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 text-center py-2">
        <div className="flex items-center justify-center gap-3 mb-2">
          <span className="text-black/20 text-sm">♠</span>
          <span className="text-red-400 text-sm">♥</span>
          <span className="text-red-400 text-sm">♦</span>
          <span className="text-black/20 text-sm">♣</span>
        </div>
        <p className="text-[8px] text-black/40 tracking-[0.25em] uppercase">
          AI • AGENTS • ORCHESTRATION • HOUSE OF CARDS
        </p>
      </footer>
    </div>
  );
};

export default Login;
