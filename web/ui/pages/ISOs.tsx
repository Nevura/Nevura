import React, { useEffect, useState } from "react";
import { api } from "../lib/api";
import { formatBytes } from "../lib/format";

interface ISOInfo { filename: string; os?: string; version?: string; size: number; added_on: string; }

export default function ISOs() {
  const [isos, setIsos] = useState<ISOInfo[]>([]);
  const [url, setUrl] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const fetchIsos = async () => {
    const res = await api.get<ISOInfo[]>("/iso");
    setIsos(res.data);
  };

  useEffect(() => { fetchIsos(); }, []);

  const handleDownload = async () => {
    await api.post("/iso/download", { url });
    fetchIsos();
  };

  const handleUpload = async () => {
    if (!file) return;
    const form = new FormData();
    form.append("file", file);
    await api.postForm("/iso/upload", form);
    fetchIsos();
  };

  const handleDelete = async (fn: string) => {
    await api.delete(`/iso/${fn}`);
    fetchIsos();
  };

  return (
    <div className="root p-6 space-y-6">
      <h1 className="text-3xl font-bold">Gestion des ISOs</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card space-y-4">
          <h2 className="text-xl font-semibold">ISO disponibles</h2>
          <table className="w-full">
            <thead><tr><th>Nom</th><th>OS</th><th>Ver.</th><th>Taille</th><th>Ajouté</th><th>Actions</th></tr></thead>
            <tbody>
              {isos.map(i => (
                <tr key={i.filename}>
                  <td>{i.filename}</td>
                  <td>{i.os || "-"}</td>
                  <td>{i.version || "-"}</td>
                  <td>{formatBytes(i.size)}</td>
                  <td>{new Date(Number(i.added_on)*1000).toLocaleString()}</td>
                  <td><button className="btn-danger" onClick={()=>handleDelete(i.filename)}>Suppr.</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="space-y-6">
          <div className="card p-4">
            <h2 className="text-xl font-semibold">Télécharger depuis URL</h2>
            <input type="url" placeholder="https://..." value={url} onChange={e=>setUrl(e.target.value)} className="input"/>
            <button className="btn-primary mt-2" onClick={handleDownload}>Télécharger</button>
          </div>

          <div className="card p-4">
            <h2 className="text-xl font-semibold">Uploader depuis local</h2>
            <input type="file" accept=".iso" onChange={e=>setFile(e.target.files?.[0]||null)} className="input"/>
            <button className="btn-primary mt-2" onClick={handleUpload}>Uploader</button>
          </div>
        </div>
      </div>
    </div>
  );
}
