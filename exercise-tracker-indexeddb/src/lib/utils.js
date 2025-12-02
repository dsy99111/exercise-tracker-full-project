export function calculateParams(minutes, cfg={minutes_per_day:20}) {
  const duration = Number(minutes);
  return {
    p1: duration, // duration minutes
    p2: Math.round(duration * 5), // calories approx
    p3: Math.round((duration / cfg.minutes_per_day) * 100), // completion %
    p4: Math.round(Math.min(100, (duration / cfg.minutes_per_day) * 100 + Math.random()*10)), // consistency (mock)
    p5: Math.round(Math.min(100, (duration / cfg.minutes_per_day) * 100 + Math.random()*5)) // performance (mock)
  };
}
