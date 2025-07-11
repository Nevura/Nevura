import React, { useEffect, useState } from 'react';

interface Share {
  id: string;
  type: 'SMB' | 'FTP' | 'Nextcloud';
  name: string;
  path: string;
}

const Shares: React.FC = () => {
  const [shares, setShares] = useState<Share[]>([]);

  const fetchShares = () =>
    fetch('/api/system/shares')
      .then((r) => r.json())
      .then((d) => setShares(d));

  useEffect(fetchShares, []);

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Partages réseau</h1>
      <button
        onClick={() =>
          fetch('/api/system/shares', { method: 'POST' }).then(fetchShares)
        }
        className="btn-primary"
      >
        Ajouter un partage
      </button>
      <ul>
        {shares.map((s) => (
          <li key={s.id}>
            [{s.type}] {s.name} ➝ {s.path}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Shares;
