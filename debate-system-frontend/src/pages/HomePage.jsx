import { useState } from 'react';

import Layout from '../components/ui/Layout.jsx';
import Loading from '../components/ui/Loading.jsx';
import Error from '../components/ui/Error.jsx';

import DebateForm from '../components/features/DebateForm.jsx';
import DebateResult from '../components/features/DebateResult.jsx';

import { streamDebate } from '../services/debateService.js';

const HomePage = () => {

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [status, setStatus] = useState('');

  const [proponent, setProponent] = useState(null);
  const [critic, setCritic] = useState(null);
  const [moderator, setModerator] = useState(null);

  const handleDebateSubmit = async (topic) => {

    setLoading(true);

    setError(null);

    setStatus('');

    setProponent(null);
    setCritic(null);
    setModerator(null);

    try {

      await streamDebate(topic, {

        onStatus(data) {
          setStatus(data);
        },

        onProponent(data) {
          setProponent(data);
        },

        onCritic(data) {
          setCritic(data);
        },

        onModerator(data) {
          setModerator(data);
        },

        onDone() {
          setLoading(false);
        },

        onError(err) {
          setError(String(err));
          setLoading(false);
        },

      });

    } catch (err) {

      setError(err.message);

      setLoading(false);

    }

  };

  return (
    <Layout>

      <div style={{ maxWidth: '760px', margin: '0 auto' }}>

        <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
          <h1 style={{
            color: 'white',
            fontSize: '2rem',
            fontWeight: '700'
          }}>
            Multi-Agent Debate System
          </h1>

          <p style={{ color: '#6b7280' }}>
            Powered by three AI agents
          </p>
        </div>

        <div style={{
          background: '#111127',
          border: '1px solid #1e1e3a',
          borderRadius: '16px',
          padding: '2rem',
          marginBottom: '2rem'
        }}>

          <DebateForm
            onSubmit={handleDebateSubmit}
            isLoading={loading}
          />

        </div>

        {loading && (
          <Loading
            message={status || 'Running debate...'}
          />
        )}

        {error && (
          <Error message={error} />
        )}

        {(proponent || critic || moderator) && (

          <div style={{
            background: '#111127',
            border: '1px solid #1e1e3a',
            borderRadius: '16px',
            padding: '2rem'
          }}>

            <DebateResult
              proponent={proponent}
              critic={critic}
              moderator={moderator}
            />

          </div>

        )}

      </div>

    </Layout>
  );

};

export default HomePage;