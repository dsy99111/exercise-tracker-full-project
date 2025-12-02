<script>
  import { onMount, onDestroy } from "svelte";
  import Chart from "chart.js/auto";

  export let params = {};

  let canvasEl;
  let chart;

  // Normalize params so we never break Chart.js
  function normalize(p) {
    return [
      p?.p1 ?? 0,
      p?.p2 ?? 0,
      p?.p3 ?? 0,
      p?.p4 ?? 0,
      p?.p5 ?? 0,
    ];
  }

  function renderChart() {
    if (!canvasEl) return;

    // Destroy previous chart to avoid duplicates
    if (chart) chart.destroy();

    const values = normalize(params);

    chart = new Chart(canvasEl, {
      type: "radar",
      data: {
        labels: [
          "Duration",
          "Calories",
          "Completion",
          "Consistency",
          "Performance"
        ],
        datasets: [
          {
            label: "Score",
            data: values,
            fill: true,
            borderWidth: 2,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            beginAtZero: true,
            suggestedMin: 0,
            suggestedMax: 100,
          }
        },
        animation: {
          duration: 500
        }
      }
    });
  }

  onMount(() => {
    renderChart();
  });

  // Re-render when params change
  $: if (params) {
    renderChart();
  }

  onDestroy(() => {
    if (chart) chart.destroy();
  });
</script>

<div style="width:100%; height:260px;">
  <canvas bind:this={canvasEl}></canvas>
</div>
