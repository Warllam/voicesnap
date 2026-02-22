// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Deserialize, Serialize};
use std::sync::Mutex;
use tauri::{Emitter, Manager};

#[cfg(not(any(target_os = "android", target_os = "ios")))]
use tauri_plugin_global_shortcut::GlobalShortcutExt;

// Python backend URL
const PYTHON_BACKEND: &str = "http://localhost:8765";

// App state
#[allow(dead_code)]
struct AppState {
    python_server_running: Mutex<bool>,
}

#[derive(Debug, Serialize, Deserialize)]
struct ApiResponse<T> {
    success: bool,
    data: Option<T>,
    error: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct TranscriptionResult {
    text: String,
    language: Option<String>,
    duration: f64,
    audio_file: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct DeviceInfo {
    index: i32,
    name: String,
    channels: i32,
    sample_rate: f64,
}

// Tauri Commands

#[tauri::command]
async fn start_python_server() -> Result<bool, String> {
    // This will be called on app startup to launch Python server
    println!("Starting Python backend server...");
    
    // The Python server will be launched as a separate process
    // In production, we'll bundle Python with the app
    
    Ok(true)
}

#[tauri::command]
async fn check_server_health() -> Result<bool, String> {
    let client = reqwest::Client::new();
    
    match client.get(format!("{}/health", PYTHON_BACKEND))
        .timeout(std::time::Duration::from_secs(2))
        .send()
        .await {
        Ok(response) => Ok(response.status().is_success()),
        Err(_) => Ok(false),
    }
}

#[tauri::command]
async fn start_recording() -> Result<bool, String> {
    let client = reqwest::Client::new();
    
    match client.post(format!("{}/api/recording/start", PYTHON_BACKEND))
        .send()
        .await {
        Ok(response) => {
            let result: ApiResponse<bool> = response.json().await
                .map_err(|e| format!("Failed to parse response: {}", e))?;
            
            if result.success {
                Ok(result.data.unwrap_or(false))
            } else {
                Err(result.error.unwrap_or("Unknown error".to_string()))
            }
        },
        Err(e) => Err(format!("Failed to start recording: {}", e)),
    }
}

#[tauri::command]
async fn stop_recording() -> Result<TranscriptionResult, String> {
    let client = reqwest::Client::new();
    
    match client.post(format!("{}/api/recording/stop", PYTHON_BACKEND))
        .send()
        .await {
        Ok(response) => {
            let result: ApiResponse<TranscriptionResult> = response.json().await
                .map_err(|e| format!("Failed to parse response: {}", e))?;
            
            if result.success {
                result.data.ok_or("No transcription data".to_string())
            } else {
                Err(result.error.unwrap_or("Transcription failed".to_string()))
            }
        },
        Err(e) => Err(format!("Failed to stop recording: {}", e)),
    }
}

#[tauri::command]
async fn get_audio_devices() -> Result<Vec<DeviceInfo>, String> {
    let client = reqwest::Client::new();
    
    match client.get(format!("{}/api/devices", PYTHON_BACKEND))
        .send()
        .await {
        Ok(response) => {
            let result: ApiResponse<Vec<DeviceInfo>> = response.json().await
                .map_err(|e| format!("Failed to parse response: {}", e))?;
            
            if result.success {
                Ok(result.data.unwrap_or_default())
            } else {
                Err(result.error.unwrap_or("Failed to get devices".to_string()))
            }
        },
        Err(e) => Err(format!("Failed to get devices: {}", e)),
    }
}

#[tauri::command]
async fn get_transcriptions(limit: Option<i32>) -> Result<serde_json::Value, String> {
    let client = reqwest::Client::new();
    let limit_param = limit.unwrap_or(100);
    
    match client.get(format!("{}/api/transcriptions?limit={}", PYTHON_BACKEND, limit_param))
        .send()
        .await {
        Ok(response) => {
            let result: ApiResponse<serde_json::Value> = response.json().await
                .map_err(|e| format!("Failed to parse response: {}", e))?;
            
            if result.success {
                Ok(result.data.unwrap_or(serde_json::json!([])))
            } else {
                Err(result.error.unwrap_or("Failed to get transcriptions".to_string()))
            }
        },
        Err(e) => Err(format!("Failed to get transcriptions: {}", e)),
    }
}

#[tauri::command]
async fn delete_transcription(id: i32) -> Result<bool, String> {
    let client = reqwest::Client::new();
    
    match client.delete(format!("{}/api/transcriptions/{}", PYTHON_BACKEND, id))
        .send()
        .await {
        Ok(response) => {
            let result: ApiResponse<bool> = response.json().await
                .map_err(|e| format!("Failed to parse response: {}", e))?;
            
            if result.success {
                Ok(result.data.unwrap_or(false))
            } else {
                Err(result.error.unwrap_or("Failed to delete".to_string()))
            }
        },
        Err(e) => Err(format!("Failed to delete transcription: {}", e)),
    }
}

#[tauri::command]
async fn get_config() -> Result<serde_json::Value, String> {
    let client = reqwest::Client::new();
    
    match client.get(format!("{}/api/config", PYTHON_BACKEND))
        .send()
        .await {
        Ok(response) => {
            let result: ApiResponse<serde_json::Value> = response.json().await
                .map_err(|e| format!("Failed to parse response: {}", e))?;
            
            if result.success {
                Ok(result.data.unwrap_or(serde_json::json!({})))
            } else {
                Err(result.error.unwrap_or("Failed to get config".to_string()))
            }
        },
        Err(e) => Err(format!("Failed to get config: {}", e)),
    }
}

#[tauri::command]
async fn update_config(config: serde_json::Value) -> Result<bool, String> {
    let client = reqwest::Client::new();
    
    match client.post(format!("{}/api/config", PYTHON_BACKEND))
        .json(&config)
        .send()
        .await {
        Ok(response) => {
            let result: ApiResponse<bool> = response.json().await
                .map_err(|e| format!("Failed to parse response: {}", e))?;
            
            if result.success {
                Ok(result.data.unwrap_or(false))
            } else {
                Err(result.error.unwrap_or("Failed to update config".to_string()))
            }
        },
        Err(e) => Err(format!("Failed to update config: {}", e)),
    }
}

#[tauri::command]
async fn paste_text(text: String) -> Result<bool, String> {
    let client = reqwest::Client::new();
    
    match client.post(format!("{}/api/paste", PYTHON_BACKEND))
        .json(&serde_json::json!({"text": text}))
        .send()
        .await {
        Ok(response) => {
            let result: ApiResponse<bool> = response.json().await
                .map_err(|e| format!("Failed to parse response: {}", e))?;
            
            if result.success {
                Ok(result.data.unwrap_or(false))
            } else {
                Err(result.error.unwrap_or("Failed to paste".to_string()))
            }
        },
        Err(e) => Err(format!("Failed to paste text: {}", e)),
    }
}

fn main() {
    tauri::Builder::default()
        .manage(AppState {
            python_server_running: Mutex::new(false),
        })
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            #[cfg(not(any(target_os = "android", target_os = "ios")))]
            {
                use tauri_plugin_global_shortcut::ShortcutState;
                
                let app_handle = app.handle().clone();
                
                app.handle().plugin(
                    tauri_plugin_global_shortcut::Builder::new()
                        .with_handler(move |_app, shortcut, event| {
                            if event.state == ShortcutState::Pressed {
                                println!("Global hotkey pressed: {:?}", shortcut);
                                
                                // Emit to all webview windows
                                println!("Emitting hotkey-pressed event to frontend...");
                                app_handle.webview_windows().values().for_each(|window| {
                                    if let Err(e) = window.emit("hotkey-pressed", ()) {
                                        eprintln!("Failed to emit to window: {}", e);
                                    } else {
                                        println!("Event emitted to window successfully!");
                                    }
                                });
                            }
                        })
                        .build(),
                )?;
                
                // Register Ctrl+Space
                app.global_shortcut().register("CommandOrControl+Space")?;
            }
            
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            start_python_server,
            check_server_health,
            start_recording,
            stop_recording,
            get_audio_devices,
            get_transcriptions,
            delete_transcription,
            get_config,
            update_config,
            paste_text,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
