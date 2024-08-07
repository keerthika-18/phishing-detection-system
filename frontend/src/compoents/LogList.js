import React, { useState, useEffect } from 'react';
import axios from 'axios';

const LogList = () => {
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/logs')
            .then(response => setLogs(response.data))
            .catch(error => console.error('Error fetching logs:', error));
    }, []);

    return (
        <div className="log-list">
            {logs.length > 0 ? (
                <ul>
                    {/* {logs.map((log, index) => (
                        <li key={index}>
                            <strong>Type:</strong> {log.contentType} <br />
                            <strong>Content:</strong> {log.content} <br />
                            <strong>Timestamp:</strong> {new Date(Number(log.timestamp) * 1000).toLocaleString()} <br />
                        </li>
                    ))} */}
                </ul>
            ) : (
                <p>No logs available.</p>
            )}
        </div>
    );
};

export default LogList;
