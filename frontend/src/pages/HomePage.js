import React from 'react';
import LogList from '../compoents/LogList';
import AddLogForm from '../compoents/AddLogForm';
import BlockchainLog from '../compoents/BlockchainLog'

const HomePage = () => {
    return (
        <div>
          
            <AddLogForm /> 
            <LogList />
            <BlockchainLog />
        </div>
    );
};

export default HomePage;
