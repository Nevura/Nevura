import React, { useEffect, useState, useRef } from "react";
import { api } from "../lib/api";
import { LucideCpu, LucideMemory, LucideHardDrive } from "@lucide/react";

interface VM {
  uuid: string;
  name: string;
  state: string;
  cpu: number;
  memory: number;
  diskCount: number;
}

export default function VMs() {
  const [vms, setVMs] = useState<VM[]>([]);
  const [creating, setCreating] = useState(false);
  const [form, setForm] = useState({ name: "", cpu: 1, memory_mb: 512, disk_gb: 20, node_id: "local" });
  const wsRef = useRef<WebSocket | null>(null);
  const [consoleLog, setConsoleLog] = useState("");

  useEffect(() => { api.get<VM[]>("/vm").then(r => setVMs(r.data)); }, []);

  const handleCreate = async () => {
    setCreating(true);
    await api.post("/vm/create", form);
    setCreating(false);
    api.get<VM[]>("/vm").then(r => setVMs(r.data));
  };

  const openConsole = (uuid: string) => {
    wsRef.current = new WebSocket(`${window.location.origin.replace(/^http/, "ws")}/api/vm/console/${uuid}`);
    wsRef.current.onmessage = e => setConsoleLog(prev => prev + e.data);
  };

  return (
    <div className="root p-6 space-y-6">
      <h1 className="text-3xl font-bold">Machines Virtuelles</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {vms.map(vm => (
          <div key={vm.uuid} className="card">
            <h2 className="font-semibold">{vm.name}</h2>
            <p><LucideCpu /> CPU: {vm.cpu}</p>
            <p><LucideMemory /> RAM: {vm.memory} Mo</p>
            <p><LucideHardDrive /> Disques: {vm.diskCount}</p>
            <p>État: {vm.state}</p>
            <button className="btn-primary" onClick={() => openConsole(vm.uuid)}>Console</button>
          </div>
        ))}
      </div>

      <div className="mt-8 p-4 border rounded">
        <h2 className="text-xl font-semibold">Créer une VM</h2>
        <input className="input mb-2" placeholder="Nom" value={form.name} onChange={e=>setForm(f=>({...f,name:e.target.value}))}/>
        <input type="number" className="input mb-2" placeholder="CPU" value={form.cpu} onChange={e=>setForm(f=>({...f,cpu:+e.target.value}))}/>
        <input type="number" className="input mb-2" placeholder="RAM Mo" value={form.memory_mb} onChange={e=>setForm(f=>({...f,memory_mb:+e.target.value}))}/>
        <input type="number" className="input mb-2" placeholder="Disque GB" value={form.disk_gb} onChange={e=>setForm(f=>({...f,disk_gb:+e.target.value}))}/>
        <button className="btn-primary w-full" disabled={creating} onClick={handleCreate}>
          {creating ? "Création..." : "Créer VM"}
        </button>
      </div>

      {consoleLog && (
        <div className="terminal mt-6 p-4 bg-black text-green-300 overflow-auto whitespace-pre-wrap">
          {consoleLog}
        </div>
      )}
    </div>
  );
}
