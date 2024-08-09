import React, { useState } from 'react';
import axios from 'axios';

const AddLogForm = () => {
    const [type, setType] = useState('type'); // Default type
    const [content, setContent] = useState('');
    const [timestamp, setTimestamp] = useState('');
    const [statusMessage, setStatusMessage] = useState('');
    const [prediction, setPrediction] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
    
        // Basic validation
        if (!content || !timestamp) {
            setStatusMessage('Content and Timestamp are required.');
            return;
        }
    
        const newLog = {
            contentType: type,
            content,
            timestamp: new Date(timestamp).toISOString() // Convert timestamp to ISO 8601 format
        };
    
        try {
            // Declare response and await the axios call
            const response = await axios.post('http://127.0.0.1:5000/api/logs', newLog);
            console.log('Full Response:', response.data); 
            console.log('Log added:', response.data);
            setType('phishing_url'); // Reset to default
            setContent('');
            setTimestamp('');
            setStatusMessage('Log added successfully.');
    
            // Ensure correct handling of the prediction result
            const isPhishing = parseInt(response.data.is_phishing) === 1 ? 'not safe' : 'safe';
            console.log(isPhishing);
            setPrediction(`The ${type === 'phishing_email' ? 'email' : 'URL'} is ${isPhishing}.`);
        } catch (error) {
            console.error('There was an error adding the log!', error);
            setStatusMessage('There was an error adding the log.');
            setPrediction('');
        }
        // const isPhishing = parseInt(response.data.is_phishing) === 1 ? 'not safe' : 'safe';   
       
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
                <button type="submit">Add Log</button>
                {statusMessage && <p className="status-message">{statusMessage}</p>}
                {prediction && <p className="prediction">{prediction}</p>} {/* Display the prediction result */}
            </form>
        </div>
    );
};

export default AddLogForm;
