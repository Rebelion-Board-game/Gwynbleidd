<script>
  import { onMount } from 'svelte';
  import Navbar from './lib/Navbar.svelte';
  import Footer from './lib/Footer.svelte';
  import Landing from './lib/Landing.svelte';
  import Auth from './lib/Auth.svelte';
  import Dashboard from './lib/Dashboard.svelte';
  import Documentation from './lib/Documentation.svelte';

  let currentPage = 'landing'; 
  let authMode = 'login';      
  let token = '';              
  
  const APP_URL = import.meta.env.VITE_APP_URL || 'http://localhost:8000';
  const API_BASE = `${APP_URL}/api/dev`;

  onMount(() => {
    const savedToken = localStorage.getItem('authToken');
    if (savedToken) {
      token = savedToken;
      currentPage = 'dashboard';
    }
  });

  function handleNavigation(event) {
    currentPage = event.detail;
  }

  function handleAuthRedirect(event) {
    authMode = event.detail;
    currentPage = 'auth';
  }

  function handleLoginSuccess(event) {
    token = event.detail.token;
    localStorage.setItem('authToken', token);
    currentPage = 'dashboard';
  }

  function handleLogout() {
    token = '';
    localStorage.removeItem('authToken');
    currentPage = 'landing';
  }
</script>

<div class="app-layout">
  <Navbar {token} on:nav={handleNavigation} on:auth={handleAuthRedirect} on:logout={handleLogout} />

  <main class="main-content">
    {#if currentPage === 'landing'}
      <Landing {API_BASE} on:register={() => { authMode = 'register'; currentPage = 'auth'; }} />
    {:else if currentPage === 'auth'}
      <Auth {API_BASE} mode={authMode} on:loginSuccess={handleLoginSuccess} on:back={() => currentPage = 'landing'} />
    {:else if currentPage === 'dashboard'}
      <Dashboard {API_BASE} {token} />
    {:else if currentPage === 'docs'}
      <Documentation {APP_URL} />
    {/if}
  </main>

  <Footer on:nav={handleNavigation} />
</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    background-color: #0f172a; 
    font-family: system-ui, -apple-system, sans-serif;
  }

  .app-layout {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  .main-content {
    flex: 1 0 auto; 
    display: flex;
    flex-direction: column;
  }
</style>