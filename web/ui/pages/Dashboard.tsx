import React, { useEffect } from 'react';
import { useSystemStore } from '../store/systemStore';
import { useSettingsStore } from '../store/settingsStore';
import { useAlertStore } from '../store/alertStore';

const Dashboard: React.FC = () => {
  const fetchInfo = useSystemStore((s) => s.fetchInfo);
  const { hostname, timezone, osVersion, disks, ramUsed, ramTotal, cpuLoad } =
    useSystemStore();
  const alerts = useAlertStore((s) => s.alerts);

  useEffect(() => {
    fetchInfo();
  }, [fetchInfo]);

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Tableau de bord</h1>
      <section className="grid grid-cols-2 gap-4">
        <div className="card">
          <h2>Système</h2>
          <ul>
            <li>Nom d’hôte : {hostname}</li>
            <li>Timezone : {timezone}</li>
            <li>Version OS : {osVersion}</li>
          </ul>
        </div>
        <div className="card">
          <h2>Ressources</h2>
          <ul>
            <li>RAM utilisée / totale : {ramUsed} / {ramTotal} Mo</li>
            <li>Charge CPU : {cpuLoad}%</li>
          </ul>
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-semibold">Alertes système</h2>
        {alerts.map((a) => (
          <div key={a.id} className="alert">
            <strong>{a.title}</strong> — {a.message}
          </div>
        ))}
      </section>
    </div>
  );
};

export default Dashboard;
