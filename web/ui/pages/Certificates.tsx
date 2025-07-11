const Certificates: React.FC = () => {
  const [certs, setCerts] = useState<{ id: string; domain: string; validUntil: string }[]>([]);

  useEffect(() => {
    fetch('/api/system/certificates').then(r => r.json()).then(setCerts);
  }, []);

  const renew = (id: string) => {
    fetch(`/api/system/certificates/${id}/renew`, { method: 'POST' }).then(() => {
      setCerts(certs.map(c => c.id === id ? { ...c, validUntil: 'pending...' } : c));
    });
  };

  return (
    <div className="space-y-6 p-6">
      <h1 className="text-3xl font-bold">Certificats TLS</h1>
      <ul className="space-y-4">
        {certs.map(c => (
          <li key={c.id} className="card flex justify-between items-center">
            <div>
              <p><strong>{c.domain}</strong></p>
              <p>Valide jusqu’au : {c.validUntil}</p>
            </div>
            <button onClick={() => renew(c.id)} className="btn-secondary">
              Renouveler
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Certificates;
