import React from 'react';
import { useAlertStore } from '../store/alertStore';

const Alerts: React.FC = () => {
  const alerts = useAlertStore((s) => s.alerts);
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold">Alertes</h1>
      <ul className="space-y-4">
        {alerts.map((a) => (
          <li key={a.id} className="alert">
            <strong>{a.title}</strong>: {a.message}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Alerts;
