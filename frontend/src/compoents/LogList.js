import React, { useState, useEffect } from 'react';
import axios from 'axios';

const LogList = () => {
    const [logs, setLogs] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/logs');
                console.log('Logs fetched:', response.data); // Debug log
                setLogs(response.data);
            } catch (error) {
                console.error('Error fetching logs:', error);
                setError('Failed to fetch logs');
            }
        };

        fetchLogs();
    }, []);

    return (
        <div className="log-list">
            {error && <p>{error}</p>}
            {logs.length > 0 ? (
                <ul>
                    {/* {logs.map((log, index) => (
                        // <li key={index}>
                        //     <strong>Content:</strong> {log.content} <br />
                        //     <strong>Content Type:</strong> {log.contentType} <br />
                        //     <strong>Timestamp:</strong> {new Date(log.timestamp * 1000).toLocaleString()} <br />
                        // </li>
                    ))} */}
                </ul>
            ) : (
                <p>No logs available.</p>
            )}
        </div>
    );
};

export default LogList;
