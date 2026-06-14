<script>
  export let type = 'error'; 
  export let message = '';
</script>

{#if message}
  <div class="banner {type}" role="alert">
    <div class="indicator"></div>
    <span class="message">{message}</span>
  </div>
{/if}

<style>
  .banner {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.85rem 1rem;
    border-radius: 6px;
    font-size: 0.875rem;
    line-height: 1.25rem;
    margin: 1rem 0;
    border: 1px solid transparent;
  }

  .indicator {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .message {
    flex: 1;
    font-weight: 500;
  }

  /* Light mode styles */
  .error {
    background-color: #fef2f2;
    color: #991b1b;
    border-color: #fca5a5;
  }
  .error .indicator {
    background-color: #dc2626;
  }

  .success {
    background-color: #f0fdf4;
    color: #166534;
    border-color: #86efac;
  }
  .success .indicator {
    background-color: #16a34a;
  }

  /* Dark mode styles */
  @media (prefers-color-scheme: dark) {
    .error {
      background-color: rgba(248, 81, 73, 0.1);
      color: #ff7b72;
      border-color: rgba(248, 81, 73, 0.25);
    }
    .error .indicator {
      background-color: #f85149;
    }

    .success {
      background-color: rgba(56, 139, 253, 0.1);
      color: #58a6ff;
      border-color: rgba(56, 139, 253, 0.25);
    }
    .success .indicator {
      background-color: #58a6ff;
    }
  }
</style>