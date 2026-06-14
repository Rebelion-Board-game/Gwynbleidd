<script>
  import { onMount } from 'svelte';
  import GameDetails from './GameDetails.svelte';

  export let token;
  export let API_BASE;

  let games = [];
  let gameName = '';
  let errorMessage = '';
  let selectedGameId = null;

  onMount(() => {
    if (token) loadGames();
  });

  async function loadGames() {
    try {
      const response = await fetch(`${API_BASE}/games`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      if (response.ok) {
        games = data.games;
      }
    } catch (err) {
      console.error('Connection failed');
    }
  }

  async function createGame() {
    if (!gameName) return;
    errorMessage = '';
    try {
      const response = await fetch(`${API_BASE}/games`, {
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
      } else {
        const errorData = await response.json();
        errorMessage = errorData.detail || 'Failed to create game.';
      }
    } catch (err) {
      errorMessage = 'Connection error.';
    }
  }

  async function deleteGame(gameId, name) {
    if (!confirm(`Delete "${name}"?`)) return;
    try {
      const response = await fetch(`${API_BASE}/games/${gameId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) loadGames();
    } catch (err) {
      console.error(err);
    }
  }
</script>

{#if selectedGameId}
  <GameDetails {token} {API_BASE} gameId={selectedGameId} onBack={() => selectedGameId = null} />
{:else}
  <div class="dashboard-grid container">
    <div class="panel-card creation-panel">
      <h3>Register New Game</h3>
      <p class="card-desc">Create a new project workspace. Maximum limit is 5 active games per developer account.</p>
      
      <form on:submit|preventDefault={createGame} class="create-form">
        <label for="game_name">Project Title</label>
        <input 
          type="text" 
          id="game_name" 
          bind:value={gameName} 
          placeholder="e.g. Cyberpunk Odyssey" 
          required
          class="modern-input"
        >
        
        {#if errorMessage}
          <p class="error-msg">{errorMessage}</p>
        {/if}
        
        <button type="submit" class="primary-action">Create Game</button>
      </form>
    </div>

    <div class="panel-card workspace-panel">
      <h3>Your Games</h3>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th class="col-name">Project Name</th>
              <th class="col-users">Users</th>
              <th class="col-actions">Actions</th>
            </tr>
          </thead>
          <tbody>
            {#each games as game}
              <tr>
                <td class="game-title col-name">
                  <button class="link-btn" on:click={() => selectedGameId = game.id}>
                    ✨ {game.game_name}
                  </button>
                </td>
                <td class="col-users">
                  <code class="user-number">{game.current_users ?? 0} / {game.max_users ?? 100}</code>
                </td>
                <td class="col-actions">
                  <button class="delete-btn" on:click={() => deleteGame(game.id, game.game_name)}>
                    🗑️
                  </button>
                </td>
              </tr>
            {:else}
              <tr>
                <td colspan="3" class="empty-state">No active projects found.</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  </div>
{/if}

<style>
  .container {
    width: 100%;
    max-width: 1440px;
    margin: 0 auto;
    padding: 2rem;
    box-sizing: border-box;
  }

  .dashboard-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  @media (min-width: 992px) {
    .dashboard-grid {
      grid-template-columns: 360px 1fr;
    }
  }

  .panel-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 2.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
  }

  .panel-card h3 {
    color: #f8fafc;
    font-size: 1.4rem;
    font-weight: 600;
    margin: 0 0 0.25rem 0;
  }

  .card-desc {
    color: #94a3b8;
    font-size: 0.95rem;
    margin: 0 0 2rem 0;
    line-height: 1.5;
  }

  .create-form {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  label {
    display: block;
    color: #cbd5e1;
    font-weight: 500;
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
  }

  .modern-input {
    background: #0f172a;
    border: 1px solid #475569;
    border-radius: 6px;
    color: #f8fafc;
    padding: 0.85rem 1rem;
    font-size: 0.95rem;
    outline: none;
    transition: border-color 0.2s;
  }

  .modern-input:focus {
    border-color: #818cf8;
  }

  .primary-action {
    background: #4f46e5;
    border: none;
    color: #ffffff;
    padding: 0.85rem 1.5rem;
    border-radius: 6px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
    margin-top: 1rem;
  }

  .primary-action:hover {
    background: #4338ca;
  }

  .table-container {
    overflow-x: auto;
    margin-top: 1rem;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
  }

  th, td {
    padding: 1rem 0;
    box-sizing: border-box;
    vertical-align: middle;
  }

  th {
    color: #94a3b8;
    font-weight: 500;
    font-size: 0.9rem;
    border-bottom: 1px solid #334155;
    padding-bottom: 1rem;
  }

  td {
    border-bottom: 1px solid #334155;
  }

  tr:last-child td {
    border-bottom: none;
  }

  .col-name {
    text-align: left;
    width: auto;
    padding-left: 0.5rem;
  }

  .col-users {
    text-align: center;
    width: 140px;
  }

  .col-actions {
    text-align: right;
    width: 100px;
    padding-right: 0.5rem;
  }

  .link-btn {
    background: none;
    border: none;
    padding: 0;
    color: #38bdf8;
    font-size: 1.05rem;
    text-decoration: none;
    cursor: pointer;
    text-align: left;
    font-weight: 600;
    transition: color 0.2s;
    display: inline-block;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .link-btn:hover {
    color: #818cf8;
  }

  .user-number {
    font-family: monospace;
    font-size: 0.85rem;
    background: #0f172a;
    border: 1px solid #475569;
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
    color: #38bdf8;
    display: inline-block;
  }

  .delete-btn {
    background: transparent;
    border: 1px solid #ef4444;
    color: #fca5a5;
    padding: 0.4rem 0.75rem;
    font-size: 0.9rem;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .delete-btn:hover {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
  }

  .empty-state {
    text-align: center;
    color: #64748b;
    font-style: italic;
    padding: 3rem;
  }

  .error-msg {
    color: #fca5a5;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.2);
    padding: 0.75rem;
    border-radius: 6px;
    font-size: 0.9rem;
    margin-top: 0.5rem;
  }
</style>