<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
</script>

<footer class="site-footer">
  <div class="container footer-content">
    <div class="footer-left">
      <div class="brand-wrapper">
        <span class="icon">🐺</span>
        <strong class="footer-brand">Gwynbleidd</strong>
      </div>
      <p class="footer-copy">Open source backend for Godot by slime3000fly</p>
    </div>
    <nav class="footer-right" aria-label="Footer navigation">
      <a href="https://github.com/Rebelion-Board-game/Gwynbleidd" target="_blank" rel="noopener noreferrer">GitHub</a>
      <a href="https://discord.gg/AUYVJRuWX" target="_blank" rel="noopener noreferrer" aria-label="Discord">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
          <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.126c.126-.093.252-.19.372-.287a.077.077 0 0 1 .085-.006c3.328 1.515 6.94 1.515 10.182 0a.077.077 0 0 1 .085.006c.12.098.246.194.372.287a.077.077 0 0 1-.007.126 12.98 12.98 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.094-.838-9.42-3.543-13.44a.06.06 0 0 0-.032-.026zM8.04 15.297c-1.125 0-2.044-1.032-2.044-2.301 0-1.269.919-2.301 2.044-2.301 1.13 0 2.048 1.032 2.044 2.301 0 1.269-.914 2.301-2.044 2.301zm7.92 0c-1.125 0-2.044-1.032-2.044-2.301 0-1.269.919-2.301 2.044-2.301 1.13 0 2.048 1.032 2.044 2.301 0 1.269-.914 2.301-2.044 2.301z"/>
        </svg>
      </a>
      <button class="nav-link-btn" on:click={() => dispatch('nav', 'docs')}>Documentation</button>
    </nav>
  </div>
</footer>

<style>
  .nav-link-btn {
    background: none;
    border: none;
    color: #58a6ff;
    cursor: pointer;
    font-size: 0.9rem;
    padding: 0;
  }
  .nav-link-btn:hover {
    color: #79c0ff;
    text-decoration: underline;
  }
  .site-footer {
    background: #161b22;
    border-top: 1px solid #30363d;
    padding: 2rem 0;
    margin-top: auto;
  }
  
  .container {
    max-width: 1400px;
    width: 95%;
    margin: 0 auto;
  }
  
  .footer-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1.5rem;
  }
  
  .footer-left {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    color: #8b949e;
    font-size: 0.9rem;
  }

  .brand-wrapper {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .footer-brand {
    font-weight: 700;
    color: #f0f6fc;
  }
  
  .footer-copy {
    margin: 0;
  }
  
  .footer-right {
    display: flex;
    gap: 1.5rem;
  }
  
  .footer-right a {
    color: #58a6ff;
    text-decoration: none;
    font-size: 0.9rem;
    transition: color 0.1s ease;
  }
  
  .footer-right a:hover {
    color: #79c0ff;
    text-decoration: underline;
  }

.footer-right a, .nav-link-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .footer-right a:hover {
    color: #79c0ff;
  }
  /* Responsive layout for small screens */
  @media (max-width: 640px) {
    .footer-content {
      flex-direction: column;
      align-items: flex-start;
    }
    
    .footer-left {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }
  }
</style>