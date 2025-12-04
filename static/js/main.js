/**
 * Conference Management System - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Conference Management System loaded');
    
    // Initialize event listeners
    initializeEventListeners();
});

function initializeEventListeners() {
    // Add any global event listeners here
    console.log('Event listeners initialized');
}

// Utility function to make API calls
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(endpoint, options);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}
