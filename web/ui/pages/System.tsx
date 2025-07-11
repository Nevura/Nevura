import React, { useEffect } from 'react';
import { useSystemStore } from '../store/systemStore';

const System: React.FC = () => {
  const { hostname, timezone, disks, setTimezone, setHostname } =
    useSystemStore();

  const updateTimezone = async (tz: string) => {
    await fetch('/api/system/update', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ timezone: tz }),
    });
    setTimezone(tz);
  };

  const updateHostname = async (hn: string) => {
    await fetch('/api/system/update', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ hostname: hn }),
    });
    setHostname(hn);
  };

  useEffect(() => {
    fetch('/api/system/info')
      .then((r) => r.json())
      .then((data) => {
        useSystemStore.setState({
          hostname: data.hostname,
          timezone: data.timezone,
          osVersion: data.osVersion,
        });
      });
  }, []);

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Paramètres système</h1>
      <div className="space-y-4">
        <label>
          Nom d’hôte :
          <input
            type="text"
            defaultValue={hostname}
            onBlur={(e) => updateHostname(e.target.value)}
            className="input"
          />
        </label>
        <label>
          Timezone :
          <input
            type="text"
            defaultValue={timezone}
            onBlur={(e) => updateTimezone(e.target.value)}
            className="input"
          />
        </label>
      </div>
      <section>
        <h2 className="text-2xl font-semibold">Disques disponibles</h2>
        <ul>
          {disks.map((d) => (
            <li key={d.id}>
              {d.name}: {d.usage}% utilisé, fs: {d.fsType}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
};

export default System;
