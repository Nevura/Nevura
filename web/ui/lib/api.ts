export async function fetchModules(): Promise<Module[]> {
  const res = await fetch('/api/modules');
  return res.json();
}

export async function installModule(name: string) {
  await fetch(`/api/modules/install`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  });
}

export async function removeModule(name: string) {
  await fetch(`/api/modules/remove`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  });
}
export async function apiGet<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function apiPost<T>(url: string, body: unknown): Promise<T> {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function apiDelete(url: string): Promise<void> {
  const res = await fetch(url, { method: 'DELETE' });
  if (!res.ok) throw new Error(await res.text());
}

export interface VM {
  uuid: string;
  name: string;
  state: string; // running, stopped, paused...
  cpu: number; // vCPU count
  memory: number; // MB
  diskCount: number;
}

export interface Node {
  id: string;
  name: string;
  ip: string;
  status: string; // online, offline
  lastSeen: string; // timestamp
}

export async function getVMs(): Promise<VM[]> {
  const res = await fetch("/api/vm/");
  if (!res.ok) throw new Error("Erreur lors de la récupération des VMs");
  return res.json();
}

export async function getNodes(): Promise<Node[]> {
  const res = await fetch("/api/nodes/");
  if (!res.ok) throw new Error("Erreur lors de la récupération des nœuds");
  return res.json();
}

export async function snapshotVM(uuid: string, name: string) {
  return api.post("/vm/snapshot", { uuid, snapshot_name: name });
}
export async function cloneVM(uuid: string, name: string) {
  return api.post("/vm/clone", { uuid, clone_name: name });
}
export async function resizeVM(uuid: string, memory_mb: number, disk_gb: number) {
  return api.post("/vm/resize", { uuid, memory_mb, disk_gb });
}
export async function postForm(url: string, form: FormData) {
  const res = await fetch(url, { method: "POST", body: form });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
