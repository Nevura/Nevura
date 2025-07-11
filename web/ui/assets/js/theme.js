(() => {
  const htmlEl = document.documentElement;
  const toggleBtn = document.getElementById('theme-toggle');
  const paletteSelector = document.getElementById('palette-select');

  // Chargement du mode initial (localStorage > system preference)
  function getPreferredTheme() {
    const stored = localStorage.getItem('theme');
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    if (theme === 'dark') {
      htmlEl.classList.add('dark');
    } else {
      htmlEl.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }

  // Chargement palette
  function applyPalette(palette) {
    htmlEl.classList.remove('palette-green', 'palette-red', 'palette-orange', 'palette-gray');
    if (palette && palette !== 'default') {
      htmlEl.classList.add('palette-' + palette);
    }
    localStorage.setItem('palette', palette);
  }

  // Init
  applyTheme(getPreferredTheme());
  const savedPalette = localStorage.getItem('palette') || 'default';
  applyPalette(savedPalette);

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      const current = htmlEl.classList.contains('dark') ? 'dark' : 'light';
      applyTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  if (paletteSelector) {
    paletteSelector.addEventListener('change', e => {
      applyPalette(e.target.value);
    });
  }
})();
