const axios = require('axios');

exports.checkFact = async (query) => {
    try {
        const response = await axios.get("https://factchecktools.googleapis.com/v1alpha1/claims:search", {

            params: { query, key: process.env.FACTCHECK_API_KEY },
        });

        return response.data || { message: 'No fact-check found' };
    } catch (error) {
        return { error: 'API request failed' };
    }
};
