<script>
  import { onMount } from 'svelte';
  import LeaderboardManager from './LeaderboardManager.svelte';
  import UsersManager from './UsersManager.svelte';
  import SaveDataManager from './SaveDataManager.svelte';

  export let token;
  export let API_BASE;
  export let gameId;
  export let onBack;

  let gameDetails = null;
  let loading = true;
  let errorMessage = ''; 
  let apiKey = ''; 
  let showApiKey = false; 

  let apiSecret = ''; 
  let showApiSecret = false; 

  let regenerating = false;  
  let loadingKey = false;
  let copied = false;
  let copiedSecret = false;

  // State to manage active tab
  let activeTab = 'credentials'; 

  onMount(async () => {
    try {
      const response = await fetch(`${API_BASE}/games`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      if (response.ok) {
        gameDetails = data.games.find(g => g.id === gameId);
      }
    } catch (err) {
      errorMessage = 'Could not load workspace.';
    } finally {
      loading = false;
    }
  });

  async function fetchKeyIfNeeded(type) {
    const cache = type === 'secret' ? apiSecret : apiKey;
    if (cache) return true;
    
    loadingKey = true;
    try {
        const url = `${API_BASE}/games/${gameId}/api_${type === 'secret' ? 'secret' : 'key'}`;
        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.detail || `Failed to fetch API ${type}.`);
            return false;
        }
        
        if (type === 'secret') {
            apiSecret = data.api_secret;
        } else {
            apiKey = data.api_key;
        }
        return true;
        
    } catch (err) {
        alert(`Network error while fetching API ${type}.`);
        return false;
    } finally {
        loadingKey = false;
    }
  }

  async function toggleRevealApiKey() {
    showApiKey = showApiKey ? false : await fetchKeyIfNeeded('key');
  }

  async function toggleRevealApiSecret() {
    showApiSecret = showApiSecret ? false : await fetchKeyIfNeeded('secret');
  }

  async function handleCopy() {
    const success = await fetchKeyIfNeeded('key');
    if (!success) return;

    try {
      await navigator.clipboard.writeText(apiKey);
      copied = true;
      setTimeout(() => { copied = false; }, 1500);
    } catch (err) {
      alert('Failed to copy text to clipboard.');
    }
  }
  
  async function handleCopySecret() {
    const success = await fetchKeyIfNeeded('secret');
    if (!success) return;

    try {
      await navigator.clipboard.writeText(apiSecret);
      copiedSecret = true;
      setTimeout(() => { copiedSecret = false; }, 1500);
    } catch (err) {
      alert('Failed to copy secret to clipboard.');
    }
  }

  async function handleRegenerate() {
    const confirmed = confirm(
      "Are you absolutely sure you want to revoke this API key? Any applications currently using this key will immediately stop working!"
    );
    
    if (!confirmed) return; 

    regenerating = true;
    try {
      const response = await fetch(`${API_BASE}/games/${gameId}/api_key_regenerate`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.status === 204) {
        alert("API Key successfully revoked and regenerated!");
        apiKey = ''; 
        showApiKey = false;
        await toggleRevealApiKey(); 
      } else {
        const data = await response.json().catch(() => ({}));
        alert(data.detail || "Failed to regenerate API key.");
      }
    } catch (err) {
      alert("Network error during API key regeneration.");
    } finally {
      regenerating = false;
    }
  }
</script>

