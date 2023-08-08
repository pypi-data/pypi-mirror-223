pub mod structures;
use pyo3::prelude::*;
use structures::logger::Logger;
use structures::logging::Log;

#[pymodule]
#[pyo3(name = "jlogr")]
#[doc = "
Module for clean and colourful logging in python
This is just how i like my logs, so there aren't formatting options or anything like that.
If you want to change the format, feel free to make a fork.
"]
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
#[doc = "
Log a info message

# Example
```python
import jlogr
jlogr.info(\"Hello, world!\")
```

# Output
```bash
2021-08-15T21:04:05.000000000+00:00 :: [INFO] :: Hello, world!
```

# Parameters
- message: The message to log
- module: The module that the message is coming from
- function: The function that the message is coming from
- class: The class that the message is coming from
"]
#[pyo3(name = "info")]
#[pyo3(text_signature = "(message, module=None, function=None, class=None)")]
pub fn info(message: &str, module: Option<&str>, function: Option<&str>, class: Option<&str>) {
    Log::new(message, "info", module, function, class).pretty_print();
}

#[pyfunction]
#[doc = "
Log a debug message
# Example
```python
import jlogr
jlogr.debug(\"Hello, world!\")
```

# Output
```bash
2021-08-15T21:04:05.000000000+00:00 :: [DEBUG] :: Hello, world!
```

# Parameters
- message: The message to log
- module: The module that the message is coming from
- function: The function that the message is coming from
- class: The class that the message is coming from
"]
#[pyo3(text_signature = "(message, module=None, function=None, class=None)")]
#[pyo3(name = "debug")]
pub fn debug(message: &str) {
    Log::new(message, "debug", None, None, None).pretty_print();
}

#[pyfunction]
#[doc = "
Log a message as a warning

# Example
```python
import jlogr
jlogr.warning(\"Hello, world!\")
```

# Output
```bash
2021-08-15T21:04:05.000000000+00:00 :: [WARNING] :: Hello, world!
```

# Parameters
- message: The message to log
- module: The module that the message is coming from
- function: The function that the message is coming from
- class: The class that the message is coming from
"]
#[pyo3(text_signature = "(message, module=None, function=None, class=None)")]
#[pyo3(name = "warning")]
pub fn warning(message: &str) {
    Log::new(message, "warning", None, None, None).pretty_print();
}

#[pyfunction]
#[doc = "
Log a message as an error

# Example
```python
import jlogr
jlogr.error(\"Hello, world!\")
```

# Output
```bash
2021-08-15T21:04:05.000000000+00:00 :: [ERROR] :: Hello, world!
```

# Parameters
- message: The message to log
- module: The module that the message is coming from
- function: The function that the message is coming from
- class: The class that the message is coming from
"]
#[pyo3(text_signature = "(message, module=None, function=None, class=None)")]
#[pyo3(name = "error")]
pub fn error(message: &str) {
    Log::new(message, "error", None, None, None).pretty_print();
}

#[pyfunction]
#[doc = "
Logs should be a list of tuples of strings, where the first string is the message and the second
string is the log level.

# Example
```python
import jlogr
logs = [(\"Hello, world!\", \"info\"), (\"Hello, world!\", \"debug\"), (\"Hello, world!\", \"warning\"), (\"Hello, world!\", \"error\")]
jlogr.parse_list_of_logs(logs)
```

# Output
```bash
2021-08-15T21:04:05.000000000+00:00 :: [INFO] :: Hello, world!
2021-08-15T21:04:05.000000000+00:00 :: [DEBUG] :: Hello, world!
2021-08-15T21:04:05.000000000+00:00 :: [WARNING] :: Hello, world!
2021-08-15T21:04:05.000000000+00:00 :: [ERROR] :: Hello, world!
```

# Parameters
- logs: A list of tuples of strings, where the tuple is structured (message, level, module, function, class)
"]
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
