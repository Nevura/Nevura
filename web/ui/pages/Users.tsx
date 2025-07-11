import React, { useEffect, useState } from 'react';

interface User {
  id: number;
  username: string;
  email: string;
  isAdmin: boolean;
}

const Users: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [newEmail, setNewEmail] = useState('');
  const [newUser, setNewUser] = useState('');

  useEffect(() => {
    fetch('/api/users')
      .then((r) => r.json())
      .then((d) => setUsers(d));
  }, []);

  const createUser = () => {
    fetch('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: newUser, email: newEmail }),
    })
      .then((r) => r.json())
      .then((u) => setUsers((s) => [...s, u]));
  };

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Utilisateurs</h1>
      <div className="space-y-4">
        <input
          placeholder="Nom utilisateur"
          value={newUser}
          onChange={(e) => setNewUser(e.target.value)}
          className="input"
        />
        <input
          type="email"
          placeholder="Email"
          value={newEmail}
          onChange={(e) => setNewEmail(e.target.value)}
          className="input"
        />
        <button onClick={createUser} className="btn-primary">
          Créer
        </button>
      </div>
      <ul>
        {users.map((u) => (
          <li key={u.id} className="flex justify-between">
            <span>{u.username} ({u.email})</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Users;
