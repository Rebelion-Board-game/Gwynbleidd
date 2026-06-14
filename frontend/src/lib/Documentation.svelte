<script>
  export let APP_URL;

  $: apiDocsUrl = `${APP_URL}/docs/godot`
</script>

<div class="doc-container">
  <aside class="sidebar">
    <h3>Documentation</h3>
    <nav>
      <a href="#intro">Introduction</a>
      <a href="#setup">Setup</a>
      <a href="#auth">Authentication</a>
      <a href="#scores">Leaderboards</a>
      <div class="divider"></div>
      <a href={apiDocsUrl} target="_blank" class="api-link">🔗 API Reference</a>
    </nav>
  </aside>

  <main class="content">
    <section id="intro">
      <h2>Introduction</h2>
      <p>Gwynbleidd is a lightweight, open source backend solution for Godot 4. It provides a simple integration layer for handling player accounts and global leaderboards directly from your game project.</p>
    </section>

    <section id="setup">
      <h2>Setup</h2>
      <p>You can download Gwynbleidd plugin form godot AssetLib</p>
      <p>Add the integration script to your project as an Autoload (Singleton). After adding it, initialize the connection in your script using your unique Game ID and API keys:</p>
      <pre><code># Inside your main scene or game manager
func _ready():
    GwynbleiddApi.setup("YOUR_API_KEY", "YOUR_API_SECRET", YOUR_GAME_ID)</code></pre>
      <p>You can find your <strong>Game ID</strong>, <strong>API Key</strong>, and <strong>API Secret</strong> directly in the dashboard panel of your specific game.</p>
    
      <img src="/images/game_dashboard.png" alt="Dashboard configuration" class="doc-image" />
    </section>

    <section id="auth">
      <h2>Authentication</h2>
      <p>The system supports player registration and login. Methods are asynchronous and emit signals upon completion.</p>
      <pre><code># Register a new player
GwynbleiddApi.register_player("username", "password")

# Login an existing player
GwynbleiddApi.login_player("username", "password")

# Handle the result via signals
func _on_player_logged_in(success, data):
    if success:
        print("Token received: ", data["player_token"])</code></pre>
    </section>

    <section id="scores">
      <h2>Leaderboards</h2>
      <p>Scores are submitted with a SHA256 integrity hash to prevent tampering. You can fetch the leaderboard at any time.</p>
      <pre><code># Submit a score
GwynbleiddApi.submit_score("player_name", 2000)

# Fetch current leaderboard
GwynbleiddApi.fetch_leaderboard()

# Listen for results
func _on_leaderboard_loaded(success, scores):
    if success:
        for entry in scores:
            print(entry["player_name"], ": ", entry["score"])</code></pre>
    </section>
  </main>
</div>

<style>
  .doc-container {
    display: flex;
    max-width: 1200px;
    margin: 3rem auto;
    gap: 4rem;
    padding: 0 2rem;
    overflow: hidden;
  }

  .sidebar {
    width: 220px;
    flex: 0 0 220px;
    border-right: 1px solid #1e293b;
    padding-right: 2rem;
    position: sticky;
    top: 2rem;
    height: fit-content;
    }

  .sidebar h3 {
    color: #f8fafc;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748b;
  }

  .sidebar nav {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .sidebar a {
    color: #94a3b8;
    text-decoration: none;
    font-size: 0.95rem;
    transition: color 0.2s;
  }

  .sidebar a:hover {
    color: #38bdf8;
  }

  .divider {
    height: 1px;
    background: #1e293b;
    margin: 0.5rem 0;
  }

  .api-link {
    color: #38bdf8 !important;
    font-weight: 500;
  }

  .content {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 3rem;
  }

  pre {
    background: #0f172a;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #334155;
    overflow-x: auto;
    max-width: 100%;
    box-sizing: border-box;
    }

  code {
    font-family: 'Fira Code', monospace;
    color: #38bdf8;
    font-size: 0.9rem;
    word-break: break-all;
    white-space: pre-wrap;
    }

  h2 {
    color: #f8fafc;
    margin-bottom: 1rem;
    font-size: 1.75rem;
  }

  p {
    color: #cbd5e1;
    line-height: 1.7;
    margin-bottom: 1rem;
  }

  pre {
    background: #0f172a;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #334155;
    overflow-x: auto;
  }

  code {
    font-family: 'Fira Code', monospace;
    color: #38bdf8;
    font-size: 0.9rem;
  }

  :global(html) {
  scroll-behavior: smooth;
  }

  .doc-image {
  max-width: 100%;      
  height: auto;         
  display: block;      
  border-radius: 8px;
  border: 1px solid #334155;
  margin: 1.5rem 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  object-fit: contain;  
 }
</style>