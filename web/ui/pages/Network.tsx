const Network: React.FC = () => {
  // fetch network config + status
  const [config, setConfig] = useState<{ ip: string; gateway: string } | null>(null);

  useEffect(() => {
    fetch('/api/system/network').then(r => r.json()).then(d => setConfig(d));
  }, []);

  const sendWake = (mac: string) => {
    fetch('/api/system/network/wake', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mac }),
    });
  };

  return (
    <div>
      <h1 className="text-2xl font-semibold">Réseau</h1>
      {config && (
        <div className="card">
          <p>IP : {config.ip}</p>
          <p>Passerelle : {config.gateway}</p>
        </div>
      )}
      <form onSubmit={e => { e.preventDefault(); sendWake((e.target as any).mac.value); }}>
        <input name="mac" placeholder="MAC address" className="input" />
        <button className="btn-primary">Wake-on‑LAN</button>
      </form>
    </div>
  );
};

export default Network;
