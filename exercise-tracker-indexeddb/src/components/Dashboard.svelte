<script>
  import { onMount } from "svelte";
  import { saveRoutineAPI } from "../lib/api.js";
import { getRoutineHistory } from "../lib/api.js";
import FiveChart from "../components/FiveChart.svelte";

  export let user;

  let quote = "Loading quote...";
  let openPanel = null;

  /** AUDIO (OPTIONAL) */
  let audio = null;

  /** TIMER CORE */
  let countdown = 0;        // total seconds
  let remainingTime = 0;    // seconds left
  let timerInterval = null;
  let countdownStart = 1;   // reactive baseline for circle
  let history = [];
  let filterStart = "";
  let filterEnd = "";
  let originalHistory = [];

  /** Ask notification permission */
  onMount(() => {
    if (Notification.permission !== "granted") {
      Notification.requestPermission();
    }
  });

  /** Optional audio — no error if missing */
  onMount(() => {
    try {
      audio = new Audio("http://127.0.0.1:8000/media/audio/108gm.mp3");
    } catch (e) {
      audio = null;  // safe fallback
    }
  });

  /** Fetch Quote */
  onMount(async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/daily-quote/");
      const data = await res.json();
      quote = data.quote;
    } catch (e) {
      quote = "Unable to load quote 😞";
    }
  });
