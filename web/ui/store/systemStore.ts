import { create } from 'zustand';
import { produce } from 'immer';

interface Disk {
  id: string;
  name: string;
  size: number;
  usage: number;
  mountpoint: string;
  fsType: string;
}

interface SystemStore {
  hostname: string;
  timezone: string;
  osVersion: string;
  disks: Disk[];
  ramTotal: number;
  ramUsed: number;
  cpuLoad: number;
  alerts: string[];
  setHostname: (hostname: string) => void;
  setTimezone: (tz: string) => void;
  setDisks: (d: Disk[]) => void;
  setRAM: (used: number, total: number) => void;
  setCPULoad: (load: number) => void;
  setAlerts: (a: string[]) => void;
}

export const useSystemStore = create<SystemStore>((set) => ({
  hostname: '',
  timezone: '',
  osVersion: '',
  disks: [],
  ramTotal: 0,
  ramUsed: 0,
  cpuLoad: 0,
  alerts: [],
  setHostname: (hostname) =>
    set(
      produce((s: SystemStore) => {
        s.hostname = hostname;
      })
    ),
  setTimezone: (tz) =>
    set(
      produce((s: SystemStore) => {
        s.timezone = tz;
      })
    ),
  setDisks: (d) =>
    set(
      produce((s: SystemStore) => {
        s.disks = d;
      })
    ),
  setRAM: (used, total) =>
    set(
      produce((s: SystemStore) => {
        s.ramUsed = used;
        s.ramTotal = total;
      })
    ),
  setCPULoad: (load) =>
    set(
      produce((s: SystemStore) => {
        s.cpuLoad = load;
      })
    ),
  setAlerts: (a) =>
    set(
      produce((s: SystemStore) => {
        s.alerts = a;
      })
    )
}));
