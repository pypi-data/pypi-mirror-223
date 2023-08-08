pub mod structures;
use pyo3::prelude::*;
use structures::logger::Logger;
use structures::logging::Log;

#[pymodule]
#[pyo3(name = "jlogr")]
pub fn jlogr(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(info, m)?)?;
    m.add_function(wrap_pyfunction!(debug, m)?)?;
    m.add_function(wrap_pyfunction!(warning, m)?)?;
    m.add_function(wrap_pyfunction!(error, m)?)?;
    m.add_function(wrap_pyfunction!(parse_list_of_logs, m)?)?;
    m.add_class::<Logger>()?;
    m.add_class::<Log>()?;
    Ok(())
}

#[pyfunction]
#[pyo3(name = "info")]
#[pyo3(text_signature = "(message, module=None, function=None, class=None)")]
pub fn info(message: &str, module: Option<&str>, function: Option<&str>, class: Option<&str>) {
    Log::new(message, "info", module, function, class).pretty_print();
}

#[pyfunction]
#[pyo3(text_signature = "(message, module=None, function=None, class=None)")]
#[pyo3(name = "debug")]
pub fn debug(message: &str) {
    Log::new(message, "debug", None, None, None).pretty_print();
}

#[pyfunction]
#[pyo3(text_signature = "(message, module=None, function=None, class=None)")]
#[pyo3(name = "warning")]
pub fn warning(message: &str) {
    Log::new(message, "warning", None, None, None).pretty_print();
}

#[pyfunction]
#[pyo3(text_signature = "(message, module=None, function=None, class=None)")]
#[pyo3(name = "error")]
pub fn error(message: &str) {
    Log::new(message, "error", None, None, None).pretty_print();
}

#[pyfunction]
#[pyo3(text_signature = "(logs)")]
#[pyo3(name = "parse_list_of_logs")]
pub fn parse_list_of_logs(
    logs: Vec<(
        String,
        String,
        Option<String>,
        Option<String>,
        Option<String>,
    )>,
) {
    for log in logs {
        let (message, level, module, function, class) = log;
        let log = Log::new(
            message.as_str(),
            level.as_str(),
            module.as_deref(),
            function.as_deref(),
            class.as_deref(),
        );
        log.pretty_print();
    }
}
