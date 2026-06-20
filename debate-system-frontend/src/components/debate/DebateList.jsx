// FILE: src/components/debate/DebateList.jsx

import { useState } from 'react';
import DebateCard from './Debatecard';
import LoadingSpinner from '../common/LoadingSpinner';

function DebateList() {
  // Mock data — will be replaced by API call in Part 2
  const [debates] = useState([
    {
      id: 1,
      topic: 'AI should have legal rights',
      status: 'completed',
      agents: ['Claude', 'GPT-4'],
      createdAt: '2024-06-01',
    },
    {
      id: 2,
      topic: 'Quantum computing will break encryption',
      status: 'active',
      agents: ['Claude', 'Gemini'],
      createdAt: '2024-06-05',
    },
    {
      id: 3,
      topic: 'Open source AI is safer than closed source',
      status: 'pending',
      agents: ['GPT-4', 'Gemini'],
      createdAt: '2024-06-08',
    },
  ]);
  
  const [selectedDebateId, setSelectedDebateId] = useState(null);
  const [filter, setFilter] = useState('all');
  
  // Derived data — computed from state, not stored separately
  const filteredDebates = filter === 'all'
    ? debates
    : debates.filter(d => d.status === filter);
  
  function handleSelectDebate(id) {
    setSelectedDebateId(id);
    console.log('Selected debate:', id);
    // Later: navigate to debate detail page
  }
  
  return (
    <div className="debate-list">
      <div className="debate-list-header">
        <h2>Debates ({filteredDebates.length})</h2>
        
        <div className="filter-buttons">
          {['all', 'active', 'completed', 'pending'].map(f => (
            <button
              key={f}
              className={`filter-btn ${filter === f ? 'active' : ''}`}
              onClick={() => setFilter(f)}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
      </div>
      
      {filteredDebates.length === 0 ? (
        <p className="empty-state">No debates found for this filter.</p>
      ) : (
        <div className="debate-grid">
          {filteredDebates.map(debate => (
            <DebateCard
              key={debate.id}
              debate={debate}
              onSelect={handleSelectDebate}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default DebateList;