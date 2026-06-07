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
      const response = await fetch(`${API_BASE}/dev/login`, {
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
  
  <Banner type="success" message={successMessage} />

  <form on:submit|preventDefault={handleLogin}>
    <label for="login-email">Email Address</label>
    <input type="email" id="login-email" bind:value={email} placeholder="name@domain.com" required>
    
    <label for="login-password">Password</label>
    <input type="password" id="login-password" bind:value={password} placeholder="••••••••" required>
    
    <button type="submit" class="primary-action">Sign In</button>
  </form>
  
  <p class="switch-prompt">
    Don't have an account? <a href="#register" on:click|preventDefault={() => dispatch('switch', 'register')}>Create one here</a>
  </p>

  <Banner type="error" message={errorMessage} />
</div>