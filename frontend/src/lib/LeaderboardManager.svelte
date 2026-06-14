<script>
  import { onMount } from 'svelte';

  export let token;
  export let API_BASE;
  export let gameId;

  let scores = [];
  let loading = true;
  let errorMessage = '';

  onMount(async () => {
    await fetchScores();
  });

  async function fetchScores() {
    loading = true;
    errorMessage = '';
    try {
      const response = await fetch(`${API_BASE}/games/${gameId}/scores`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      
      if (response.ok) {
        scores = data.scores || [];
      } else {
        errorMessage = data.detail || 'Failed to load scores.';
      }
    } catch (err) {
      errorMessage = 'Network error while fetching scores.';
    } finally {
      loading = false;
    }
  }
</script>

<div class="manager-container">
  <div class="header">
    <h3>🏆 Top Scores</h3>
  </div>

  {#if errorMessage}
    <p class="error-msg">{errorMessage}</p>
  {/if}

  {#if loading}
    <div class="loading">Loading leaderboard...</div>
  {:else if scores.length === 0}
    <div class="empty-state">No scores submitted yet.</div>
  {:else}
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th class="col-rank">Rank</th>
            <th class="col-name">Player</th>
            <th class="col-score">Score</th>
            <th class="col-date">Submitted At</th>
          </tr>
        </thead>
        <tbody>
          {#each scores as entry, index}
            <tr>
              <td class="col-rank">#{index + 1}</td>
              <td class="col-name player-name">{entry.player_name}</td>
              <td class="col-score score-value">{entry.score}</td>
              <td class="col-date date-cell">{new Date(entry.timestamp).toLocaleString()}</td>
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

  .col-rank { width: 15%; text-align: left; }
  .col-name { width: 30%; text-align: left; }
  .col-score { width: 20%; text-align: left; }
  .col-date { width: 35%; text-align: left; }

  .player-name { font-weight: 600; color: #f1f5f9; }
  .score-value { font-weight: 700; color: #38bdf8; font-family: monospace; }
  .date-cell { color: #94a3b8; font-size: 0.85rem; font-family: monospace; }

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