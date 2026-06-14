<script>
  import { createEventDispatcher } from 'svelte';
  import Banner from '../lib/Banner.svelte';

  export let API_BASE;
  const dispatch = createEventDispatcher();

  let email = '';
  let password = '';
  let confirmPassword = '';
  let errorMessage = '';

  async function handleRegister() {
    errorMessage = '';

    if (password.length < 8) {
      errorMessage = 'Password must be at least 8 characters long.';
      return;
    }

    if (password !== confirmPassword) {
      errorMessage = 'Passwords do not match. Please verify and try again.';
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Registration failed.');

      dispatch('registerSuccess');
    } catch (err) {
      errorMessage = err.message;
    }
  }
</script>

<div class="auth-wrapper">
  <div class="auth-card">
    <h2>Create Developer Account</h2>
    <p class="subtitle">Get instant access to your dedicated database pool</p>
    
    <form on:submit|preventDefault={handleRegister}>
      <div class="form-group">
        <label for="reg-email">Email Address</label>
        <input type="email" id="reg-email" bind:value={email} placeholder="name@domain.com" required>
      </div>
      
      <div class="form-group">
        <label for="reg-password">Password</label>
        <input type="password" id="reg-password" bind:value={password} placeholder="Minimum 8 characters" required>
      </div>
      
      <div class="form-group">
        <label for="confirm-password">Repeat Password</label>
        <input type="password" id="confirm-password" bind:value={confirmPassword} placeholder="••••••••" required>
      </div>
      
      <button type="submit" class="primary-action signup-color">Register Account</button>
    </form>
    
    <p class="switch-prompt">
      Already registered? <a href="#login" on:click|preventDefault={() => dispatch('switch', 'login')}>Log in to your dashboard</a>
    </p>

    <!-- Banner component integration -->
    {#if errorMessage}
      <div class="banner-space">
        <Banner type="error" message={errorMessage} />
      </div>
    {/if}
  </div>
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

  .switch-prompt {
    color: #94a3b8;
    font-size: 0.875rem;
    text-align: center;
    margin: 1.5rem 0 0 0;
  }

  .switch-prompt a {
    color: #818cf8;
    text-decoration: none;
    font-weight: 500;
  }

  .switch-prompt a:hover {
    text-decoration: underline;
  }

  .banner-space {
    margin-top: 1.5rem;
  }
</style>