<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  const appVersion = import.meta.env.VITE_APP_VERSION || 'v1.0.0 Stable';
</script>



<div class="landing-container">
  <section class="hero">
    <div class="brand-badge">{appVersion}</div>
    <div class="logo-wrapper">
    <svg viewBox="0 0 24 24" width="80" height="80" fill="none" stroke="#4f46e5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 2L3 9l2 11 7 2 7-2 2-11-9-7z"/>
      <path d="M12 22V12"/>
      <path d="M12 12L5 9.5"/>
      <path d="M12 12l7-2.5"/>
      <path d="M12 6l-4 3.5 4 2.5 4-2.5L12 6z"/>
      <path d="M6.5 14.5L12 12l5.5 2.5"/>
    </svg>
  </div>
    <h1>Gwynbleidd</h1>
    <p class="tagline">Self-hosted, opensource backend for Godot 4.</p>
    <p class="sub-tagline">Inspired by SilentWolf</p>
    

    <div class="cta-group">
      <button class="btn-primary" on:click={() => dispatch('getStarted')}>
        Get Started
      </button>
      <button class="btn-outline" on:click={() => dispatch('register')}>
        Sign In
      </button>
    </div>
  </section>

  <section class="features-section">
    <h2>Everything your game needs, right out of the box</h2>
    <p class="section-subtitle">No multi-platform configuration hell. Pure GDScript API tailored to Godot's lifecycle.</p>
    
    <div class="features">
      <div class="feature-card">
        <div class="feature-icon">🔌</div>
        <h3>Godot Autoload</h3>
        <p>Drop-in GDScript addon. Intercept system signals, connect your whole database structure and initialize everything with just two lines of code.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🛡️</div>
        <h3>Tamper Protection</h3>
        <p>Built-in client-side SHA256 payload signing. Prevent score manipulation, spoofed network tokens, and leaderboards corruption seamlessly.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🏠</div>
        <h3>Self-Hosted Control</h3>
        <p>Your VPS, your database, your rules. Zero pricing tiers, no vendor lock-in, and absolutely no surprise usage billing spikes or limits.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🏅</div>
        <h3>Global Leaderboards</h3>
        <p>Instantly spawn multiple tables, secure asynchronous score submissions, and fetch clean player rows effortlessly inside your nodes.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">☁️</div>
        <h3>Secure Cloud Saves</h3>
        <p>Store, load and update full custom dictionary game-state snapshots directly linked with authenticated player sessions.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">👥</div>
        <h3>Player Auth</h3>
        <p>Async registration and login pipelines that handle local storage session tracking and emit cleaner signals upon completion.</p>
      </div>
    </div>
  </section>
</div>

<style>
  .landing-container {
    width: 100%;
    max-width: 1440px; 
    margin: 0 auto;
    padding: 8rem 2rem; 
    display: flex;
    flex-direction: column;
    gap: 5rem; 
    box-sizing: border-box;
  }

  .features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    width: 100%;
  }

  .hero {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .brand-badge {
    background: #1e293b;
    border: 1px solid #334155;
    color: #818cf8;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 2rem;
    letter-spacing: 0.5px;
  }

  .hero h1 {
    font-size: 4rem;
    font-weight: 800;
    color: #f8fafc;
    margin: 0 0 1.5rem 0;
    letter-spacing: -1.5px;
    line-height: 1.1;
  }

  .tagline {
    font-size: 1.25rem;
    color: #cbd5e1;
    margin: 0 0 0.75rem 0;
    font-weight: 500;
    line-height: 1.4;
  }

  .sub-tagline {
    font-size: 1rem;
    color: #64748b;
    margin: 0 0 3rem 0;
    line-height: 1.4;
  }

  .cta-group {
    display: flex;
    gap: 1rem;
  }

  .btn-primary {
    background: #4f46e5;
    border: none;
    color: #ffffff;
    padding: 0.85rem 2rem;
    border-radius: 6px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .btn-primary:hover {
    background: #4338ca;
  }

  .btn-outline {
    background: transparent;
    border: 1px solid #475569;
    color: #cbd5e1;
    padding: 0.85rem 2rem;
    border-radius: 6px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .btn-outline:hover {
    background-color: #1e293b;
    color: #f8fafc;
    border-color: #64748b;
  }

  .feature-card {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 2.5rem 2rem;
    text-align: left;
    transition: transform 0.2s ease, border-color 0.2s ease;
  }

  .feature-card:hover {
    transform: translateY(-2px);
    border-color: #475569;
  }

  .feature-icon {
    font-size: 2rem;
    margin-bottom: 1.25rem;
  }

  .feature-card h3 {
    color: #f8fafc;
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0 0 0.75rem 0;
  }

  .feature-card p {
    color: #94a3b8;
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
  }

  .code-preview {
    background: #090d16;
    border: 1px solid #334155;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    max-width: 1000px;
    width: 100%;
    margin: 0 auto;
    box-sizing: border-box;
  }

  .code-header {
    background: #1e293b;
    padding: 0.85rem 1.25rem;
    border-bottom: 1px solid #334155;
    display: flex;
    align-items: center;
    position: relative;
  }

  .code-dots {
    display: flex;
    gap: 0.45rem;
  }

  .dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
  }

  .dot.red { background: #ef4444; }
  .dot.yellow { background: #f59e0b; }
  .dot.green { background: #10b981; }

  .code-title {
    color: #64748b;
    font-size: 0.8rem;
    font-family: monospace;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
  }

  pre {
    margin: 0;
    padding: 1.75rem;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-all;
  }

  code {
    font-family: 'Fira Code', 'Courier New', monospace;
    font-size: 0.925rem;
    line-height: 1.6;
    color: #94a3b8;
  }

  .keyword { color: #ff7b72; font-weight: 600; }
  .function { color: #d2a6ff; }
  .class { color: #79c0ff; }
  .string { color: #a5d6ff; }
</style>