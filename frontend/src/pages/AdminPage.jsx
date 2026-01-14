import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';

const AdminPage = () => {
  const { user } = useAuth();
  const [tps, setTps] = useState([]);
  const [vms, setVms] = useState([]);
  const [newTp, setNewTp] = useState({ title: '', description: '', instructions: '', template: '' });

  useEffect(() => {
    if (user?.role !== 'teacher') {
      // Redirect or show error
      return;
    }
    fetchTPs();
    fetchVMs();
  }, [user]);

  const fetchTPs = async () => {
    try {
      const response = await API.get('/admin/tp');
      setTps(response.data);
    } catch (error) {
      console.error('Error fetching TPs:', error);
    }
  };

  const fetchVMs = async () => {
    try {
      const response = await API.get('/admin/vm');
      setVms(response.data);
    } catch (error) {
      console.error('Error fetching VMs:', error);
    }
  };

  const createTP = async () => {
    try {
      await API.post('/admin/tp', newTp);
      setNewTp({ title: '', description: '', instructions: '', template: '' });
      fetchTPs();
    } catch (error) {
      console.error('Error creating TP:', error);
    }
  };

  const assignTP = async (tpId, studentIds) => {
    try {
      await API.post(`/admin/tp/${tpId}/assign`, { students: studentIds });
    } catch (error) {
      console.error('Error assigning TP:', error);
    }
  };

  return (
    <div className="admin-page">
      <h1>Espace Enseignant</h1>

      <section>
        <h2>Créer un TP</h2>
        <input
          type="text"
          placeholder="Titre"
          value={newTp.title}
          onChange={(e) => setNewTp({ ...newTp, title: e.target.value })}
        />
        <textarea
          placeholder="Description"
          value={newTp.description}
          onChange={(e) => setNewTp({ ...newTp, description: e.target.value })}
        />
        <textarea
          placeholder="Instructions (Markdown)"
          value={newTp.instructions}
          onChange={(e) => setNewTp({ ...newTp, instructions: e.target.value })}
        />
        <input
          type="text"
          placeholder="Template Proxmox"
          value={newTp.template}
          onChange={(e) => setNewTp({ ...newTp, template: e.target.value })}
        />
        <button onClick={createTP}>Créer TP</button>
      </section>

      <section>
        <h2>Monitoring des VMs</h2>
        <table>
          <thead>
            <tr>
              <th>TP</th>
              <th>Étudiant</th>
              <th>Statut</th>
              <th>RAM</th>
            </tr>
          </thead>
          <tbody>
            {vms.map((vm) => (
              <tr key={vm.id}>
                <td>{vm.tp_title}</td>
                <td>{vm.student_name}</td>
                <td>{vm.status}</td>
                <td>{vm.ram} MB</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
};

export default AdminPage; 
