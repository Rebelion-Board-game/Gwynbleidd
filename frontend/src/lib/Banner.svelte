<script>
  export let type = 'error'; // 'error' lub 'success'
  export let message = '';
</script>

{#if message}
  <div class="banner {type}">
    {message}
  </div>
{/if}

<style>
  .banner { padding: 0.75rem 1rem; border-radius: 6px; font-size: 0.85rem; }
  .error { background: rgba(248, 81, 73, 0.1); color: #ff7b72; }
  .success { background: rgba(56, 139, 253, 0.1); color: #58a6ff; }
</style>
