const { checkFact } = require('../utils/factCheckAPI');

exports.analyzeNews = async (req, res) => {
    try {
        const { text } = req.body;
        if (!text) return res.status(400).json({ message: 'Text is required' });

        const result = await checkFact(text);
        res.json({ credibility: result });
    } catch (error) {
        res.status(500).json({ error: 'Error analyzing news' });
    }
};
