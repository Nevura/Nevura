import { useEffect, useState } from 'react';
import { installModule, removeModule, fetchModules } from '../lib/api';
import { useSystemStore } from '../store/systemStore';

type Module = {
  name: string;
  description: string;
  installed: boolean;
  requires: string[];
  ramUsage: number;
};

const Modules: React.FC = () => {
  const [modules, setModules] = useState<Module[]>([]);
  const [loading, setLoading] = useState(false);
  const { systemInfo } = useSystemStore();

  useEffect(() => {
    refreshModules();
  }, []);

  const refreshModules = async () => {
    const res = await fetchModules();
    setModules(res);
  };

  const toggleModule = async (mod: Module) => {
    setLoading(true);
    try {
      if (mod.installed) {
        await removeModule(mod.name);
      } else {
        const ramLeft = systemInfo?.ramTotal - systemInfo?.ramUsed;
        if (ramLeft && ramLeft < mod.ramUsage) {
          alert("Mémoire insuffisante pour installer ce module.");
          return;
        }
        await installModule(mod.name);
      }
      await refreshModules();
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Modules</h1>
      <div className="grid md:grid-cols-2 gap-6">
        {modules.map((mod) => (
          <div key={mod.name} className="card flex flex-col justify-between">
            <div>
              <h2 className="text-xl font-semibold">{mod.name}</h2>
              <p className="text-sm text-gray-600">{mod.description}</p>
              <ul className="text-xs mt-2">
                {mod.requires.map((r, i) => (
                  <li key={i}>• {r}</li>
                ))}
              </ul>
              <p className="text-xs mt-1 text-gray-400">RAM estimée : {mod.ramUsage} Mo</p>
            </div>
            <button
              onClick={() => toggleModule(mod)}
              disabled={loading}
              className={`mt-4 ${
                mod.installed ? 'bg-red-600 hover:bg-red-700' : 'bg-blue-600 hover:bg-blue-700'
              } text-white px-4 py-2 rounded-md`}
            >
              {mod.installed ? 'Supprimer' : 'Installer'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Modules;