onMount(async () => {
  originalHistory = await getRoutineHistory(user.id);
  history = originalHistory;
});


  /** HABIT STORE */
  let habits = {
    morning: initHabit(),
    micro: initHabit(),
    evening: initHabit()
  };

  function initHabit() {
    return {
      emotional: false,
      mental: false,
      physical: false,
      emotionalMinutes: 0,
      mentalMinutes: 0,
      physicalMinutes: 0,
      start: null,
      end: null,
      progressResult: null
    };
  }

  function togglePanel(section) {
    openPanel = openPanel === section ? null : section;
  }

  /** START ROUTINE */
  function startRoutine(section) {
    const h = habits[section];
    h.start = new Date();
    h.end = null;
    h.progressResult = null;

    /** Calculate selected minutes — fallback to 30 mins each if not selected */
    const em = h.emotional ? h.emotionalMinutes : 0;
    const me = h.mental ? h.mentalMinutes : 0;
    const ph = h.physical ? h.physicalMinutes : 0;

    const totalMinutes = em + me + ph;

    countdown = totalMinutes * 60;
    remainingTime = countdown;
    countdownStart = countdown || 1;

    if (timerInterval) clearInterval(timerInterval);

    timerInterval = setInterval(() => {
      remainingTime--;

      if (remainingTime <= 0) {
        remainingTime = 0;
        endRoutine(section, true); // AUTO STOP
      }
    }, 1000);

    if (audio) {
      audio.currentTime = 0;
      audio.play();
    }
  }

  /** END ROUTINE */
 async function endRoutine(section, autoStop = false) {
  const h = habits[section];
  h.end = new Date();

  if (timerInterval) clearInterval(timerInterval);
  if (audio) audio.pause();

  const selected =
    (h.emotional ? h.emotionalMinutes : 0) +
    (h.mental ? h.mentalMinutes : 0) +
    (h.physical ? h.physicalMinutes : 0);

  h.progressResult = Math.round((selected / 90) * 100);

  /** Notify desktop */
  if (autoStop) {
    new Notification("⏳ Time’s Up!", {
      body: `${section} routine completed.`,
    });
  }

  /** --- SAVE TO BACKEND --- */
  await saveRoutineAPI({
    section,
    emotional: h.emotional,
    mental: h.mental,
    physical: h.physical,
    emotionalMinutes: h.emotionalMinutes,
    mentalMinutes: h.mentalMinutes,
    physicalMinutes: h.physicalMinutes,
    start: h.start.toISOString(),
    end: h.end.toISOString(),
  });
}


  function formatCountdown(sec) {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}:${s.toString().padStart(2, "0")}`;
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
  if (!filterStart && !filterEnd) {
    history = originalHistory;
    return;
  }
  history = applyFilters(originalHistory);
}

</script>


<!-- PAGE -->
<div class="page">

  <div class="quote-box">
    <h2>{quote}</h2>
  </div>

  <div class="section" on:click={() => togglePanel("morning")}><h3>MORNING</h3></div>
  <div class="section" on:click={() => togglePanel("micro")}><h3>MICRO - ACTION</h3></div>
  <div class="section" on:click={() => togglePanel("evening")}><h3>EVENING</h3></div>


  {#if openPanel}
    {#key openPanel}
      <div class="panel">

        <h2 style="text-transform: capitalize;">{openPanel} Routine</h2>

        <!-- START BUTTON -->
        {#if !habits[openPanel].start}
          <button class="btn" on:click={() => startRoutine(openPanel)}>▶ Start</button>
        {/if}

        <!-- LIVE COUNTDOWN -->
        {#if habits[openPanel].start && !habits[openPanel].end}
          <p><strong>Remaining:</strong> {formatCountdown(remainingTime)}</p>
        {/if}

        <!-- START TIME -->
        {#if habits[openPanel].start}
          <p><strong>Start:</strong> {habits[openPanel].start.toLocaleTimeString()}</p>
        {/if}

        <!-- EMOTIONAL -->
        <label>
          <input type="checkbox" bind:checked={habits[openPanel].emotional}>
          Emotional – 108 HPN
        </label>
        {#if habits[openPanel].emotional}
          <input type="range" min="0" max="30" bind:value={habits[openPanel].emotionalMinutes}>
          <p>Minutes: {habits[openPanel].emotionalMinutes}</p>
        {/if}

        <!-- MENTAL -->
        <label>
          <input type="checkbox" bind:checked={habits[openPanel].mental}>
          Mental – Reading / Writing
        </label>
        {#if habits[openPanel].mental}
          <input type="range" min="0" max="30" bind:value={habits[openPanel].mentalMinutes}>
          <p>Minutes: {habits[openPanel].mentalMinutes}</p>
        {/if}

        <!-- PHYSICAL -->
        <label>
          <input type="checkbox" bind:checked={habits[openPanel].physical}>
          Physical – Walk / Activity
        </label>
        {#if habits[openPanel].physical}
          <input type="range" min="0" max="30" bind:value={habits[openPanel].physicalMinutes}>
          <p>Minutes: {habits[openPanel].physicalMinutes}</p>
        {/if}

        <!-- PROGRESS ONLY AFTER END -->
        {#if habits[openPanel].progressResult !== null}
          <p><strong>Progress:</strong> {habits[openPanel].progressResult}%</p>
        {/if}

        <!-- END BUTTON -->
        {#if habits[openPanel].start && !habits[openPanel].end}
          <button class="btn end" on:click={() => endRoutine(openPanel)}>⏹ End</button>
        {/if}

        {#if habits[openPanel].end}
          <p><strong>End:</strong> {habits[openPanel].end.toLocaleTimeString()}</p>
        {/if}

      </div>
    {/key}
  {/if}
  <h2 style="margin-top:40px;">Your Progress History</h2>

<div style="display:flex;gap:12px;margin-bottom:12px;">
  <input type="date" bind:value={filterStart} />
  <input type="date" bind:value={filterEnd} />
  <button on:click={applyDateFilter}>Filter</button>
</div>

{#each history as h}
  <div style="padding:12px; ...">
    <div style="font-weight:600;">
      {new Date(h.created_at).toLocaleString()} — {h.section.toUpperCase()}
    </div>

    <FiveChart params={{
      p1: h.emotional_minutes,
      p2: h.mental_minutes,
      p3: h.physical_minutes,
      p4: (h.emotional || h.mental || h.physical) ? 100 : 0,
      p5: (h.emotional_minutes + h.mental_minutes + h.physical_minutes) / 3
    }} />
  </div>
{/each}

</div>


<!-- CIRCULAR TIMER -->
{#if openPanel && habits[openPanel].start && !habits[openPanel].end}
<div class="circle-wrapper">
  <svg width="160" height="160">
    <circle cx="80" cy="80" r="70" stroke="#eee" stroke-width="10" fill="none" />
    <circle
      cx="80"
      cy="80"
      r="70"
      stroke="teal"
      stroke-width="10"
      fill="none"
      stroke-dasharray="440"
      stroke-dashoffset={440 - (remainingTime / countdownStart) * 440}
      style="transition: stroke-dashoffset 1s linear;"
    />
  </svg>

  <div class="circle-text">
    {formatCountdown(remainingTime)}
  </div>
</div>
{/if}


<style>
  .btn { padding: 10px 20px; background: teal; color: white; border: none; border-radius: 8px; margin-top: 15px; cursor: pointer; font-size: 16px; }
  .end { background: crimson; }
  .page { max-width: 800px; margin: 0 auto; padding: 25px; }
  .quote-box { background: #f4f4f4; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 30px; }
  .section { background: white; padding: 20px; margin-top: 15px; border-radius: 14px; box-shadow: 0 3px 10px rgba(0,0,0,0.1); cursor: pointer; text-align:center; }
  .panel { margin-top: 20px; background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
  label { display: block; font-size: 18px; margin-top: 18px; }
  input[type="range"] { width: 100%; margin-top: 10px; }
  input[type="checkbox"] { margin-right: 10px; transform: scale(1.3); }

  .circle-wrapper {
    position: relative;
    width: 160px;
    height: 160px;
    margin: 20px auto;
  }
  .circle-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 26px;
    font-weight: bold;
  }
</style>