<div class="workspace-container">
  <div class="top-nav">
    <button on:click={onBack} class="back-btn">
      ← Back to Dashboard
    </button>
  </div>

  {#if loading}
    <div class="loading-state">Loading game workspace...</div>
  {:else if errorMessage}
    <div class="error-state">{errorMessage}</div>
  {:else}
    {#if gameDetails}
      <header class="game-header">
        <h2>🎮 {gameDetails.game_name}</h2>
        <p class="subtitle">Game ID: <code>{gameDetails.id}</code></p>
      </header>

      <div class="tabs-nav">
        <button class="tab-link" class:active={activeTab === 'credentials'} on:click={() => activeTab = 'credentials'}>
          🔑 Credentials
        </button>
        <button class="tab-link" class:active={activeTab === 'users'} on:click={() => activeTab = 'users'}>
          👥 Users Manager
        </button>
        <button class="tab-link" class:active={activeTab === 'leaderboard'} on:click={() => activeTab = 'leaderboard'}>
          🏆 Leaderboard
        </button>
        <button class="tab-link" class:active={activeTab === 'saves'} on:click={() => activeTab = 'saves'}>
          💾 Player Saves
        </button>
      </div>

      <div class="tab-content">
        {#if activeTab === 'credentials'}
          <section class="panel-card credentials-card">
            <h3>Security Credentials</h3>
            <p class="card-desc">Use these credentials inside your Godot project configuration.</p>
            
            <div class="credential-group">
              <label for="api_key">API Key</label>
              <div class="credential-wrapper">
                <input 
                  type={showApiKey ? "text" : "password"} 
                  id="api_key" 
                  value={apiKey || "••••••••••••••••••••••••••••••••"} 
                  readonly 
                  class="secure-input"
                >
                <button type="button" class="action-btn" disabled={loadingKey || regenerating} on:click={handleCopy}>
                  {copied ? "Copied!" : "Copy"}
                </button>
                <button type="button" class="action-btn" disabled={loadingKey} on:click={toggleRevealApiKey}>
                  {showApiKey ? "Hide" : "Reveal"}
                </button>
              </div>
              <div class="revoke-container">
                <button type="button" class="revoke-btn" disabled={regenerating} on:click={handleRegenerate}>
                  {regenerating ? "Regenerating..." : "Revoke & Regenerate Key"}
                </button>
              </div>
            </div>

            <div class="credential-group">
              <label for="api_secret">API Secret</label>
              <div class="credential-wrapper">
                <input 
                  type={showApiSecret ? "text" : "password"} 
                  id="api_secret" 
                  value={apiSecret || "••••••••••••••••••••••••••••••••"} 
                  readonly 
                  class="secure-input"
                >
                <button type="button" class="action-btn" disabled={loadingKey || regenerating} on:click={handleCopySecret}>
                  {copiedSecret ? "Copied!" : "Copy"}
                </button>
                <button type="button" class="action-btn" disabled={loadingKey} on:click={toggleRevealApiSecret}>
                  {showApiSecret ? "Hide" : "Reveal"}
                </button>
              </div>
            </div>
          </section>
        {/if}

        {#if activeTab === 'users'}
          <div class="panel-card main-content-panel">
            <UsersManager {token} {API_BASE} {gameId} />
          </div>
        {/if}

        {#if activeTab === 'leaderboard'}
          <div class="panel-card main-content-panel">
            <LeaderboardManager {token} {API_BASE} {gameId} />
          </div>
        {/if}

        {#if activeTab === 'saves'}
          <div class="panel-card main-content-panel">
            <SaveDataManager {token} {API_BASE} {gameId} />
          </div>
        {/if}
      </div>
    {:else}
      <div class="error-state">Game workspace not found.</div>
    {/if}
  {/if}
</div>

<style>
  .workspace-container {
    width: 100%;
    max-width: 1440px;
    margin: 0 auto;
    padding: 2rem 2rem 4rem 2rem;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .top-nav {
    display: flex;
    justify-content: flex-start;
  }

  .back-btn {
    background: none;
    border: 1px solid #475569;
    color: #cbd5e1;
    padding: 0.5rem 1.25rem;
    font-size: 0.9rem;
    font-weight: 500;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .back-btn:hover {
    background-color: #1e293b;
    color: #f8fafc;
    border-color: #64748b;
  }

  .game-header {
    margin-bottom: 0.5rem;
  }

  .game-header h2 {
    color: #f8fafc;
    font-size: 2rem;
    margin: 0 0 0.5rem 0;
  }

  .subtitle {
    color: #94a3b8;
    margin: 0;
    font-size: 0.95rem;
  }

  .subtitle code {
    background: #1e293b;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    color: #f1f5f9;
  }

  /* Tabs Navigation Styling */
  .tabs-nav {
    display: flex;
    gap: 0.5rem;
    border-bottom: 2px solid #334155;
    padding-bottom: 2px;
  }

  .tab-link {
    background: none;
    border: none;
    color: #94a3b8;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    border-radius: 6px 6px 0 0;
    transition: all 0.2s ease;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
  }

  .tab-link:hover {
    color: #f1f5f9;
    background: #1e293b;
  }

  .tab-link.active {
    color: #38bdf8;
    border-bottom: 2px solid #38bdf8;
    background: #1e293b;
  }

  .tab-content {
    width: 100%;
  }

  .panel-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 2.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  }

  .credentials-card h3 {
    color: #f8fafc;
    margin: 0 0 0.25rem 0;
    font-size: 1.4rem;
  }

  .card-desc {
    color: #94a3b8;
    margin: 0 0 2rem 0;
    font-size: 0.95rem;
  }

  .credential-group {
    margin-bottom: 2rem;
  }

  .credential-group:last-child {
    margin-bottom: 0;
  }

  label {
    display: block;
    color: #cbd5e1;
    font-weight: 500;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
  }

  .credential-wrapper {
    display: flex;
    align-items: center;
    background: #0f172a;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 0.25rem;
    overflow: hidden;
  }

  .secure-input {
    background: transparent !important;
    border: none !important;
    outline: none !important;
    flex: 1;
    font-family: monospace;
    font-size: 0.95rem;
    color: #38bdf8 !important;
    padding: 0.6rem 1rem !important;
  }

  .action-btn {
    background: #1e293b;
    border: 1px solid #475569;
    color: #cbd5e1;
    padding: 0.4rem 1rem;
    font-size: 0.85rem;
    font-weight: 500;
    border-radius: 4px;
    margin-right: 0.25rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .action-btn:hover:not(:disabled) {
    background: #0f172a;
    color: #f8fafc;
    border-color: #64748b;
  }

  .revoke-container {
    margin-top: 0.5rem;
    display: flex;
    justify-content: flex-end;
  }

  .revoke-btn {
    background: transparent;
    border: 1px solid #ef4444;
    color: #fca5a5;
    padding: 0.35rem 0.85rem;
    font-size: 0.8rem;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .revoke-btn:hover:not(:disabled) {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
  }

  .main-content-panel {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .loading-state, .error-state {
    text-align: center;
    color: #94a3b8;
    padding: 4rem;
    font-size: 1.1rem;
  }

  .error-state {
    color: #f87171;
  }
</style>