import React, { useState } from 'react';
import LogList from '../components/LogList';
import AddLogForm from '../components/AddLogForm';
import BlockchainLog from '../components/BlockchainLog';
import './HomePage.css'; // Import CSS for styling

const HomePage = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Function to handle loading and error states
    const handleLoading = (state) => {
        setLoading(state);
    };

    const handleError = (message) => {
        setError(message);
    };

    return (
        <div className="homepage-container">
            <h1 className="homepage-title">Phishing Detection System</h1>
            {error && <p className="error-message">{error}</p>}
    …
import React, { useState } from 'react';
import axios from 'axios';

const AddLogForm = ({ onLoading, onError }) => {
    // Existing state and functions...

    const handleSubmit = async (event) => {
        event.preventDefault();

        // Basic validation...

        onLoading(true);
        onError(null);

        try {
            const response = await axios.post('http://127.0.0.1:5000/api/logs', newLog);
            // Handle response...
            onLoading(false);
        } catch (error) {
            console.error('There was an error adding the log!', error);
            onError('There was an error adding the log.');
            onLoading(false);
        }
    };

    // Existing render method...
};

export default AddLogForm;
