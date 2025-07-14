from google import genai
from pydantic import BaseModel, Field
import json
from typing import List, Dict, Union

api_keys = ["AIzaSyAD7Wbxfsw8WZeJUoT6qdlGl-skxK7Afpo"]


# --- MODEL UNTUK KRITERIA ---
class KriteriaKesehatan(BaseModel):
    status_kesehatan: str  # "Ya" / "Tidak"
    penjelasan_status: str


# --- MODEL PREDIKSI KESEHATAN UTAMA ---
class PrediksiKesehatan(BaseModel):
    detail_kriteria: List[KriteriaKesehatan] = Field(..., description="List gejala dan statusnya.")
    rekomendasi_kesehatan: str = Field(..., description="Saran tindak lanjut.")


# --- FUNGSI UNTUK PREDIKSI KESEHATAN DENGAN PENCObaan BEBERAPA API KEY ---
def prediksi_kesehatan(
        api_keys: List[str],  # Daftar API key
        data_pasien: Dict[str, str],  # {"Gejala 1": "ya", "Gejala 2": "tidak", ...}
        deskripsi_kasus: str,
        instruksi_awal: str,  # Instruksi yang diletakkan di awal
        instruksi_akhir: str  # Instruksi yang diletakkan di akhir
) -> Union[Dict, PrediksiKesehatan]:
    # Iterasi melalui daftar API keys dan mencoba satu per satu
    for api_key in api_keys:
        try:
            # Inisialisasi client dengan API key
            client = genai.Client(api_key=api_key)

            # Membuat full_prompt dengan instruksi awal dan akhir
            full_prompt = f"""
            {instruksi_awal}

            1. **Deskripsi Kasus:**
            {deskripsi_kasus}

            2. **Data Jawaban Gejala:**
            {json.dumps(data_pasien, indent=2)}

            {instruksi_akhir}
            """

            # Memanggil model AI untuk menghasilkan analisis dan rekomendasi
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=full_prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": PrediksiKesehatan,
                },
            )

            # Mengembalikan hasil sebagai objek PrediksiKesehatan
            return PrediksiKesehatan.model_validate_json(response.text)

        except Exception as e:
            # Jika terjadi error, mencatat dan mencoba API key berikutnya
            print(f"Error dengan API key {api_key}: {str(e)}. Mencoba API key berikutnya.")
            continue

    # Jika semua API keys gagal
    return {"error": "Semua API keys gagal digunakan."}
if __name__ == "__main__":
    data_pasien = {
        "Sesak napas": "tidak",
        "Batuk grok-grok": "tidak",
        "Suhu >38.5°C": "ya",  # Jawaban untuk gejala yang ada
        "Diare berdarah": "tidak",
        "Warna kulit biru": "tidak"
    }

    deskripsi_kasus = "Anak berusia 4 tahun datang ke posyandu untuk pemantauan rutin."

    instruksi_awal = "Anda adalah sistem pemantauan kesehatan anak berdasarkan gejala YA/TIDAK."
    instruksi_akhir = """
    Instruksi:
    - Jika SEMUA jawaban adalah "tidak", status anak = "Normal".
    - Jika ADA SATU SAJA jawaban "ya", status anak = "Perlu diperiksa ke bidan/dokter".
    - Tampilkan status umum, analisa per gejala, dan saran umum.
    - BERIKAN SARAN UNTUK TINDAKAN AWAL
    """

    api_keys = ["AIzaSyAD7Wbxfsw8WZeJUoT6qdlGl-skxK7Afpo"]
    hasil = prediksi_kesehatan(
        api_keys=api_keys,
        data_pasien=data_pasien,
        deskripsi_kasus=deskripsi_kasus,
        instruksi_awal=instruksi_awal,
        instruksi_akhir=instruksi_akhir
    )

    # Tampilkan hasil prediksi
    print(hasil)

