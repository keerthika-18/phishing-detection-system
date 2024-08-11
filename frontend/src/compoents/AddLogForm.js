import React, { useState } from 'react';
import axios from 'axios';
import './AddLogForm.css';

const AddLogForm = () => {
    const [type, setType] = useState('phishing_url');
    const [content, setContent] = useState('');
    const [timestamp, setTimestamp] = useState('');
    const [statusMessage, setStatusMessage] = useState('');
    const [prediction, setPrediction] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!content || !timestamp) {
            setStatusMessage('Content and Timestamp are required.');
            return;
        }

        const newLog = {
            contentType: type,
            content,
            timestamp: new Date(timestamp).toISOString()
        };

        try {
            setIsLoading(true);
            const response = await axios.post('http://127.0.0.1:5000/api/logs', newLog);
            console.log('Full Response:', response.data);

            // Assuming the API returns `is_phishing` as either 1 or 0
            const isPhishing = response.data.is_phishing === 1 ? 'not safe' : 'safe';
            
            // Determine content type for prediction
            const contentTypeLabel = type === 'phishing_email' ? 'email' : 'URL';
            
            setStatusMessage('Log added successfully.');
            setPrediction(`The ${contentTypeLabel} is ${isPhishing}.`);
        } catch (error) {
            console.error('There was an error adding the log!', error);
            setStatusMessage('There was an error adding the log.');
            setPrediction('');
        } finally {
            setIsLoading(false);
        }
        
    };

    return (
        <div className="add-log-form">
            <h2>Add New Log</h2>
            <form onSubmit={handleSubmit}>
                <label>
                    Content Type:
                    <select 
                        value={type} 
                        onChange={(e) => setType(e.target.value)} 
                        required
                    >
                        <option value="phishing_url">URL</option>
                        <option value="phishing_email">Email</option>
                    </select>
                </label>
                <br />
                <label>
                    Content:
                    <input 
                        type={type === 'phishing_email' ? 'email' : 'text'} 
                        value={content} 
                        onChange={(e) => setContent(e.target.value)} 
                        placeholder={type === 'phishing_url' ? 'Enter URL' : 'Enter Email'} 
                        required 
                    />
                </label>
                <br />
                <label>
                    Timestamp:
                    <input 
                        type="datetime-local" 
                        value={timestamp} 
                        onChange={(e) => setTimestamp(e.target.value)} 
                        required 
                    />
                </label>
                <br />
                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Submitting...' : 'Add Log'}
                </button>
                {statusMessage && <p className="status-message">{statusMessage}</p>}
                {prediction && <p className="prediction">{prediction}</p>}
            </form>
        </div>
    );
};

export default AddLogForm;
