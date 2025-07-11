import React, { useEffect, useState } from 'react';
import { useSettingsStore } from '../store/settingsStore';

const Settings: React.FC = () => {
  const {
    theme,
    autoDarkMode,
    smtpEnabled,
    notifyDesktop,
    notifyMail,
    setTheme,
    toggleDarkMode,
    setSmtpEnabled,
    setNotifyDesktop,
    setNotifyMail,
  } = useSettingsStore();
  const [availableThemes, setAvailableThemes] = useState([]);

  useEffect(() => {
    fetch('/api/themes')
      .then((r) => r.json())
      .then((d) => {
        setAvailableThemes(d);
        useSettingsStore.setState({ themesAvailable: d });
      });
  }, []);

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Paramètres</h1>
      <div className="form-group">
        <label>Thème :</label>
        <select
          value={theme}
          onChange={(e) => setTheme(e.target.value)}
          className="select"
        >
          {availableThemes.map((t: any) => (
            <option key={t.name} value={t.name}>
              {t.name}
            </option>
          ))}
        </select>
      </div>
      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={autoDarkMode}
            onChange={(e) => toggleDarkMode(e.target.checked)}
          />
          Mode sombre automatique
        </label>
      </div>
      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={smtpEnabled}
            onChange={(e) => setSmtpEnabled(e.target.checked)}
          />
          Activer SMTP
        </label>
      </div>
      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={notifyDesktop}
            onChange={(e) => setNotifyDesktop(e.target.checked)}
          />
          Notifications bureau activées
        </label>
      </div>
      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={notifyMail}
            onChange={(e) => setNotifyMail(e.target.checked)}
          />
          Notifications par email
        </label>
      </div>
    </div>
  );
};

export default Settings;
