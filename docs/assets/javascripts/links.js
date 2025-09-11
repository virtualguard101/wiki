document$.subscribe(() => {
  // 让非当前网站的外部链接在新窗口打开
  const selectors = 'a[href^="http"]:not([href*="' + window.location.host + '"])';
  for (const link of document.querySelectorAll(selectors)) {
    link.setAttribute('target', '_blank');
    link.setAttribute('rel', 'noopener noreferrer');
  }
});
