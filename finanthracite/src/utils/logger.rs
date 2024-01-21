use log::{Record, Level, Metadata};
use std::fs::OpenOptions;
use std::io::{Write, Result};

pub struct FileLogger {
    file: std::fs::File,
}

impl FileLogger {
    pub fn new(log_file_path: &str) -> Result<Self> {
        let file = OpenOptions::new()
            .create(true)
            .write(true)
            .append(true)
            .open(log_file_path)?;

        Ok(FileLogger { file })
    }
}

impl log::Log for FileLogger {
    fn enabled(&self, metadata: &Metadata) -> bool {
        metadata.level() <= Level::Info // Adjust the log level as needed
    }

    fn log(&self, record: &Record) {
        if self.enabled(record.metadata()) {
            if let Err(err) = writeln!(self.file, "{} - {}: {}", record.level(), record.target(), record.args()) {
                eprintln!("Failed to write to log file: {}", err);
            }
        }
    }

    fn flush(&self) {
        if let Err(err) = self.file.flush() {
            eprintln!("Failed to flush log file: {}", err);
        }
    }
}
