import React, { useState } from 'react';
import { LogIn, User, Key } from 'lucide-react';
import GenericCard from './GenericCard';
import './styles.CSS';


const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const LoginPage = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isRegister, setIsRegister] = useState(false);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        const endpoint = isRegister ? `${API_URL}/api/auth/register` : `${API_URL}/api/auth/login`;

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

         const data = await response.json();
if (response.ok && data.access_token) {
  localStorage.setItem("access_token", data.access_token);
  localStorage.setItem("current_username", username);
  onLogin(username, data.access_token);
}

 else {
                setError(data.msg || 'Authentication failed. Check credentials.');
            }
        } catch (err) {
            setError('Could not connect to the server. Check console for details.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <GenericCard title={isRegister ? "Agent Registration" : "Agent Login"} icon={LogIn}>
            <form onSubmit={handleSubmit} className="form-group space-y-4">
                {/* Username Input */}
                <div className="form-group">
                    <label htmlFor="username" className="form-label">Agent ID</label>
                    <div className="input-wrapper">
                        <User className="input-icon" />
                        <input
                            id="username"
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            className="form-input"
                            placeholder="Enter your Agent ID"
                        />
                    </div>
                </div>
                
                {/* Password Input */}
                <div className="form-group">
                    <label htmlFor="password" className="form-label">Authorization Key</label>
                    <div className="input-wrapper">
                        <Key className="input-icon" />
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className="form-input"
                            placeholder="Enter your secret key"
                        />
                    </div>
                </div>
                
                {/* Display error message */}
                {error && <p className="text-red-600 text-sm text-center font-medium">{error}</p>}
                
                <button type="submit" className="btn-primary" disabled={loading}>
                    {loading ? 'Processing...' : (isRegister ? 'Register & Log In' : 'Sign In')}
                </button>
            </form>

            <p className="auth-toggle-text">
                {isRegister ? "Already have an account?" : "New to the platform?"}
                <button
                    onClick={() => setIsRegister(!isRegister)}
                    className="auth-toggle-btn"
                >
                    {isRegister ? 'Log In' : 'Create Agent Profile'}
                </button>
            </p>
        </GenericCard>
    );
};

export default LoginPage;