<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();
</script>

<div class="contact-container">
  <div class="contact-center">
    <h2>Get in touch</h2>
    <p class="subtitle">Have questions about Gwynbleidd? Choose the best way to reach us.</p>
    
    <div class="channels-list">
      <a href="https://discord.gg/AUYVJRuWX" target="_blank" rel="noopener noreferrer" class="channel-card discord">
        <div class="channel-icon">
          <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
            <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.126c.126-.093.252-.19.372-.287a.077.077 0 0 1 .085-.006c3.328 1.515 6.94 1.515 10.182 0a.077.077 0 0 1 .085.006c.12.098.246.194.372.287a.077.077 0 0 1-.007.126 12.98 12.98 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.094-.838-9.42-3.543-13.44a.06.06 0 0 0-.032-.026zM8.04 15.297c-1.125 0-2.044-1.032-2.044-2.301 0-1.269.919-2.301 2.044-2.301 1.13 0 2.048 1.032 2.044 2.301 0 1.269-.914 2.301-2.044 2.301zm7.92 0c-1.125 0-2.044-1.032-2.044-2.301 0-1.269.919-2.301 2.044-2.301 1.13 0 2.048 1.032 2.044 2.301 0 1.269-.914 2.301-2.044 2.301z"/>
          </svg>
        </div>
        <div class="channel-details">
          <strong>Join Discord Server</strong>
          <span>Community support, live chat & dev log</span>
        </div>
      </a>

      <a href="https://github.com/Rebelion-Board-game/Gwynbleidd/issues" target="_blank" rel="noopener noreferrer" class="channel-card github">
        <div class="channel-icon">
          <span class="icon-txt">🐙</span>
        </div>
        <div class="channel-details">
          <strong>GitHub Issues</strong>
          <span>Report bugs or request new features</span>
        </div>
      </a>
    </div>
    
    <div class="info-footer">
      <p>Looking for technical references? Check out the <button class="link-btn" on:click={() => dispatch('nav', 'docs')}>Documentation</button>.</p>
    </div>
  </div>
</div>

<style>
  .contact-container {
    max-width: 600px;
    width: 95%;
    margin: 6rem auto;
    color: #cbd5e1;
  }

  .contact-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  h2 {
    color: #f8fafc;
    font-size: 2.5rem;
    margin: 0 0 0.75rem 0;
    font-weight: 800;
  }

  .subtitle {
    color: #94a3b8;
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 3rem;
  }

  .channels-list {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    width: 100%;
  }

  .channel-card {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    padding: 1.5rem;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    text-decoration: none;
    color: #cbd5e1;
    text-align: left;
    transition: transform 0.2s, border-color 0.2s, background 0.2s;
  }

  .channel-card:hover {
    transform: translateY(-2px);
    background: #1f2631;
  }

  .channel-card.discord:hover {
    border-color: #5865f2;
  }

  .channel-card.github:hover {
    border-color: #f0f6fc;
  }

  .channel-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 52px;
    height: 52px;
    border-radius: 10px;
    background: #21262d;
    color: #f0f6fc;
    flex-shrink: 0;
  }

  .discord .channel-icon {
    color: #5865f2;
  }

  .icon-txt {
    font-size: 1.6rem;
  }

  .channel-details {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }

  .channel-details strong {
    color: #f8fafc;
    font-size: 1.1rem;
  }

  .channel-details span {
    color: #8b949e;
    font-size: 0.95rem;
  }

  .info-footer {
    margin-top: 4rem;
    font-size: 1rem;
    color: #94a3b8;
  }

  .link-btn {
    background: none;
    border: none;
    color: #58a6ff;
    padding: 0;
    font-size: inherit;
    font-family: inherit;
    cursor: pointer;
    text-decoration: underline;
  }

  .link-btn:hover {
    color: #79c0ff;
  }
</style>