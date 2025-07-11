import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { produce } from 'immer';

interface SessionDevice {
  id: string;
  userAgent: string;
  ip: string;
  lastActive: string;
}

interface UserStore {
  token: string | null;
  username: string;
  email: string;
  language: string;
  isAdmin: boolean;
  sessions: SessionDevice[];
  setToken: (token: string) => void;
  logout: () => void;
  updateProfile: (email: string, username: string) => void;
  setLanguage: (lang: string) => void;
  setSessions: (sessions: SessionDevice[]) => void;
}

export const useUserStore = create<UserStore>()(
  persist(
    (set) => ({
      token: null,
      username: '',
      email: '',
      language: 'fr',
      isAdmin: false,
      sessions: [],
      setToken: (token) =>
        set(
          produce((state: UserStore) => {
            state.token = token;
          })
        ),
      logout: () =>
        set(
          produce((state: UserStore) => {
            state.token = null;
            state.username = '';
            state.email = '';
            state.isAdmin = false;
            state.sessions = [];
          })
        ),
      updateProfile: (email, username) =>
        set(
          produce((state: UserStore) => {
            state.email = email;
            state.username = username;
          })
        ),
      setLanguage: (lang) =>
        set(
          produce((state: UserStore) => {
            state.language = lang;
          })
        ),
      setSessions: (sessions) =>
        set(
          produce((state: UserStore) => {
            state.sessions = sessions;
          })
        )
    }),
    {
      name: 'user-storage'
    }
  )
);
