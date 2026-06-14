<footer class="site-footer">
  <div class="container footer-content">
    <div class="footer-left">
      <!-- Use semantic tag for logo/icon area -->
      <div class="brand-wrapper">
        <span class="icon">🐺</span>
        <strong class="footer-brand">Gwynbleidd</strong>
      </div>
      <p class="footer-copy">Open source backend for Godot by slime3000fly</p>
    </div>
    <nav class="footer-right" aria-label="Footer navigation">
      <a href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a>
      <a href="#" on:click|preventDefault>Documentation</a>
    </nav>
  </div>
</footer>

<style>
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