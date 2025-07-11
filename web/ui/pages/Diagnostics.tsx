const Diagnostics: React.FC = () => {
  const [stats, setStats] = useState({ cpu: 0, ramUsed: 0, ramTotal: 0 });
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    fetch('/api/system/stats').then(r => r.json()).then(d => setStats(d));
    fetch('/api/system/logs').then(r => r.json()).then(d => setLogs(d));
  }, []);

  const doUpdate = () => {
    fetch('/api/system/update', { method: 'POST' });
  };

  return (
    <div className="space-y-6 p-6">
      <h1 className="text-3xl font-bold">Diagnostics système</h1>
      <div className="card">
        <p>CPU utilisation : {stats.cpu}%</p>
        <p>RAM : {stats.ramUsed} / {stats.ramTotal} Mo</p>
      </div>
      <button onClick={doUpdate} className="btn-primary">Lancer la mise à jour</button>
      <div>
        <h2 className="text-2xl">Logs récents</h2>
        <ul className="font-mono text-xs">{logs.map((l,i) => <li key={i}>{l}</li>)}</ul>
      </div>
    </div>
  );
};

export default Diagnostics;
