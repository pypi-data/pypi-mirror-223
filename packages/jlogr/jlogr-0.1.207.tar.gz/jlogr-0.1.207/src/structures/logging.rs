use chrono::{DateTime, Local};
use pyo3::prelude::*;
use std::fmt::Display;
use std::io::Write;
use termcolor::{Color, ColorChoice, ColorSpec, StandardStream, WriteColor};

#[pyclass]
pub struct Log {
    pub created_at: DateTime<Local>,
    pub message: String,
    pub level: LogLevel,
    pub module: Option<String>,
    pub function: Option<String>,
    pub class: Option<String>,
}

#[pymethods]
impl Log {
    #[new]
    pub fn new(
        message: &str,
        level: &str,
        module: Option<&str>,
        function: Option<&str>,
        class: Option<&str>,
    ) -> Self {
        Self {
            created_at: Local::now(),
            message: message.to_string(),
            level: LogLevel::from(level),
            module: module.map(|m| m.to_string()),
            function: function.map(|f| f.to_string()),
            class: class.map(|c| c.to_string()),
        }
    }

    #[staticmethod]
    pub fn from_log_string(log_string: &str) -> Self {
        let mut log = Log::new("", "", None, None, None);
        let mut split = log_string.split(" :: ");
        log.created_at = DateTime::parse_from_rfc3339(split.next().expect("spit to have a next"))
            .expect("datetime parse to work")
            .with_timezone(&Local);
        log.level = LogLevel::from_log_string(split.next().unwrap());
        log.message = split.next().unwrap().to_string();
        log.module = split.next().map(|m| m.to_string());
        log.function = split.next().map(|f| f.to_string());
        log.class = split.next().map(|c| c.to_string());
        log
    }

    pub fn pretty_print(&self) {
        let mut stdout = StandardStream::stdout(ColorChoice::Always);
        let formatted_date = self.created_at.format("%Y-%m-%d %H:%M:%S");
        write!(stdout, "{} :: ", formatted_date).unwrap_or_else(|e| {
            eprintln!(
                "Failed to write to stdout: {}\nError: {}",
                self.message,
                e.to_string()
            );
        });
        stdout
            .set_color(ColorSpec::new().set_fg(Some(self.level.color())))
            .unwrap_or_else(|e| {
                eprintln!(
                    "Failed to set color: {:?}\nError: {}",
                    self.level.color(),
                    e.to_string()
                );
            });
        write!(stdout, "{}", self.level.prefix()).unwrap();
        stdout
            .set_color(ColorSpec::new().set_fg(Some(Color::White)))
            .unwrap_or_else(|e| {
                eprintln!(
                    "Failed to set color: {:?}\nError: {}",
                    Color::White,
                    e.to_string()
                );
            });
        writeln!(stdout, " :: {}", self.message).unwrap_or_else(|e| {
            eprintln!(
                "Failed to write to stdout: {}\nError: {}",
                self.message,
                e.to_string()
            );
        });
        stdout.reset().unwrap();
    }
}

impl Display for Log {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{} :: {} :: {}",
            self.created_at.to_rfc3339(),
            self.level.prefix(),
            self.message
        )
        .unwrap_or_else(|e| {
            eprintln!(
                "Failed to write to stdout: {}\nError: {}",
                self.message,
                e.to_string()
            );
        });
        Ok(())
    }
}

#[derive(Debug, Clone)]
#[pyclass]
pub enum LogLevel {
    Info,
    Debug,
    Warning,
    Error,
}

impl LogLevel {
    fn color(&self) -> Color {
        match self {
            LogLevel::Info => Color::Green,
            LogLevel::Debug => Color::Blue,
            LogLevel::Warning => Color::Yellow,
            LogLevel::Error => Color::Red,
        }
    }

    fn prefix(&self) -> &'static str {
        match self {
            LogLevel::Info => "[INFO]",
            LogLevel::Debug => "[DEBUG]",
            LogLevel::Warning => "[WARNING]",
            LogLevel::Error => "[ERROR]",
        }
    }
    fn from_log_string(level: &str) -> Self {
        match level {
            "[INFO]" => LogLevel::Info,
            "[DEBUG]" => LogLevel::Debug,
            "[WARNING]" => LogLevel::Warning,
            "[ERROR]" => LogLevel::Error,
            _ => {
                println!("Invalid log level {}, setting to info.", level);
                LogLevel::Info
            }
        }
    }
}

impl From<&str> for LogLevel {
    fn from(level: &str) -> Self {
        match level {
            "info" => LogLevel::Info,
            "debug" => LogLevel::Debug,
            "warning" => LogLevel::Warning,
            "error" => LogLevel::Error,
            _ => {
                println!("Invalid log level {}, setting to info.", level);
                LogLevel::Info
            }
        }
    }
}
