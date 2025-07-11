class Translator {
  constructor(lang = "en") {
    this.lang = lang;
    this.translations = {};
  }

  async load() {
    const res = await fetch(`/api/translation/?lang=${this.lang}`);
    if (res.ok) {
      this.translations = await res.json();
    }
  }

  t(key) {
    return this.translations[key] || key;
  }
}