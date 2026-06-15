<script>
  import { createEventDispatcher } from 'svelte';
  import Login from './Login.svelte';
  import Register from './Register.svelte';

  export let API_BASE;
  export let mode = 'login';

  const dispatch = createEventDispatcher();
  let currentForm = mode;
  let globalSuccessMessage = '';

  function onRegisterSuccess() {
    globalSuccessMessage = 'Account created successfully! You can now log in below.';
    currentForm = 'login';
  }
</script>

<div class="auth-page">
  <div class="auth-wrapper">
    <div class="auth-container">
      {#if currentForm === 'login'}
        <Login 
          {API_BASE} 
          successMessage={globalSuccessMessage} 
          on:loginSuccess={(e) => dispatch('loginSuccess', e.detail)} 
          on:switch={() => currentForm = 'register'} 
          on:back={() => dispatch('back')}
        />
      {:else}
        <Register 
          {API_BASE} 
          on:registerSuccess={onRegisterSuccess} 
          on:switch={() => currentForm = 'login'} 
          on:back={() => dispatch('back')}
        />
      {/if}
    </div>
  </div>
</div>

<style>
  .auth-page {
    min-height: 80vh;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem 0;
  }

  .auth-wrapper {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .auth-container {
    width: 100%;
    max-width: 440px; 
  }

  :global(.banner-space) {
    margin-top: 1.5rem;
    width: 100%;
  }
</style>