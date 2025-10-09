import { injectSpeedInsights } from '@vercel/speed-insights';

injectSpeedInsights();

document.addEventListener('DOMContentLoaded', function() {
  if (window.initializeSakanaWidget) {
    window.initializeSakanaWidget();
  }
});