<script>
  import { onMount } from 'svelte';

  export let token;
  export let API_BASE;
  export let gameId;

  let saves = [];
  let loading = true;
  let errorMessage = '';
  
  let selectedPlayerId = null;
  let rawJsonView = null;

  onMount(async () => {
    await fetchSaves();
  });

  async function fetchSaves() {
    loading = true;
    errorMessage = '';
    try {
      const response = await fetch(`${API_BASE}/games/${gameId}/saves`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      
      if (response.ok) {
        saves = data.saves || [];
      } else {
        errorMessage = data.detail || 'Failed to load player saves.';
      }
    } catch (err) {
      errorMessage = 'Network error while fetching saves.';
    } finally {
      loading = false;
    }
  }

  function viewRawJson(player_id, rawData) {
    if (selectedPlayerId === player_id) {
      // Close inspector if clicking the same player again
      selectedPlayerId = null;
      rawJsonView = null;
    } else {
      selectedPlayerId = player_id;
      // Format JSON with 2-space indentation
      rawJsonView = JSON.stringify(rawData, null, 2);
    }
  }
</script>

<div class="manager-container">
  <div class="header">
    <h3>💾 Player Save Files</h3>
  </div>

  {#if errorMessage}
    <p class="error-msg">{errorMessage}</p>
  {/if}

  {#if loading}
    <div class="loading">Loading saves...</div>
  {:else if saves.length === 0}
    <div class="empty-state">No save states found for this game.</div>
  {:else}
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th class="col-id">Player ID</th>
            <th class="col-username">Username</th>
            <th class="col-date">Last Saved At</th>
            <th class="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each saves as entry}
            <tr class:row-active={selectedPlayerId === entry.player_id}>
              <td class="col-id font-mono">#{entry.player_id}</td>
              <td class="col-username username-value">{entry.username}</td>
              <td class="col-date date-cell">{new Date(entry.updated_at).toLocaleString()}</td>
              <td class="col-actions">
                <button class="inspect-btn" on:click={() => viewRawJson(entry.player_id, entry.data)}>
                  {selectedPlayerId === entry.player_id ? "Hide Data" : "Inspect JSON"}
                </button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    {#if selectedPlayerId && rawJsonView}
      <div class="json-inspector">
        <h4>📋 Raw JSON Save State (Player #{selectedPlayerId})</h4>
        <pre><code>{rawJsonView}</code></pre>
      </div>
    {/if}
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
    vertical-align: middle;
  }

  tr:last-child td { border-bottom: none; }
  tr.row-active td { background-color: rgba(56, 189, 248, 0.05); }

  .col-id { width: 15%; text-align: left; }
  .col-username { width: 35%; text-align: left; }
  .col-date { width: 30%; text-align: left; }
  .col-actions { width: 20%; text-align: right; }

  .font-mono { font-family: monospace; color: #64748b; }
  .username-value { font-weight: 600; color: #f1f5f9; }
  .date-cell { color: #94a3b8; font-size: 0.85rem; font-family: monospace; }

  .inspect-btn {
    background: #1e293b;
    border: 1px solid #475569;
    color: #cbd5e1;
    padding: 0.35rem 0.75rem;
    font-size: 0.8rem;
    font-weight: 500;
    border-radius: 4px;
    margin-right: 0.25rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .inspect-btn:hover {
    background: #0f172a;
    color: #38bdf8;
    border-color: #38bdf8;
  }

  .json-inspector {
    margin-top: 1rem;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 1.5rem;
  }

  .json-inspector h4 {
    margin: 0 0 0.75rem 0;
    color: #38bdf8;
    font-size: 0.95rem;
  }

  pre {
    background: #020617;
    border: 1px solid #1e293b;
    padding: 1rem;
    border-radius: 6px;
    overflow-x: auto;
    margin: 0;
    max-height: 400px;
  }

  code {
    font-family: monospace;
    font-size: 0.85rem;
    color: #a7f3d0;
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