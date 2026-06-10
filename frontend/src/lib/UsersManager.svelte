<script>
  import { onMount } from 'svelte';

  export let token;
  export let API_BASE;
  export let gameId;

  let users = [];
  let loading = true;
  let errorMessage = '';

  onMount(async () => {
    await fetchUsers();
  });

  async function fetchUsers() {
    loading = true;
    errorMessage = '';
    try {
      const response = await fetch(`${API_BASE}/${gameId}/users`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      
      if (response.ok) {
        // Endpoint zwraca {"users": rows}
        users = data.users || [];
      } else {
        errorMessage = data.detail || 'Failed to load users.';
      }
    } catch (err) {
      errorMessage = 'Network error while fetching users.';
    } finally {
      loading = false;
    }
  }
</script>

<div class="leaderboard-manager">
  <div class="board-header">
    <h3>👥 Players</h3>
  </div>

  {#if errorMessage}
    <p class="error-msg">❌ {errorMessage}</p>
  {/if}

  {#if loading}
    <p aria-busy="true">Loading players data...</p>
  {:else}
    {#if users.length === 0}
      <div class="empty-state">
        <p>No players found for this game yet.</p>
      </div>
    {:else}
      <table class="striped">
        <thead>
          <tr>
            <th>Username</th>
            <th>Last Login</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          {#each users as user}
            <tr>
              <td><span class="player-name">{user.username}</span></td>
              <td>
                <small>
                  {user.last_login ? new Date(user.last_login).toLocaleString() : 'Never'}
                </small>
              </td>
              <td>
                <small>
                  {user.created_at ? new Date(user.created_at).toLocaleString() : 'N/A'}
                </small>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  {/if}
</div>

<style>
  .muted {
    color: #8b949e;
  }
  .subtitle {
    margin-top: -0.5rem;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
  }
  .empty-state {
    text-align: center;
    padding: 2.5rem;
    background: #161b22;
    border-radius: 6px;
    color: #8b949e;
    border: 1px dashed #30363d;
  }
  .player-name {
    font-weight: 500;
    color: #c9d1d9;
  }
  .error-msg {
    color: #f85149;
    background: rgba(248, 81, 73, 0.1);
    padding: 0.75rem;
    border-radius: 6px;
    border: 1px solid rgba(248, 81, 73, 0.2);
    margin-bottom: 1rem;
  }
</style>