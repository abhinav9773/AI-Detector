require('dotenv').config();
const express = require('express');
const cors = require('cors');
const newsRoutes = require('./routes/newsRoutes');

const app = express();


app.use(express.json());
app.use(cors());


app.use('/api/news', newsRoutes);


const path = require('path');
app.use(express.static(path.join(__dirname, '../TruthLens-Frontend')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../TruthLens-Frontend/index.html'));
});


app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ success: false, message: "Internal Server Error" });
});


const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));
