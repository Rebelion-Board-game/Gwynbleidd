<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  const appVersion = import.meta.env.VITE_APP_VERSION || 'v1.1.1 Stable';
</script>

<div class="landing-container">
  <section class="hero">
    <div class="brand-badge">{appVersion}</div>
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

  <section class="features">
    <div class="feature-card">
      <div class="feature-icon">🔌</div>
      <h3>Godot Plugin</h3>
      <p>Drop-in GDScript addon. Connect your entire backend with just two lines of code.</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon">⚡</div>
      <h3>Easy to Use</h3>
      <p>Simple player authentication and management. Set up your user database and leaderboards in minutes.</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon">🏠</div>
      <h3>Self-Hosted</h3>
      <p>Your VPS, your database, your rules. Zero pricing tiers or sudden usage billing limits.</p>
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
    gap: 8rem; 
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
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 2.5rem 2rem;
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