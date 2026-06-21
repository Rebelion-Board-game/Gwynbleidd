<script>
  import { onMount } from 'svelte';

  export let APP_URL;

  $: apiDocsUrl = `${APP_URL}/docs/godot`

  onMount(() => {
    if (typeof window !== 'undefined' && window.Prism) {
      window.Prism.highlightAll();
    }
  });
</script>

<svelte:head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-gdscript.min.js"></script>
</svelte:head>

<div class="doc-container">
  <aside class="sidebar">
    <h3>Documentation</h3>
    <nav>
      <a href="#intro">Introduction</a>
      <a href="#setup">Setup</a>
      <a href="#auth">Authentication</a>
      <a href="#scores">Leaderboards</a>
      <a href="#saves">Cloud Saves</a>
      <div class="divider"></div>
      <a href={apiDocsUrl} target="_blank" class="api-link">🔗 API Reference</a>
    </nav>
  </aside>

  <main class="content">
    <section id="intro">
      <h2>Introduction</h2>
      <p>Gwynbleidd is a lightweight, open-source backend solution for Godot 4. It provides a simple integration layer for handling player accounts, global leaderboards, and cloud save states directly from your game project.</p>
    </section>

    <section id="setup">
      <h2>Setup</h2>
      <p>You can download the Gwynbleidd plugin directly from the Godot AssetLib or clone it from <a href="https://github.com/Rebelion-Board-game/Gwynbleidd-godot-plugin" target="_blank" class="api-link">GitHub</a>.</p>
      <p>Add the integration script to your project as an Autoload (Singleton). After adding it, initialize the connection in your script using your unique Game ID and API keys:</p>
      
      <div class="code-block" data-lang="GDScript">
        <pre><code class="language-gdscript"># Initialize the API helper in your main scene or game manager
func _ready():
    GwynbleiddApi.setup("YOUR_API_KEY", "YOUR_API_SECRET", YOUR_GAME_ID)</code></pre>
      </div>

      <p>You can find your <strong>Game ID</strong>, <strong>API Key</strong>, and <strong>API Secret</strong> directly in the dashboard panel of your specific game.</p>
      <img src="/images/game_dashboard.png" alt="Dashboard configuration" class="doc-image" />
    </section>

    <section id="auth">
      <h2>Authentication</h2>
      <p>The system supports player registration and login. Methods are asynchronous and emit signals upon completion.</p>
      
      <div class="code-block" data-lang="GDScript">
        <pre><code class="language-gdscript"># Register a new player account
GwynbleiddApi.register_player("username", "password")

# Login an existing player to get a JWT token
GwynbleiddApi.login_player("username", "password")

# Handle the result via autoload signals
func _on_player_logged_in(success, data):
    if success:
        print("Session token received: ", data["player_token"])</code></pre>
      </div>
    </section>

    <section id="scores">
      <h2>Leaderboards</h2>
      <p>Scores are submitted with a SHA256 integrity hash to prevent client-side tampering. You can fetch the leaderboard rows at any time.</p>
      
      <div class="code-block" data-lang="GDScript">
        <pre><code class="language-gdscript"># Submit a score safely
GwynbleiddApi.submit_score("player_name", 2000)

# Fetch current top leaderboards
GwynbleiddApi.fetch_leaderboard()

# Listen for results using callbacks
func _on_leaderboard_loaded(success, scores):
    if success:
        for entry in scores:
            print(entry["player_name"], ": ", entry["score"])</code></pre>
      </div>
    </section>

    <section id="saves">
      <h2>Cloud Saves</h2>
      <p>Store and retrieve full game state objects securely in the cloud. Cloud save operations require an authorized player session.</p>
      
      <div class="code-block" data-lang="GDScript">
        <pre><code class="language-gdscript"># Prepare save state data as a Dictionary
var save_state = &#123;
    "level": 14,
    "gold": 420,
    "inventory": ["silver_sword", "swallow_potion"]
&#125;

# Push current state data up to the cloud save endpoint
GwynbleiddApi.save_game_data(save_state)

# Request the last cloud save block back down
GwynbleiddApi.load_game_data()

# Handle game state response data inside your listener
func _on_game_loaded(success, response):
    if success:
        var data = response.get("data", &#123;&#125;)
        print("Loaded gold count from cloud: ", data.get("gold", 0))</code></pre>
      </div>
      
      <div class="info-note">
        <p>💡 <strong>Looking for a full runtime execution workflow?</strong> Check out the complete <code>https://github.com/Rebelion-Board-game/Gwynbleidd-godot-plugin/blob/main/Example.gd</code> script included directly in our GitHub plugin repository to see the full, step-by-step registration, sequential login validation, and save-state lifecycle in action.</p>
      </div>
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

  .code-block {
    position: relative;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 12px;
    margin: 1.5rem 0;
    padding-top: 2.5rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    overflow: hidden;
  }

  .code-block::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2.5rem;
    background: #161b22;
    border-bottom: 1px solid #30363d;
    z-index: 2;
  }

  .code-block pre::before {
    content: '';
    position: absolute;
    top: 0.85rem;
    left: 1.25rem;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #ff5f56;
    box-shadow: 18px 0 0 #ffbd2e, 36px 0 0 #27c93f;
    z-index: 3;
  }

  .code-block::after {
    content: attr(data-lang);
    position: absolute;
    top: 0.7rem;
    right: 1.25rem;
    font-size: 0.7rem;
    font-family: ui-monospace, monospace;
    color: #8b949e;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    z-index: 3;
  }

  pre {
    margin: 0;
    padding: 1rem 1.5rem 1.5rem 1.5rem;
    overflow-x: auto;
    max-width: 100%;
    box-sizing: border-box;
    background: transparent;
  }

  code {
    font-family: 'Fira Code', 'JetBrains Mono', ui-monospace, monospace;
    font-size: 0.875rem;
    line-height: 1.7;
    white-space: pre;
    tab-size: 4;
    word-break: normal;
    display: block;
    position: relative;
    z-index: 1;
  }

  .code-block code .token.comment { color: #8b949e; font-style: italic; }
  .code-block code .token.keyword { color: #ff7b72; }
  .code-block code .token.string { color: #a5d6ff; }
  .code-block code .token.function { color: #d2a8ff; }
  .code-block code .token.number { color: #79c0ff; }
  .code-block code .token.operator { color: #ffab70; }
  .code-block code .token.punctuation { color: #c9d1d9; }
  .code-block code .token.builtin { color: #ffa657; }

  .info-note {
    background: rgba(30, 41, 59, 0.4);
    border-left: 4px solid #38bdf8;
    padding: 1.1rem 1.25rem;
    border-radius: 0 8px 8px 0;
    margin-top: 2rem;
  }

  .info-note p {
    margin: 0;
    font-size: 0.9rem;
    color: #94a3b8;
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