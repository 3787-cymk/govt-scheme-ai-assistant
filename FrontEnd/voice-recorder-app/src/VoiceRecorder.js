import React, { useState, useRef } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay, faPause, faStop, faDownload, faSpinner, faPaperPlane } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
import './VoiceRecorder.css';

const VoiceRecorder = () => {
  const [processedAudioURL, setProcessedAudioURL] = useState('');
  const [processedText, setProcessedText] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const [textInput, setTextInput] = useState('');
  // Set default language to English
  const [selectedLanguage, setSelectedLanguage] = useState('en-US');

  const audioRef = useRef(null);

  const handleTextInputChange = (event) => {
    setTextInput(event.target.value);
  };

  const handleLanguageChange = (event) => {
    setSelectedLanguage(event.target.value);
  };

  const uploadInput = async () => {
    setIsLoading(true);
    setProcessedAudioURL('');
    setProcessedText('');

    try {
      if (textInput.trim() !== '') {
        const formData = new FormData();
        formData.append('text', textInput);
        formData.append('language', selectedLanguage);

        const initial_response = await axios.post('http://localhost:8000/chat', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        if (initial_response) {
          const result = initial_response.data;

          const response = await axios.get('http://localhost:8000/download', { responseType: 'blob' });
          setIsLoading(false);
          setProcessedText(result.response);
          const contentType = response.headers['content-type'] || 'audio/mpeg';
          const audioBlob = new Blob([response.data], { type: contentType });
          const url = window.URL.createObjectURL(audioBlob);
          setProcessedAudioURL(url);
          playAudio(url);
        }
      }
    } catch (error) {
      console.error('Error processing input:', error);
      setProcessedText("There was an error processing your request");
    } finally {
      setIsLoading(false);
    }
  };

  const playAudio = (url) => {
    if (audioRef.current) {
      audioRef.current.pause();
    }
    const audio = new Audio(url);
    audioRef.current = audio;

    audio.play();
    setIsPlaying(true);

    audio.onended = () => {
      setIsPlaying(false);
      window.URL.revokeObjectURL(url);
    };
  };

  const pauseAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      setIsPlaying(false);
    }
  };

  const stopAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setIsPlaying(false);
    }
  };

  const downloadAudio = () => {
    if (processedAudioURL) {
      const link = document.createElement('a');
      link.href = processedAudioURL;
      link.setAttribute('download', 'processed-audio.mp3');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <div className="recorder-container">
      <div className="language-selector">
        <label htmlFor="language-select">Select Language:</label>
        <select
          id="language-select"
          value={selectedLanguage}
          onChange={handleLanguageChange}
          className="language-dropdown"
          disabled={isLoading}
        >
          <option value="en-US">English</option>
          <option value="hi-IN">Hindi</option>
          <option value="pa-IN">Punjabi</option>
        </select>
      </div>

      <div className="text-input-container">
        <textarea
          value={textInput}
          onChange={handleTextInputChange}
          placeholder="Type your question here..."
          disabled={isLoading}
          className="text-input"
        />
        <button
          onClick={uploadInput}
          disabled={isLoading || textInput.trim() === ''}
          className="submit-button"
        >
          {isLoading ? <FontAwesomeIcon icon={faSpinner} spin /> : <><FontAwesomeIcon icon={faPaperPlane} /> Submit</>}
        </button>
      </div>

      {isLoading && (
        <div className="loading-icon-container">
          <FontAwesomeIcon icon={faSpinner} spin size="3x" />
          <p>Processing...</p>
        </div>
      )}

      {!isLoading && processedText && (
        <div className="output-container">
          <p>Key Insights:</p>
          <div className="output-textbox auto-expand">
            {processedText}
          </div>
        </div>
      )}

      {!isLoading && processedAudioURL && (
        <div className="controls">
          <button onClick={() => playAudio(processedAudioURL)} disabled={isPlaying} className="control-button">
            <FontAwesomeIcon icon={faPlay} size="2x" />
          </button>
          <button onClick={pauseAudio} disabled={!isPlaying} className="control-button">
            <FontAwesomeIcon icon={faPause} size="2x" />
          </button>
          <button onClick={stopAudio} disabled={!isPlaying} className="control-button">
            <FontAwesomeIcon icon={faStop} size="2x" />
          </button>
          <button onClick={downloadAudio} disabled={!processedAudioURL} className="control-button">
            <FontAwesomeIcon icon={faDownload} size="2x" />
          </button>
        </div>
      )}
    </div>
  );
};

export default VoiceRecorder;
