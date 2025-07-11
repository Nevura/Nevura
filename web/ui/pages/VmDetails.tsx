import React, { useEffect, useState, useRef } from "react";
import { api } from "../lib/api";
import { Line } from "recharts";

interface VMDetail { uuid: string; name: string; os?: string; ip?: string; hostname?: string; cpu_used_percent: number; cpu_alloc: number; ram_used_mb: number; ram_alloc_mb: number; disk_used_gb: number; disk_alloc_gb: number; latency_percent: number; virtio_installed: boolean; }

export default function VmDetails({ uuid }: { uuid: string }) {
  const [vm, setVm] = useState<VMDetail | null>(null);
  const [consoleLog, setConsoleLog] = useState<string>("");
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    api.get<VMDetail>(`/vm/${uuid}`).then(r => setVm(r.data));
    ws.current = new WebSocket(`${window.location.origin.replace(/^http/, "ws")}/api/vm/console/${uuid}`);
    ws.current.onmessage = e => setConsoleLog(prev => prev + e.data);
  }, [uuid]);

  if (!vm) return null;

  const data = [
    { name: "CPU", value: vm.cpu_used_percent },
    { name: "RAM", value: (vm.ram_used_mb / vm.ram_alloc_mb) * 100 },
    { name: "Disk", value: (vm.disk_used_gb / vm.disk_alloc_gb) * 100 },
    { name: "Latency", value: vm.latency_percent }
  ];
  const colors = (v: number) => v < 50 ? "#10B981" : v < 85 ? "#F59E0B" : v < 95 ? "#EF4444" : "#000000";

  return (
    <div className="root p-6 space-y-6">
      <h1 className="text-3xl font-bold">{vm.name}</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Line width={300} height={200} data={data} dataKey="value" stroke="#2563EB" label={{ position: "top" }} />
        <div className="card space-y-2">
          <p><strong>OS :</strong> {vm.os}</p>
          <p><strong>IP :</strong> {vm.ip || "—"}</p>
          <p><strong>CPU utilisé :</strong> {vm.cpu_used_percent.toFixed(1)} % / {vm.cpu_alloc}</p>
          <p><strong>RAM utilisé :</strong> {vm.ram_used_mb} Mo / {vm.ram_alloc_mb} Mo</p>
          <p><strong>Stockage utilisé :</strong> {vm.disk_used_gb.toFixed(2)} Go / {vm.disk_alloc_gb.toFixed(2)} Go</p>
          <p><strong>Latence :</strong> {vm.latency_percent.toFixed(1)} %</p>
          {!vm.virtio_installed && vm.os?.toLowerCase().startsWith("windows") && (
            <button className="btn-primary" onClick={() => api.post(`/vm/${uuid}/install-virtio`)}>
              Installer Virtio Drivers
            </button>
          )}
        </div>
      </div>
      <div className="terminal p-4 bg-black text-green-300 overflow-auto whitespace-pre-wrap">
        {consoleLog}
      </div>
    </div>
  );
}
