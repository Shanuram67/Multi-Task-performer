import React, { useState } from 'react';
import { X, Send, BookOpen } from 'lucide-react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const NewBriefModal = ({ isVisible, onClose, onBriefSubmitted }) => {
const [title, setTitle] = useState('');
const [description, setDescription] = useState('');
const [loading, setLoading] = useState(false);
const [error, setError] = useState('');

if (!isVisible) return null;

const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const username = localStorage.getItem('current_username');
    if (!username) {
        setError('User not found. Please log in again.');
        setLoading(false);
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/briefs`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, title, description }),
        });

        const data = await response.json();

        if (response.ok) {
            console.log(data.msg);
            onBriefSubmitted(data.brief_id);
            setTitle('');
            setDescription('');
            onClose();
        } else {
            setError(data.msg || `Failed to submit brief. Status: ${response.status}`);
        }
    } catch (err) {
        setError('Connection error. Please ensure the backend server is running.');
        console.error(err);
    } finally {
        setLoading(false);
    }
};

return (
    <div className="modal-overlay">
        <div className="modal-content">
            <header className="modal-header">
                <BookOpen className="w-6 h-6 text-teal-600" />
                <h2 className="modal-title">Submit New Project Brief</h2>
                <button onClick={onClose} className="btn-close"><X className="w-5 h-5" /></button>
            </header>

            {error && <p style={{ color: 'red', textAlign: 'center', marginBottom: '1rem' }}>{error}</p>}

            <form onSubmit={handleSubmit} className="form-group space-y-4">
                <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="Short Project Title (e.g., Build a task management app)"
                    required
                    className="form-input modal-input"
                />
                <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Detailed Requirements (e.g., needs user auth, task sharing, REST APIs...)"
                    rows="6"
                    required
                    className="form-input modal-textarea"
                />
                <button type="submit" className="btn-primary" disabled={loading}>
                    {loading ? 'Sending...' : 'Submit Brief to Coordinator'}
                    <Send className="w-4 h-4 ml-2" />
                </button>
            </form>
        </div>
    </div>
);


};

export default NewBriefModal;