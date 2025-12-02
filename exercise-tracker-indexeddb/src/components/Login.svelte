<script>
  import { createEventDispatcher } from 'svelte';
  import { login as apiLogin } from "../lib/api.js";

  const dispatch = createEventDispatcher();

  let username = "";
  let password = "";
  let loading = false;

  async function loginUser() {
    loading = true;

    try {
      // Call Django login API
      const data = await apiLogin(username, password);

      // Save JWT access + refresh tokens
      if (data.token) {
        localStorage.setItem("token", data.token);       // access token
      }
      if (data.refresh) {
        localStorage.setItem("refresh", data.refresh);   // refresh token
      }

      // Notify parent component (App.svelte)
      dispatch("login", {
        id: data.id,
        username: data.username,
        role: data.role
      });

    } catch (err) {
      alert(err.error || err.message || "Login failed!");
    } finally {
      loading = false;
    }
  }
</script>

<style>
  body, html {
    height: 100%;
    margin: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #0ea5a4, #3b82f6);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .login-wrapper {
    width: 100%;
    max-width: 400px;
    padding: 32px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.95);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    text-align: center;
  }

  .logo {
    width: 80px;
    height: 80px;
    margin: 0 auto 16px auto;
    border-radius: 50%;
    background: #0ea5a4;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 2rem;
    font-weight: bold;
  }

  .login-wrapper h1 {
    margin: 0;
    font-size: 2rem;
    color: #0f172a;
  }

  .login-wrapper h2 {
    margin: 4px 0 24px 0;
    font-size: 0.9rem;
    color: #64748b;
    font-weight: normal;
  }

  .login-wrapper input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border-radius: 8px;
    border: 1px solid #ddd;
    font-size: 1rem;
    outline: none;
    transition: border 0.3s, box-shadow 0.3s;
  }

  .login-wrapper input:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 6px rgba(59, 130, 246, 0.4);
  }

  .login-wrapper button {
    width: 100%;
    padding: 12px;
    margin-top: 16px;
    border-radius: 8px;
    background: #3b82f6;
    color: #fff;
    font-weight: 600;
    font-size: 1rem;
    border: none;
    cursor: pointer;
    transition: background 0.3s, transform 0.2s;
  }

  .login-wrapper button:hover {
    background: #2563eb;
    transform: translateY(-2px);
  }

  @media (max-width: 480px) {
    .login-wrapper {
      padding: 24px 16px;
    }
    .logo {
      width: 60px;
      height: 60px;
      font-size: 1.5rem;
    }
    .login-wrapper h1 {
      font-size: 1.5rem;
    }
    .login-wrapper h2 {
      font-size: 0.85rem;
    }
  }
</style>

<div class="login-wrapper">
  <div class="logo">ET</div>
  <h1>Exercise Tracker</h1>
  <h2>Developed by codecademyonline.com</h2>

  <input placeholder="Username" bind:value={username} />
  <input type="password" placeholder="Password" bind:value={password} />

  <button on:click={loginUser} disabled={loading}>
    {loading ? "Logging in..." : "Login"}
  </button>
</div>
