<script>
  import { onMount } from 'svelte';
  import Login from './lib/Login.svelte';
  import Register from './lib/Register.svelte';
  import GameDetails from './lib/GameDetails.svelte';

  const API_BASE = 'http://localhost:8000/api';

  let token = localStorage.getItem('token') || '';
  let games = [];
  let gameName = '';
  
  let currentForm = 'login'; 
  let globalSuccessMessage = '';
  let selectedGameId = null;

  onMount(() => {
    if (token) loadGames();
  });

  function onLoginSuccess(event) {
    token = event.detail.token;
    localStorage.setItem('token', token);
    globalSuccessMessage = '';
    loadGames();
  }

  function onRegisterSuccess() {
    globalSuccessMessage = 'Account created successfully! You can now log in below.';
    currentForm = 'login';
  }

  async function loadGames() {
    try {
      const response = await fetch(`${API_BASE}/dev/games`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      if (response.ok) {
        games = data.games;
      } else {
        logout();
      }
    } catch (err) {
      console.error('Connection failed');
    }
  }

  async function createGame() {
    if (!gameName) return;
    try {
      const response = await fetch(`${API_BASE}/dev/games`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ game_name: gameName })
      });
      
      if (response.ok) {
        gameName = '';
        loadGames();
      }
    } catch (err) {
      console.error('Error creating game');
    }
  }

  function logout() {
    token = '';
    games = [];
    localStorage.removeItem('token');
  }
</script>

<svelte:head>
  <title>White Wolf</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
</svelte:head>

<div class="app-container">
  <header class="main-header">
    <div class="container navbar">
      <div class="logo">
        <span class="icon">🐺</span>
        <span class="brand">WHITE WOLF <small class="badge">SaaS</small></span>
      </div>
      {#if token}
        <button on:click={logout} class="outline contrast logout-btn">Logout</button>
      {/if}
    </div>
  </header>

 <main class="container body-content">
    {#if !token}
      <div class="auth-wrapper">
        {#if currentForm === 'login'}
          <Login 
            {API_BASE} 
            successMessage={globalSuccessMessage} 
            on:loginSuccess={onLoginSuccess} 
            on:switch={(e) => currentForm = e.detail} 
          />
        {:else}
          <Register 
            {API_BASE} 
            on:registerSuccess={onRegisterSuccess} 
            on:switch={(e) => currentForm = e.detail} 
          />
        {/if}
      </div>
    {:else}
      {#if selectedGameId}
        <GameDetails 
          {token} 
          {API_BASE} 
          gameId={selectedGameId} 
          onBack={() => selectedGameId = null} 
        />
      {:else} <div class="dashboard-grid">
          <div class="panel-card creation-panel">
            <h3>Register New Game</h3>
            <p class="panel-desc">Deploy a secure high-score tracking layout instantly.</p>
            
            <form on:submit|preventDefault={createGame}>
              <label for="game_name">Project Title</label>
              <input type="text" id="game_name" bind:value={gameName} placeholder="Cyberpunk Odyssey" required>
              <button type="submit" class="primary-action">Create Game</button>
            </form>
          </div>

          <div class="panel-card workspace-panel">
            <h3>Your Games</h3>
            
            <div class="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Project Name</th>
                    <th>Users</th>
                  </tr>
                </thead>
                <tbody>
                  {#each games as game}
                    <tr>
                      <td class="game-title">
                        <button on:click={() => selectedGameId = game.id} class="link-btn">
                          ✨ {game.game_name}
                        </button>
                      </td>
                      <td><code class="users-number">{game.current_users}/{game.max_users}</code></td>
                    </tr>
                  {:else}
                    <tr>
                      <td colspan="2" class="empty-state">No active projects found. Spin up a database cluster using the registration block.</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      {/if} {/if}
  </main>
</div>

<style>
  :global(body) {
    background-color: #0d1117 !important;
    color: #c9d1d9 !important;
    font-family: system-ui, -apple-system, sans-serif;
  }
  .link-btn {
    background: none !important;
    border: none !important;
    padding: 0 !important;
    color: #58a6ff !important;
    text-decoration: none;
    cursor: pointer;
    text-align: left;
    box-shadow: none !important;
  }
  .link-btn:hover {
    text-decoration: underline;
  }
  .app-container { min-height: 100vh; display: flex; flex-direction: column; }
  .main-header { background: #161b22; border-bottom: 1px solid #30363d; padding: 0.75rem 0; }
  .navbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0 !important; }
  .logo { display: flex; align-items: center; gap: 0.5rem; }
  .brand { font-size: 1.2rem; font-weight: 800; letter-spacing: 1px; color: #f0f6fc; }
  .badge { background: #1f6feb; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.65rem; vertical-align: middle; margin-left: 4px; }
  .logout-btn { padding: 0.4rem 1rem; font-size: 0.85rem; border-radius: 6px; margin-bottom: 0; }
  .body-content { flex: 1; padding-top: 3rem; padding-bottom: 3rem; }
  .auth-wrapper { display: flex; justify-content: center; align-items: center; padding: 2rem 0; }
  :global(.auth-card) { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 2.5rem; width: 100%; max-width: 480px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3); }
  :global(.auth-card h2) { color: #f0f6fc; margin-bottom: 0.25rem; font-weight: 700; }
  :global(.subtitle) { color: #8b949e; font-size: 0.9rem; margin-bottom: 2rem; }
  :global(.primary-action) { background: #238636; border: 1px solid #2ea44f; color: white; font-weight: 600; border-radius: 6px; transition: background 0.2s ease, transform 0.1s ease; margin-top: 1rem; }
  :global(.primary-action:hover) { background: #2ea44f; border-color: #3fb950; }
  :global(.primary-action:active) { transform: scale(0.98); }
  :global(.signup-color) { background: #1f6feb; border-color: #388bfd; }
  :global(.signup-color:hover) { background: #388bfd; border-color: #58a6ff; }
  :global(.switch-prompt) { text-align: center; margin-top: 1.5rem; font-size: 0.85rem; color: #8b949e; margin-bottom: 0; }
  :global(.switch-prompt a) { color: #58a6ff; text-decoration: none; font-weight: 500; }
  :global(.switch-prompt a:hover) { text-decoration: underline; }
  :global(.container) {max-width: 1400px !important;width: 95% !important;}
  .dashboard-grid { display: grid; grid-template-columns: 1fr; gap: 2rem; }
  @media (min-width: 992px) { .dashboard-grid { grid-template-columns: 320px 1fr; } }
  .panel-card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1.5rem; }
  .panel-card h3 { color: #f0f6fc; font-size: 1.2rem; font-weight: 600; margin-bottom: 0.25rem; }
  .panel-desc { color: #8b949e; font-size: 0.85rem; margin-bottom: 1.5rem; }
  .table-container { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; margin-bottom: 0; }
  th { color: #8b949e !important; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #21262d !important; padding: 0.75rem 1rem !important; }
  td { border-bottom: 1px solid #21262d !important; padding: 1rem !important; vertical-align: middle; }
  .game-title { font-weight: 600; color: #c9d1d9; }
  .user-number { font-family: 'SFMono-Regular', Consolas, monospace; font-size: 0.8rem; background: #0d1117 !important; border: 1px solid #30363d; padding: 4px 8px !important; border-radius: 6px; color: #58a6ff !important; display: inline-block; max-width: 240px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .token-snippet.secret { color: #ff7b72 !important; max-width: 320px; }
  .empty-state { text-align: center; color: #8b949e; font-style: italic; padding: 3rem !important; }
</style>