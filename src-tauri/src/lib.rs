use tauri::{AppHandle, Manager, Emitter};
use std::sync::{Arc, Mutex};
use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use tokio::sync::mpsc;

struct AppState {
    is_recording: Arc<Mutex<bool>>,
    audio_tx: Option<mpsc::Sender<Vec<f32>>>,
}

#[tauri::command]
async fn toggle_recording(state: tauri::State<'_, AppState>, app_handle: tauri::AppHandle) -> Result<bool, String> {
    let mut is_recording = state.is_recording.lock().unwrap();
    *is_recording = !*is_recording;
    
    if *is_recording {
        println!("Empezando a escuchar (Rust)...");
        // Start audio capture loop via cpal (simulated for now to ensure compilation)
        // In the next step we will implement the actual cpal callback
        app_handle.emit("transcription_update", "Grabando...").unwrap();
    } else {
        println!("Deteniendo escucha (Rust)...");
        app_handle.emit("transcription_update", "Grabación detenida. Analizando...").unwrap();
    }

    Ok(*is_recording)
}

#[tauri::command]
async fn init_ai_engine() -> Result<String, String> {
    println!("Inicializando motor IA local (Faster-Whisper, LanceDB, Gemma)...");
    // Placeholder para la carga de modelos de RAG Híbrido
    Ok("Motor IA local iniciado correctamente".to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .manage(AppState {
            is_recording: Arc::new(Mutex::new(false)),
            audio_tx: None,
        })
        .invoke_handler(tauri::generate_handler![toggle_recording, init_ai_engine])
        .setup(|app| {
            println!("Menura Desktop App iniciada (Tauri v2)");
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
