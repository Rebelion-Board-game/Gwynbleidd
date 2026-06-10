<script>
  import { onMount } from 'svelte';
  import LeaderboardManager from './LeaderboardManager.svelte';
  import UsersManager from './UsersManager.svelte';
    import { nonpassive } from 'svelte/legacy';

  // Component props received from parent component
  export let token;
  export let API_BASE;
  export let gameId;
  export let onBack; // Callback function to return to the dashboard list

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

  onMount(async () => {
    try {
      const response = await fetch(`${API_BASE}/dev/games`, {
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
        const url = `${API_BASE}/dev/games/${gameId}/api_${type === 'secret' ? 'secret' : 'key'}`;
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
    const success = await fetchKeyIfNeeded();
    if (!success) return;

    try {
      await navigator.clipboard.writeText(apiKey);
      copied = true;

      setTimeout(() => {
        copied = false;
      }, 1500);
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

      setTimeout(() => {
        copiedSecret = false;
      }, 1500);
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
      const response = await fetch(`${API_BASE}/dev/games/${gameId}/api_key_regenerate`, {
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


<div class="panel-card">
  <button on:click={onBack} class="outline secondary" style="margin-bottom: 1.5rem; width: auto;">
    ← Back to Dashboard
  </button>

  {#if loading}
    <p aria-busy="true">Loading game workspace...</p>
  {:else}
    {#if gameDetails}
      <h2>🎮 {gameDetails.game_name}</h2>
      <p class="subtitle">Game ID: <code>{gameDetails.id}</code></p>
      
      <hr />

      <div class="credentials-section">
        <label for="api_key">API Key</label>
        <div class="credential-wrapper">
          <input 
            type={showApiKey ? "text" : "password"} 
            id="f" 
            value={apiKey || "No key returned from database"} 
            readonly 
            class="secure-input"
          >

          <button 
            type="button" 
            class="outline contrast reveal-btn"
            disabled={loadingKey || regenerating}
            on:click={handleCopy}
          >
            {copied ? "Copied!" : "Copy"}
          </button>

          <button 
            type="button" 
            class="outline contrast reveal-btn"
            disabled={loadingKey}
            on:click={toggleRevealApiKey}
          >
            {showApiKey ? "Hide" : "Reveal"}
          </button>

        </div>

        <div style="margin-top: 1rem; text-align: right;">
          <button 
            type="button" 
            class="outline secondary revoke-btn"
            disabled={regenerating}
            on:click={handleRegenerate}
          >
            {regenerating ? "Regenerating..." : "Revoke & Regenerate Key"}
          </button>
        </div>

        <label for="api_secret">API SECRET</label>
        <div class="credential-wrapper">
          <input 
            type={showApiSecret ? "text" : "password"} 
            id="f" 
            value={apiSecret || "No secret returned from database"} 
            readonly 
            class="secure-input"
          >

          <button 
            type="button" 
            class="outline contrast reveal-btn"
            disabled={loadingKey || regenerating}
            on:click={handleCopySecret}
          >
            {copied ? "Copied!" : "Copy"}
          </button>

          <button 
            type="button" 
            class="outline contrast reveal-btn"
            disabled={loadingKey}
            on:click={toggleRevealApiSecret}
          >
            {showApiSecret ? "Hide" : "Reveal"}
          </button>

        </div>

        <div class="panels-container">
          <div class="main-content-panel">
            <UsersManager {token} {API_BASE} {gameId} />
          </div>

          <div class="main-content-panel">
            <LeaderboardManager {token} {API_BASE} {gameId} />
          </div>
        </div>

      </div>
    {:else}
      <p>Game workspace not found.</p>
    {/if}
  {/if}
</div>

<style>
  /* Container layout to bind the input and button together */
  .credential-wrapper {
    display: flex;
    gap: 0; /* Clean attached look */
    align-items: center;
    background: #0d1117 !important; /* Matches background to look like text snippet */
    border: 1px solid #30363d;
    border-radius: 6px;
    padding-right: 8px;
    overflow: hidden;
  }

  /* Removes the input field styling to make it look like a secure token snippet */
  .secure-input {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    margin-bottom: 0 !important;
    flex: 1;
    font-family: 'SFMono-Regular', Consolas, monospace;
    font-size: 0.9rem;
    color: #58a6ff !important;
    padding: 0.75rem 1rem !important;
    user-select: all; /* Allows easy double-click copying */
  }

  /* Compact button styling inside the component wrapper */
  .reveal-btn {
    width: auto !important;
    padding: 0.4rem 1rem !important;
    margin-bottom: 0 !important;
    font-size: 0.8rem !important;
    border-radius: 4px !important;
  }

  .main-content-panel {
    padding-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

</style>