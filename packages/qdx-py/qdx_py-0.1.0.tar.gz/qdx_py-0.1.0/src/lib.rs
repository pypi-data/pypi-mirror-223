use std::collections::HashSet;

use pyo3::{exceptions::PyRuntimeError, prelude::*};

/// Returns the json for a qdx conformer, converted from a pdb
#[pyfunction]
fn pdb_to_conformer(
    pdb_contents: String,
    keep_residues: Option<HashSet<String>>,
    skip_residues: Option<HashSet<String>>,
) -> PyResult<String> {
    serde_json::to_string(
        &qdx_common::convert::pdb::from_pdb(pdb_contents, keep_residues, skip_residues)
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))?,
    )
    .map_err(|e| PyRuntimeError::new_err(e.to_string()))
}

/// Returns the the pdb for a qdx conformer string
#[pyfunction]
fn conformer_to_pdb(conformer_contents: String) -> PyResult<String> {
    Ok(qdx_common::convert::pdb::to_pdb(
        serde_json::from_str(&conformer_contents)
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))?,
    ))
}

/// A Python module implemented in Rust.
#[pymodule]
fn qdx_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(pdb_to_conformer, m)?)?;
    m.add_function(wrap_pyfunction!(conformer_to_pdb, m)?)?;
    Ok(())
}
