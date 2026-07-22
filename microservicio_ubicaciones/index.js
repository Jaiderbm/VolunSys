const express = require('express');
const cors = require('cors');
require('dotenv').config();

const paisRoutes = require('./routes/pais');
const ciudadRoutes = require('./routes/ciudad');
const ubicacionRoutes = require('./routes/ubicacion');

const app = express();
app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
    res.send({ message: "Ubicaciones Microservice API is running" });
});

app.use('/api/pais', paisRoutes);
app.use('/api/ciudad', ciudadRoutes);
app.use('/api/ubicacion', ubicacionRoutes);

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`[Express] Ubicaciones service running on port ${PORT}`);
});
