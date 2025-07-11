import React, { useEffect, useState } from "react";
import { useSettingsStore, Theme } from "../store/settingsStore";
import { api } from "../lib/api";

export default function ThemeManager() {
  const themes = useSettingsStore((state) => state.themes);
  const selectedThemeId = useSettingsStore((state) => state.selectedThemeId);
  const addTheme = useSettingsStore((state) => state.addTheme);
  const selectTheme = useSettingsStore((state) => state.selectTheme);
  const removeTheme = useSettingsStore((state) => state.removeTheme);

  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [storeThemes, setStoreThemes] = useState<Theme[]>([]);
  const [warning, setWarning] = useState<string | null>(null);

  useEffect(() => {
    // Charger thèmes depuis le store officiel via API
    api.get<Theme[]>("/themes/store").then(res => setStoreThemes(res.data));
  }, []);

  function handleFileUpload() {
    if (!uploadFile) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      // Validation simple JSON (thème)
      try {
        const themeJson = JSON.parse(content);
        if (!themeJson.name || !themeJson.colors) {
          setWarning("Le fichier uploadé n'est pas un thème valide.");
          return;
        }
        const newTheme: Theme = {
          id: `local-${Date.now()}`,
          name: themeJson.name,
          approved: false,
          source: "local",
          filePath: "", // chemin local (non persistant ici)
        };
        addTheme(newTheme);
        setWarning(null);
      } catch {
        setWarning("Erreur lors de la lecture du fichier.");
      }
    };
    reader.readAsText(uploadFile);
  }

  function handleAddStoreTheme(theme: Theme) {
    if (!theme.approved) {
      if (!confirm(`Ce thème n'est pas approuvé officiellement. Voulez-vous vraiment l'installer ?`)) {
        return;
      }
    }
    addTheme(theme);
    setWarning(null);
  }

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">Gestion des Thèmes</h1>

      <section>
        <h2 className="font-semibold mb-2">Thèmes installés</h2>
        <div className="grid grid-cols-3 gap-3">
          {themes.map((t) => (
            <div
              key={t.id}
              className={`theme-item ${selectedThemeId === t.id ? "selected" : ""}`}
              onClick={() => selectTheme(t.id)}
            >
              {t.name}
              {!t.approved && <div className="text-yellow-500 text-xs">Non approuvé</div>}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  if (confirm("Supprimer ce thème ?")) removeTheme(t.id);
                }}
                className="text-red-600 text-xs mt-1"
              >
                Supprimer
              </button>
            </div>
          ))}
          {themes.length === 0 && <p>Aucun thème installé.</p>}
        </div>
      </section>

      <section>
        <h2 className="font-semibold mb-2">Ajouter un thème depuis votre PC</h2>
        <input
          type="file"
          accept=".json"
          onChange={(e) => setUploadFile(e.target.files?.[0] ?? null)}
          className="mb-2"
        />
        <button onClick={handleFileUpload} className="btn-primary" disabled={!uploadFile}>
          Ajouter le thème
        </button>
        {warning && <p className="warning-text">{warning}</p>}
      </section>

      <section>
        <h2 className="font-semibold mb-2">Ajouter un thème depuis le store</h2>
        <div className="grid grid-cols-3 gap-3">
          {storeThemes.map((t) => (
            <div key={t.id} className="theme-item" onClick={() => handleAddStoreTheme(t)}>
              {t.name} {t.approved ? "" : <span className="text-yellow-600">(Non approuvé)</span>}
            </div>
          ))}
          {storeThemes.length === 0 && <p>Aucun thème dans le store.</p>}
        </div>
      </section>
    </div>
  );
}
