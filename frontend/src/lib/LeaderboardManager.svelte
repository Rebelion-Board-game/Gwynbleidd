<script>
  import { onMount } from 'svelte';

  export let token;
  export let API_BASE;
  export let gameId;

  // Stany komponentu
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
      const response = await fetch(`${API_BASE}/${gameId}/scores`, {
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

<div class="leaderboard-manager">
  <div class="board-header">
    <h3>🏆 Top Scores</h3>
    <p class="muted subtitle">Live leaderboard</p>
  </div>

  {#if errorMessage}
    <p class="error-msg">❌ {errorMessage}</p>
  {/if}

  {#if loading}
    <p aria-busy="true">Loading leaderboard data...</p>
  {:else}
    {#if scores.length === 0}
      <div class="empty-state">
        <p>No scores submitted yet. Connect your Godot game using the API Key to post the first score!</p>
      </div>
    {:else}
      <table class="striped">
        <thead>
          <tr>
            <th style="width: 80px;">Rank</th>
            <th>Player Name</th>
            <th>Score</th>
            <th>Submitted At</th>
          </tr>
        </thead>
        <tbody>
          {#each scores as entry, index}
            <tr>
              <td><strong>#{index + 1}</strong></td>
              <td><span class="player-name">{entry.player_name}</span></td>
              <td><span class="score-value">{entry.score}</span></td>
              <td><small>{new Date(entry.timestamp).toLocaleString()}</small></td>
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
  .score-value {
    font-family: 'SFMono-Regular', Consolas, monospace;
    font-size: 1rem;
    color: #58a6ff;
    font-weight: bold;
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