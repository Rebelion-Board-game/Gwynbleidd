<script>
  import { createEventDispatcher } from 'svelte';
  export let token = '';

  const dispatch = createEventDispatcher();
</script>

<header class="main-header">
  <div class="container navbar">
    <button class="logo-btn" on:click={() => dispatch('nav', 'landing')}>
      <span class="icon">🐺</span>
      <span class="brand">GWYNBLEIDD <small class="badge">SaaS</small></span>
    </button>

    <nav class="nav-links" aria-label="Main navigation">
      {#if !token}
        <button class="btn-ghost" on:click={() => dispatch('auth', 'login')}>Sign In</button>
        <button class="btn-primary" on:click={() => dispatch('auth', 'register')}>Get Started</button>
      {:else}
        <button class="btn-ghost" on:click={() => dispatch('logout')}>Logout</button>
      {/if}
    </nav>
  </div>
</header>

<style>
  .main-header {
    /* background: #0b1120; */
    border-bottom: 1px solid #334155;
    padding: 0.85rem 0;
  }

  .container {
    max-width: 1400px;
    width: 95%;
    margin: 0 auto;
  }

  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .logo-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    text-align: left;
  }

  .brand {
    font-size: 1.1rem;
    font-weight: 800;
    letter-spacing: 0.5px;
    color: #f8fafc;
    display: flex;
    align-items: center;
    gap: 0.35rem;
  }

  .badge {
    background: #0d04ba;
    color: #ffffff;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
  }

  .nav-links {
    display: flex;
    gap: 0.75rem;
    align-items: center;
  }

  button {
    font-family: inherit;
    font-size: 0.875rem;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .btn-ghost {
    background: transparent;
    border: 1px solid #475569;
    color: #cbd5e1;
  }

  .btn-ghost:hover {
    background-color: #1e293b;
    color: #f8fafc;
    border-color: #64748b;
  }

  .btn-primary {
    background: #4f46e5;
    border: 1px solid transparent;
    color: #ffffff;
    font-weight: 600;
  }

  .btn-primary:hover {
    background: #4338ca;
  }
</style>