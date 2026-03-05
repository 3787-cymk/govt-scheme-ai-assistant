// src/App.js
import React from 'react';
import VoiceRecorder from './VoiceRecorder';
import './App.css';

function App() {
  return (
    <div className="app-shell">
      <div className="app-gradient" />

      <main className="app-layout">
        <section className="app-intro">
          <p className="app-kicker">Government scheme assistant</p>
          <h1 className="app-title">Discover the right support.</h1>
          <p className="app-subtitle">
            Type your question below and get a clear explanation of
            relevant schemes, eligibility, and next steps in plain words.
          </p>

          <div className="app-highlights">
            <div className="app-highlight-chip">Built for real citizens</div>
          </div>
        </section>

        <section className="app-panel">
          <header className="app-panel-header">
            <span className="app-badge">Live assistant</span>
            <span className="app-panel-caption">
              Ask about education, health, agriculture, insurance and more.
            </span>
          </header>

          <div className="app-panel-body">
            <VoiceRecorder />
          </div>
        </section>
      </main>

    </div>
  );
}

export default App;