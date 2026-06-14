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
      const response = await fetch(`${API_BASE}/games/${gameId}/users`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      
      if (response.ok) {
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

  async function deletePlayer(playerId, username) {
    if (!confirm(`Permanently delete player "${username}"?`)) return;

    try {
      const response = await fetch(`${API_BASE}/games/${gameId}/players/${playerId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        await fetchUsers();
      } else {
        const errorData = await response.json();
        errorMessage = errorData.detail || 'Failed to delete player.';
      }
    } catch (err) {
      errorMessage = 'Network error while deleting player.';
    }
  }
</script>

<div class="manager-container">
  <div class="header">
    <h3>👥 Registered Players</h3>
  </div>

  {#if errorMessage}
    <p class="error-msg">{errorMessage}</p>
  {/if}

  {#if loading}
    <div class="loading">Loading players...</div>
  {:else if users.length === 0}
    <div class="empty-state">No players found for this game yet.</div>
  {:else}
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th class="col-username">Username</th>
            <th class="col-login">Last Login</th>
            <th class="col-created">Created At</th>
            <th class="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each users as user}
            <tr>
              <td class="col-username player-name">{user.username}</td>
              <td class="col-login date-cell">{user.last_login ? new Date(user.last_login).toLocaleString() : 'Never'}</td>
              <td class="col-created date-cell">{user.created_at ? new Date(user.created_at).toLocaleString() : 'N/A'}</td>
              <td class="col-actions text-right">
                <button on:click={() => deletePlayer(user.id, user.username)} class="delete-btn">
                  🗑️
                </button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>

<style>
  .manager-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .header h3 {
    margin: 0;
    color: #f8fafc;
    font-size: 1.25rem;
  }

  .table-wrapper {
    overflow-x: auto;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
    table-layout: fixed;
  }

  th {
    color: #94a3b8;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #334155;
    font-weight: 500;
  }

  td {
    padding: 0.75rem 1rem;
    color: #cbd5e1;
    border-bottom: 1px solid #334155;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  tr:last-child td { border-bottom: none; }

  .col-username { width: 25%; text-align: left; }
  .col-login { width: 30%; text-align: left; }
  .col-created { width: 30%; text-align: left; }
  .col-actions { width: 15%; text-align: right; }

  .player-name { font-weight: 600; color: #38bdf8; }
  .date-cell { color: #94a3b8; font-size: 0.85rem; font-family: monospace; }
  .text-right { text-align: right; }

  .delete-btn {
    background: transparent;
    border: 1px solid #475569;
    padding: 0.3rem 0.6rem;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .delete-btn:hover {
    background: rgba(239, 68, 68, 0.1);
    border-color: #ef4444;
  }

  .error-msg {
    color: #fca5a5;
    background: rgba(239, 68, 68, 0.1);
    padding: 0.75rem;
    border-radius: 6px;
    border: 1px solid rgba(239, 68, 68, 0.2);
  }

  .loading, .empty-state {
    padding: 2rem;
    text-align: center;
    color: #94a3b8;
    background: #0f172a;
    border-radius: 8px;
    border: 1px solid #334155;
  }
</style>