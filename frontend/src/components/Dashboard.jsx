// Dashboard.jsx
import React, { useState, useEffect } from 'react';
import { LayoutDashboard as DashboardIcon, ListChecks, PlusCircle, CheckCircle, X } from 'lucide-react';
import GenericCard from './GenericCard';
import NewBriefModal from './NewBriefModal'; 
import './styles.CSS';

// NOTE: Adjusted imports - removed unused 'Share'

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// TaskItem Sub-Component
const TaskItem = ({ task, onDelete, onReview }) => {
  // FIX: Using task.status for statusClass as intended
  const statusClass = `status-${task.status.toLowerCase().replace(' ', '-')}`;
  const agentClass = `agent-${task.agent.toLowerCase()}`;

    return (
        <div className="task-item">
      <div className="task-details">
        <p className="task-title">{task.title}</p>
        <div className="task-meta">
          <span className={`agent-tag ${agentClass}`}>{task.agent}</span>
          <span className="meta-divider">•</span>
          <span className={`status-tag ${statusClass}`}>{task.status}</span>
        </div>
      </div>

      <div className="task-actions-group">
        <button onClick={() => onReview(task.id)} className="btn-action-icon" title="Review Task">
          <CheckCircle className="w-5 h-5 text-green-600" />
        </button>
        <button onClick={() => onDelete(task.id)} className="btn-action-icon" title="Delete Task">
          <X className="w-5 h-5 text-red-600" />
        </button>
      </div>
    </div>
    );
};

const Dashboard = ({ user, onLogout }) => {
    const [tasks, setTasks] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [loading, setLoading] = useState(true);

    // Function to fetch tasks from the Backend API
  const fetchTasks = async () => {
  const currentUser = localStorage.getItem("current_username");
  // Guard clause for unauthenticated users
  if (!currentUser) return onLogout();

  try {
    const response = await fetch(`${API_URL}/api/tasks/${currentUser}`);
    // Check for HTTP errors before parsing JSON
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    setTasks(data.tasks || []);
  } catch (error) {
    console.error("Error fetching tasks:", error);
  } finally {
    setLoading(false);
  }
};

    // --- DELETE TASK --- (Moved inside Dashboard to access fetchTasks)
  const handleDeleteTask = async (taskId) => {
    try {
      const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
        method: 'DELETE'
      });
      if (!response.ok) {
        throw new Error(`Failed to delete task: ${response.status}`);
      }
      // Optional: const data = await response.json(); console.log(data.msg);
      fetchTasks(); // refresh
    } catch (error) {
      console.error('Delete error:', error);
      alert('Failed to delete task.');
    }
  };

    // --- REVIEW TASK --- (Moved inside Dashboard to access fetchTasks)
  const handleReviewTask = async (taskId) => {
    try {
      const response = await fetch(`${API_URL}/api/review/${taskId}`, {
        method: 'POST'
      });
      if (!response.ok) {
        throw new Error(`Failed to review task: ${response.status}`);
      }
      const data = await response.json();
      alert(`Review: ${data.feedback}`);
      fetchTasks(); // refresh
    } catch (error) {
      console.error('Review error:', error);
      alert('Failed to review task.');
    }
  };


    useEffect(() => {
        fetchTasks();
    }, []); // Empty dependency array means this runs once on mount

    const handleBriefSubmitted = () => {
        // Close modal and refresh task list after submission
        setIsModalVisible(false);
        fetchTasks();
    };

    const handleLogoutClick = () => {
        localStorage.removeItem('access_token'); // Clear JWT
        localStorage.removeItem('current_username');
        onLogout();
    };

    return (
        <div className="dashboard-layout">
            <header className="dashboard-header">
                <div className="header-title-group">
                    <DashboardIcon className="card-icon" />
                    <h1 className="header-title">Agent Task Dashboard</h1>
                </div>
                <div className="header-user-info">
                    <span className="user-text">Logged in as: <span className="user-id">{user}</span></span>
                    <button onClick={handleLogoutClick} className="btn-logout">
                        Logout
                    </button>
                </div>
            </header>

            <GenericCard title="Technical Task Breakdown (Active Sprint)" icon={ListChecks}>
                <div className="task-list-controls">
                        <button onClick={() => setIsModalVisible(true)} className="btn-new-brief">
                        <PlusCircle className="w-4 h-4" />
                        <span>New Brief</span>
                    </button>
                </div>

                {loading ? (
                    <p style={{ textAlign: 'center' }}>Loading tasks...</p>
                ) : (
                    <div className="tasks-container">
                        {tasks.length > 0 ? (
                            tasks.map(task => (
                                // FIX: Only one task list rendering block. Passed onDelete and onReview props.
                                <TaskItem
                                    key={task.id}
                                    task={task}
                                    onDelete={handleDeleteTask}
                                    onReview={handleReviewTask}
                                />
                            ))
                        ) : (
                            <p style={{ textAlign: 'center', padding: '2rem' }}>No tasks found. Submit a new brief!</p>
                        )}
                    </div>
                )}
            </GenericCard>

            {/* Modal integration */}
            <NewBriefModal 
                isVisible={isModalVisible} 
                onClose={() => setIsModalVisible(false)} 
                onBriefSubmitted={handleBriefSubmitted}
            />
        </div>
    );
};

export default Dashboard;