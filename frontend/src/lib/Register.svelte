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
      const response = await fetch(`${API_BASE}/dev/register`, {
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

<div class="auth-card">
  <h2>Create Developer Account</h2>
  <p class="subtitle">Get instant access to your dedicated database pool</p>
  
  <form on:submit|preventDefault={handleRegister}>
    <label for="reg-email">Email Address</label>
    <input type="email" id="reg-email" bind:value={email} placeholder="name@domain.com" required>
    
    <label for="reg-password">Password</label>
    <input type="password" id="reg-password" bind:value={password} placeholder="Minimum 8 characters" required>
    
    <label for="confirm-password">Repeat Password</label>
    <input type="password" id="confirm-password" bind:value={confirmPassword} placeholder="••••••••" required>
    
    <button type="submit" class="primary-action signup-color">Register Account</button>
  </form>
  
  <p class="switch-prompt">
    Already registered? <a href="#login" on:click|preventDefault={() => dispatch('switch', 'login')}>Log in to your dashboard</a>
  </p>

  <Banner type="error" message={errorMessage} />
</div>