// FILE: src/components/debate/DebateCard.jsx

function DebateCard({ debate, onSelect }) {
  const { id, topic, status, agents, createdAt } = debate;
  
  // Status badge color logic
  const statusColors = {
    active: '#22c55e',    // green
    completed: '#3b82f6', // blue
    pending: '#f59e0b',   // amber
  };
  
  return (
    <div 
      className="debate-card"
      onClick={() => onSelect(id)}
      style={{ cursor: 'pointer' }}
    >
      <div className="debate-card-header">
        <h3>{topic}</h3>
        <span 
          className="status-badge"
          style={{ color: statusColors[status] || '#6b7280' }}
        >
          ● {status}
        </span>
      </div>
      
      <div className="debate-card-agents">
        {agents && agents.map(agent => (
          <span key={agent} className="agent-chip">
            {agent}
          </span>
        ))}
      </div>
      
      <div className="debate-card-footer">
        <small>{createdAt || 'Date unknown'}</small>
      </div>
    </div>
  );
}

export default DebateCard;