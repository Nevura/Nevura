import React, { useEffect, useState } from 'react';

interface Volume {
  id: string;
  name: string;
  usage: number;
  size: number;
}

const Volumes: React.FC = () => {
  const [volumes, setVolumes] = useState<Volume[]>([]);
  const [newName, setNewName] = useState('');
  const [newDisks, setNewDisks] = useState<string>('');

  const fetchVolumes = () =>
    fetch('/api/system/volumes')
      .then((r) => r.json())
      .then((d) => setVolumes(d));

  useEffect(fetchVolumes, []);

  const createVolume = () => {
    fetch('/api/system/volumes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: newName, disks: newDisks.split(',') }),
    }).then(fetchVolumes);
  };

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Volumes et RAID</h1>
      <div className="flex space-x-4">
        <input
          placeholder="Nouveau volume"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          className="input"
        />
        <input
          placeholder="Disques (IDs, séparés par ,)"
          value={newDisks}
          onChange={(e) => setNewDisks(e.target.value)}
          className="input"
        />
        <button onClick={createVolume} className="btn-primary">
          Créer
        </button>
      </div>
      <ul>
        {volumes.map((v) => (
          <li key={v.id}>
            {v.name}: {v.usage}% utilisé ({v.size} Go)
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Volumes;
