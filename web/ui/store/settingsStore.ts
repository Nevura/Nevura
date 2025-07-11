import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { produce } from 'immer';

export interface Theme {
  id: string;
  name: string;
  approved: boolean;
  source: "local" | "store";
  filePath?: string;
}

interface SettingsState {
  themes: Theme[];
  selectedThemeId: string | null;
  addTheme: (theme: Theme) => void;
  selectTheme: (id: string) => void;
  removeTheme: (id: string) => void;
}

interface SettingsStore {
  theme: string;
  autoDarkMode: boolean;
  themesAvailable: Theme[];
  language: string;
  smtpEnabled: boolean;
  notifyDesktop: boolean;
  notifyMail: boolean;
  setTheme: (theme: string) => void;
  toggleDarkMode: (v: boolean) => void;
  setThemesAvailable: (themes: Theme[]) => void;
  setLanguage: (lang: string) => void;
  setSmtpEnabled: (enabled: boolean) => void;
  setNotifyDesktop: (enabled: boolean) => void;
  setNotifyMail: (enabled: boolean) => void;
}

export const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      theme: 'default',
      autoDarkMode: true,
      themesAvailable: [],
      language: 'fr',
      smtpEnabled: false,
      notifyDesktop: true,
      notifyMail: false,
      setTheme: (theme) =>
        set(
          produce((s: SettingsStore) => {
            s.theme = theme;
          })
        ),
      toggleDarkMode: (v) =>
        set(
          produce((s: SettingsStore) => {
            s.autoDarkMode = v;
          })
        ),
      setThemesAvailable: (themes) =>
        set(
          produce((s: SettingsStore) => {
            s.themesAvailable = themes;
          })
        ),
      setLanguage: (lang) =>
        set(
          produce((s: SettingsStore) => {
            s.language = lang;
          })
        ),
      setSmtpEnabled: (enabled) =>
        set(
          produce((s: SettingsStore) => {
            s.smtpEnabled = enabled;
          })
        ),
      setNotifyDesktop: (enabled) =>
        set(
          produce((s: SettingsStore) => {
            s.notifyDesktop = enabled;
          })
        ),
      setNotifyMail: (enabled) =>
        set(
          produce((s: SettingsStore) => {
            s.notifyMail = enabled;
          })
        )
    }),
    {
      name: 'settings-storage'
    }
    themes: [],
  selectedThemeId: null,
  addTheme: (theme) => set((state) => {
    if (state.themes.find(t => t.id === theme.id)) return state;
    return { themes: [...state.themes, theme] };
  }),
  selectTheme: (id) => set({ selectedThemeId: id }),
  removeTheme: (id) => set((state) => ({
    themes: state.themes.filter(t => t.id !== id),
    selectedThemeId: state.selectedThemeId === id ? null : state.selectedThemeId,
  })),