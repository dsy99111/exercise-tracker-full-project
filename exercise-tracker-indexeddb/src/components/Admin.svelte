<script>
  import { onMount } from "svelte";
  import FiveChart from "./FiveChart.svelte";

  // API helpers
  import {
    getUsers,
    addUser,
    getConfig,
    updateConfig,
    getRoutineHistory
  } from "../lib/api.js";

  let users = [];
  let selected = null;
  let history = [];     // ⭐ RoutineTracker history
let originalHistory = [];

  let cfg = {};

  // Config fields
  let newTotal = 0;
  let newMinutes = 0;

  // New user form
  let newUsername = "";
  let newPassword = "";
  let newRole = "user";

  // Date Filters
  let filterStart = "";
  let filterEnd = "";

  onMount(async () => {
    await loadUsers();
    await loadConfig();
  });

  async function loadUsers() {
    users = await getUsers();
  }

  async function loadConfig() {
    cfg = await getConfig();

    newTotal = cfg.total_challenges?.value ?? 10;
    newMinutes = cfg.minutes_per_day?.value ?? 20;
  }

  async function load(user) {
  selected = user;

  originalHistory = await getRoutineHistory(user.id);
  history = applyFilters(originalHistory);
}
function toYMD(dt) {
  let safe = dt.replace(" ", "T");   // Fix invalid datetime
  let d = new Date(safe);
  if (isNaN(d.getTime())) return null;
  return d.toISOString().slice(0, 10);
}


 function applyFilters(list) {
  return list.filter(item => {
    const d = new Date(item.created_at).toISOString().slice(0, 10);

    if (filterStart && d < filterStart) return false;
    if (filterEnd && d > filterEnd) return false;

    return true;
  });
}



  function applyDateFilter() {
  if (!selected) return;

  if (!filterStart && !filterEnd) {
    history = originalHistory;
    return;
  }

  history = applyFilters(originalHistory);
}
function formatDate(dt) {
  if (!dt) return "No Date";

  // Fix spaces → replace with T
  let safe = dt.replace(" ", "T");

  let d = new Date(safe);

  if (isNaN(d.getTime())) {
    return "Invalid Date";
  }

  return d.toLocaleString();
}



  async function saveConfig() {
    await updateConfig("total_challenges", Number(newTotal));
    await updateConfig("minutes_per_day", Number(newMinutes));

    alert("Config saved!");
    await loadConfig();
  }

  async function addNewUser() {
    if (!newUsername || !newPassword)
      return alert("Enter username + password");

    await addUser({
      username: newUsername,
      password: newPassword,
      role: newRole
    });

    alert(`User "${newUsername}" created!`);
    newUsername = "";
    newPassword = "";
    newRole = "user";

    await loadUsers();
  }

  // Analytics
  $: totalEmotional = history.reduce((a, p) => a + p.emotional_minutes, 0);
  $: totalMental = history.reduce((a, p) => a + p.mental_minutes, 0);
  $: totalPhysical = history.reduce((a, p) => a + p.physical_minutes, 0);
  $: totalMinutes = totalEmotional + totalMental + totalPhysical;

  $: morningCount = history.filter(h => h.section === "morning").length;
  $: microCount = history.filter(h => h.section === "micro").length;
  $: eveningCount = history.filter(h => h.section === "evening").length;
</script>

<!-- PAGE START -->
<div style="max-width:1000px;margin:20px auto;font-family:sans-serif;">

  <h2 style="color:#0ea5a4;margin-bottom:20px;">Admin Dashboard</h2>

  <!-- CONFIG -->
  <div style="padding:16px;margin-bottom:20px;border-radius:12px;background:#f9f9f9;">
    <h3>⚙️ App Configuration</h3>
    <div style="display:flex;gap:12px;flex-wrap:wrap">
      <div>
        <label>Total Challenges</label>
        <input type="number" bind:value={newTotal} min="1" />
      </div>
      <div>
        <label>Minutes per Day</label>
        <input type="number" bind:value={newMinutes} min="1" />
      </div>
      <button on:click={saveConfig}>Save</button>
    </div>
  </div>

  <!-- ADD USER -->
  <div style="padding:16px;margin-bottom:20px;border-radius:12px;background:#f0f8ff;">
    <h3>➕ Add New User</h3>
    <div style="display:flex;gap:12px;flex-wrap:wrap">
      <input placeholder="Username" bind:value={newUsername} />
      <input placeholder="Password" type="password" bind:value={newPassword} />
      <select bind:value={newRole}>
        <option value="user">User</option>
        <option value="admin">Admin</option>
      </select>
      <button on:click={addNewUser}>Add User</button>
    </div>
  </div>

  <!-- USERS -->
  <div style="padding:16px;margin-bottom:20px;border-radius:12px;background:#fff;">
    <h3>👥 All Users</h3>
    <div style="display:flex;flex-wrap:wrap;gap:8px;">
      {#each users as u}
        <button on:click={() => load(u)}>{u.username} ({u.role})</button>
      {/each}
    </div>
  </div>

  <!-- ROUTINE HISTORY FOR USER -->
  {#if selected}
    <div style="padding:16px;border-radius:12px;background:#fdfdfd;box-shadow:0 3px 12px rgba(0,0,0,0.08);">

      <h3>📊 Routine History — {selected.username}</h3>

      <!-- DATE FILTERS -->
      <div style="display:flex;gap:12px;margin-bottom:12px;">
        <input type="date" bind:value={filterStart} />
        <input type="date" bind:value={filterEnd} />
        <button on:click={applyDateFilter}>Filter</button>
      </div>

      <!-- ANALYTICS -->
      <div style="margin:12px 0;padding:12px;border:1px solid #eee;border-radius:8px;">
        <h4>📈 Analytics Summary</h4>
        <p><strong>Total Minutes:</strong> {totalMinutes}</p>
        <p>Emotional: {totalEmotional} | Mental: {totalMental} | Physical: {totalPhysical}</p>

        <p><strong>Routine Count:</strong></p>
        <p>Morning: {morningCount} | Micro: {microCount} | Evening: {eveningCount}</p>
      </div>

      <!-- ALL ROUTINES -->
      {#each history as h}
        <div style="padding:12px;margin-bottom:12px;border-radius:8px;border:1px solid #eee;">
          <div style="font-weight:600;">
            {new Date(h.created_at).toLocaleString()} — {h.section}
          </div>

          <FiveChart params={{
            p1: h.emotional_minutes,
            p2: h.mental_minutes,
            p3: h.physical_minutes,
            p4: h.emotional + h.mental + h.physical ? 100 : 0,
            p5: (h.emotional_minutes + h.mental_minutes + h.physical_minutes) / 3
          }} />
        </div>
      {/each}
    </div>
  {/if}

</div>
