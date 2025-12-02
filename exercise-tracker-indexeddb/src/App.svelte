<script>
  import Login from './components/Login.svelte';
  import Dashboard from './components/Dashboard.svelte';
  import Admin from './components/Admin.svelte';
  import { onMount } from 'svelte';

  let user = null;
  onMount(()=>{
    const u = localStorage.getItem('user');
    if (u) user = JSON.parse(u);
  });

  function handleLogin(e) {
    user = e.detail;
    localStorage.setItem('user', JSON.stringify(user));
  }
  function logout() {
    user = null;
    localStorage.removeItem('user');
  }
</script>

<main style="padding:14px;max-width:720px;margin:0 auto;">
  {#if !user}
    <Login on:login={handleLogin} />
  {:else}
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
      <div><strong>Hi, {user.username}</strong> <span style="color:#666">({user.role})</span></div>
      <div><button on:click={logout} style="padding:6px 10px;border-radius:6px">Logout</button></div>
    </div>
    {#if user.role === 'admin'}
      <Admin {user} />
    {:else}
      <Dashboard {user} />
    {/if}
  {/if}
</main>
