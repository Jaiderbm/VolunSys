const express = require('express');
const router = express.Router();
const db = require('../db');

// GET all
router.get('/', async (req, res) => {
  try {
    const { rows } = await db.query('SELECT * FROM pais ORDER BY id ASC');
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET by id
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { rows } = await db.query('SELECT * FROM pais WHERE id = $1', [id]);
    if (rows.length === 0) return res.status(404).json({ message: "No encontrado" });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST
router.post('/', async (req, res) => {
  try {
    const { nombre, codigo_iso, estado } = req.body;
    const activo = estado !== undefined ? estado : true;
    const { rows } = await db.query(
      'INSERT INTO pais (nombre, codigo_iso, estado) VALUES ($1, $2, $3) RETURNING *',
      [nombre, codigo_iso, activo]
    );
    res.status(201).json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// PUT
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { nombre, codigo_iso, estado } = req.body;
    const { rows } = await db.query(
      'UPDATE pais SET nombre = $1, codigo_iso = $2, estado = $3 WHERE id = $4 RETURNING *',
      [nombre, codigo_iso, estado, id]
    );
    if (rows.length === 0) return res.status(404).json({ message: "No encontrado" });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// DELETE
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { rows } = await db.query('DELETE FROM pais WHERE id = $1 RETURNING *', [id]);
    if (rows.length === 0) return res.status(404).json({ message: "No encontrado" });
    res.json({ success: true, message: "Eliminado correctamente" });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
