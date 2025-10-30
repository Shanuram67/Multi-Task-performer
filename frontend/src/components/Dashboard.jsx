// Dashboard.jsx
import React, { useState, useEffect } from 'react';
import { LayoutDashboard as DashboardIcon, ListChecks, Share, PlusCircle, CheckCircle } from 'lucide-react';
import GenericCard from './GenericCard';
import NewBriefModal from './NewBriefModal'; 

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// TaskItem Sub-Component (FIX: Use statusClass)
const TaskItem = ({ task }) => {
    // FIX: Assign statusClass and agentClass correctly for use in JSX
    const statusClass = `status-${task.status.toLowerCase().replace(' ', '-')}`;
    const agentClass = `agent-${task.agent.toLowerCase()}`;

    return (
      <div className="task-item">
        {/* Task Details (Stacks vertically on mobile) */}
        <div className="task-details">
          <p className="task-title">{task.title}</p>
          <div className="task-meta">
            <span className={`agent-tag ${agentClass}`}>
              {task.agent}
            </span>
            <span className="meta-divider">•</span>
            {/* FIX: Use statusClass on the display tag */}
            <span className={`status-tag ${statusClass}`}>
              {task.status}
            </span>
          </div>
        </div>

        {/* Status and Action Button (Aligns horizontally on larger screens) */}
        <div className="task-actions-group">
          <button className="btn-action-icon">
            {task.status === 'Done' ? <CheckCircle className="w-5 h-5" /> : <Share className="w-5 h-5" />}
          </button>
        </div>
      </div>
    );
};


const Dashboard = ({ user, onLogout }) => {
    const [tasks, setTasks] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [loading, setLoading] = useState(true);

    // Function to fetch tasks from the Backend API (FIX: Now uses the implemented endpoint)
  const fetchTasks = async () => {
  const currentUser = localStorage.getItem("current_username");
  if (!currentUser) return onLogout();

  try {
    const response = await fetch(`${API_URL}/api/tasks/${currentUser}`);
    const data = await response.json();
    setTasks(data.tasks || []);
  } catch (error) {
    console.error("Error fetching tasks:", error);
  } finally {
    setLoading(false);
  }
};


    useEffect(() => {
        fetchTasks();
    }, []);

    const handleBriefSubmitted = () => {
        // Refresh task list after submission
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
                    {/* FIX: New Brief Button now opens the modal */}
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
                            tasks.map(task => <TaskItem key={task.id} task={task} />)
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