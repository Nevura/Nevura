import React, { useEffect, useState, useRef } from "react";
import { api } from "../lib/api";
import { LucideWakeonLan, LucideTrash2, LucidePlusCircle } from "lucide-vue-next";

interface Node { id: string; name: string; ip: string; mac: string; status: string; lastSeen: string; }

export default function Nodes() {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [newNode, setNewNode] = useState<Node>({ id: '', name: '', ip: '', mac: '', status: 'online', lastSeen: '' });
  const [wolLoading, setWolLoading] = useState<string | null>(null);

  const fetchNodes = async () => {
    const res = await api.get<Node[]>("/nodes"); setNodes(res.data);
  };

  useEffect(fetchNodes, []);

  const handleWake = async (node: Node) => {
    setWolLoading(node.id);
    await api.post(`/nodes/${node.id}/wol`);
    setWolLoading(null);
  };

  const handleDelete = async (id: string) => {
    await api.delete(`/nodes/${id}`);
    fetchNodes();
  };

  const handleAdd = async () => {
    await api.post<Node>("/nodes", newNode);
    fetchNodes();
  };

  const handleDiscover = async () => {
    const res = await api.get<{ips: string[]}>("/nodes/discover");
    alert("Active IPs:\n" + res.data.ips.join("\n"));
  };

  return (
    <div className="root p-6 space-y-8">
      <h1 className="text-4xl font-bold">Gestion des Nodes</h1>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {nodes.map(node => (
          <div key={node.id} className="border rounded-lg p-4 bg-white shadow hover:shadow-lg transition">
            <h2 className="text-xl font-semibold">{node.name}</h2>
            <p><strong>IP:</strong> {node.ip}</p>
            <p><strong>MAC:</strong> {node.mac || "—"}</p>
            <p><strong>Status:</strong> {node.status}</p>
            <p><strong>Dernier contact:</strong> {new Date(node.lastSeen).toLocaleString()}</p>
            <div className="mt-4 flex space-x-2">
              <button
                disabled={wolLoading === node.id || !node.mac}
                onClick={() => handleWake(node)}
                className="btn-primary flex items-center gap-1"
              >
                {wolLoading === node.id ? 'Envoi...' : 'Wake-on-LAN'} <LucideWakeonLan />
              </button>
              <button
                onClick={() => handleDelete(node.id)}
                className="btn-danger flex items-center gap-1"
              >
                Supprimer <LucideTrash2 />
              </button>
            </div>
          </div>
        ))}
      </section>

      <section className="mt-8 space-y-4">
        <h2 className="text-2xl font-semibold">Ajouter un Node</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-2">
          {['id', 'name', 'ip', 'mac'].map(key => (
            <input
              key={key}
              placeholder={key.toUpperCase()}
              className="input"
              value={(newNode as any)[key]}
              onChange={e => setNewNode(v => ({ ...v, [key]: e.target.value }))}
            />
          ))}
          <button onClick={handleAdd} className="btn-primary flex items-center gap-1">
            Ajouter <LucidePlusCircle />
          </button>
        </div>
        <button onClick={handleDiscover} className="btn-secondary mt-2">
          Scanner le réseau
        </button>
      </section>
    </div>
  );
}
