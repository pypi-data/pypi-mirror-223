use crate::structures::logging::Log;
use std::{fs, io::Write};

/// Handles reading and writing of logs to the file system.
/// Keeps a buffer of logs in memory, but can dump to file.
pub struct Logger {
    pub logs_path: String,
    pub logs_buffer: Vec<Log>,
}

impl Logger {
    pub fn new(logs_path: String) -> Logger {
        Logger {
            logs_path,
            logs_buffer: Vec::new(),
        }
    }

    pub fn push_log(
        &mut self,
        message: &str,
        level: &str,
        module: Option<&str>,
        function: Option<&str>,
        class: Option<&str>,
    ) {
        let log = Log::new(message, level, module, function, class);
        self.logs_buffer.push(log);
    }

    pub fn display_list_of_logs(&self) {
        for log in &self.logs_buffer {
            log.pretty_print()
        }
    }

    pub fn pull_logs_from_file(&mut self) {
        fs::read_to_string(&self.logs_path)
            .unwrap_or_else(|e| {
                eprintln!("Failed to read file: {}", e.to_string());
                return "".to_string();
            })
            .lines()
            .for_each(|line| {
                self.logs_buffer.push(Log::from_log_string(line));
            });
    }

    pub fn sort_logs_by_ctime(&mut self) {
        self.logs_buffer
            .sort_by(|a, b| a.created_at.cmp(&b.created_at));
    }

    pub fn dump_logs_to_file(&self) {
        let mut file = fs::OpenOptions::new()
            .create(true)
            .write(true)
            .append(true)
            .open(&self.logs_path)
            .expect("Open to work properly");
        for log in &self.logs_buffer {
            file.write_all(format!("{}\n", log).as_bytes())
                .unwrap_or_else(|e| {
                    eprintln!("Failed to write to file: {}", e.to_string());
                });
        }
        file.sync_all().unwrap_or_else(|e| {
            eprintln!("Failed to sync file: {}", e.to_string());
        });
    }

    pub fn clear_log_buffer(&mut self) {
        self.logs_buffer.clear();
    }

    pub fn clear_log_file(&self) {
        fs::write(&self.logs_path, "").unwrap_or_else(|e| {
            eprintln!("Failed to clear file: {}", e.to_string());
        });
    }
}
