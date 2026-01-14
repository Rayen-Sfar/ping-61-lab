import React from 'react';

const TPList = ({ tps, onStartTP }) => {
  return (
    <div className="tp-list">
      <h2>Vos TPs assignés</h2>
      {tps.length === 0 ? (
        <p>Aucun TP assigné.</p>
      ) : (
        <div className="tp-cards">
          {tps.map((tp) => (
            <div key={tp.id} className="tp-card">
              <h3>{tp.title}</h3>
              <p>{tp.description}</p>
              <p>Statut VM: {tp.vm_status || 'Arrêtée'}</p>
              <button onClick={() => onStartTP(tp.id)}>
                {tp.vm_status === 'Running' ? 'Reprendre' : 'Démarrer'} le TP
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TPList;