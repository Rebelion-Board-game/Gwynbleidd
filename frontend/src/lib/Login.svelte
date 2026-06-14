<script>
  import { createEventDispatcher } from 'svelte';
  import Banner from '../lib/Banner.svelte';

  export let API_BASE;
  export let successMessage = '';

  const dispatch = createEventDispatcher();
  
  let email = '';
  let password = '';
  let errorMessage = '';

  async function handleLogin() {
    errorMessage = '';
    try {
      const response = await fetch(`${API_BASE}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Invalid email or password.');

      dispatch('loginSuccess', { token: data.access_token });
    } catch (err) {
      errorMessage = err.message;
    }
  }
</script>

<div class="auth-card">
  <h2>Welcome Back</h2>
  <p class="subtitle">Sign in to manage your game leaderboards</p>
  
  <form on:submit|preventDefault={handleLogin}>
    <div class="form-group">
      <label for="login-email">Email Address</label>
      <input type="email" id="login-email" bind:value={email} placeholder="name@domain.com" required>
    </div>
    
    <div class="form-group">
      <label for="login-password">Password</label>
      <input type="password" id="login-password" bind:value={password} placeholder="••••••••" required>
    </div>
    
    <button type="submit" class="primary-action login-color">Sign In</button>
  </form>
  
  <p class="switch-prompt">
    Don't have an account? <a href="#register" on:click|preventDefault={() => dispatch('switch', 'register')}>Create one here</a>
  </p>

  <div class="separator"></div>

  <button type="button" class="back-btn" on:click={() => dispatch('back')}>
    Back
  </button>

  {#if successMessage}
    <div class="banner-space">
      <Banner type="success" message={successMessage} />
    </div>
  {/if}

  {#if errorMessage}
    <div class="banner-space">
      <Banner type="error" message={errorMessage} />
    </div>
  {/if}
</div>

<style>
  .auth-card {
    background: #1e293b;
    padding: 2.5rem;
    border-radius: 12px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    width: 100%;
    max-width: 440px;
    border: 1px solid #334155;
    display: flex;
    flex-direction: column;
  }

  h2 {
    color: #f8fafc;
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
    text-align: center;
  }

  .subtitle {
    color: #94a3b8;
    font-size: 0.875rem;
    margin: 0 0 2rem 0;
    text-align: center;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1.25rem;
  }

  label {
    color: #cbd5e1;
    font-size: 0.85rem;
    font-weight: 500;
  }

  input {
    background-color: #0f172a;
    border: 1px solid #475569;
    border-radius: 6px;
    color: #f8fafc;
    padding: 0.75rem 1rem;
    font-size: 0.95rem;
    transition: all 0.2s ease;
    width: 100%;
    box-sizing: border-box;
  }

  input:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
  }

  .primary-action {
    width: 100%;
    color: #ffffff;
    border: none;
    padding: 0.85rem;
    border-radius: 6px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
    margin-top: 0.5rem;
  }

  .login-color {
    background-color: #4f46e5;
  }

  .login-color:hover {
    background-color: #4338ca;
  }

  .switch-prompt {
    color: #94a3b8;
    font-size: 0.875rem;
    text-align: center;
    margin: 1.5rem 0;
  }

  .switch-prompt a {
    color: #818cf8;
    text-decoration: none;
    font-weight: 500;
  }

  .switch-prompt a:hover {
    text-decoration: underline;
  }

  .separator {
    height: 1px;
    background-color: #334155;
    margin-bottom: 1.25rem;
  }

  .back-btn {
    width: 100%;
    background: none;
    border: 1px solid #475569;
    color: #cbd5e1;
    padding: 0.75rem;
    font-size: 0.9rem;
    font-weight: 500;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .back-btn:hover {
    background-color: #0f172a;
    color: #f8fafc;
    border-color: #64748b;
  }

  .banner-space {
    margin-top: 1.5rem;
  }
</style>