from flask import Flask, request, jsonify
import joblib
import pandas as pd
import requests
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from dotenv import load_dotenv

load_dotenv()
import time
import os
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
app = Flask(__name__)

# Load model
model_path = "model/mlp_banjir_model.joblib"
loaded_model = joblib.load(model_path)

numeric_features = [
    "Curah_Hujan_Harian_mm",
    "Curah_Hujan_Kumulatif_24_Jam_mm",
    "Curah_Hujan_Kumulatif_48_Jam_mm",
    "Curah_Hujan_Kumulatif_72_Jam_mm",
    "Lintang",
    "Bujur",
    "Elevasi_m",
]
categorical_features = ["Alamat"]

label_mapping = {0: "Sangat Aman", 1: "Aman", 2: "Waspada", 3: "Siaga", 4: "Bahaya"}

def get_elevation(lat, lon, retries=3, delay=2):
    url = (
        f"https://maps.googleapis.com/maps/api/elevation/json"
        f"?locations={lat},{lon}&key={GOOGLE_API_KEY}"
    )
    for i in range(retries):
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            results = res.json().get("results", [])
            if results:
                elevation = results[0]["elevation"]
                return round(elevation)  # ⬅️ dibulatkan ke integer
            else:
                raise Exception("Hasil elevasi kosong dari API Google")
        except Exception as e:
            print(f"❌ Gagal ambil elevasi (percobaan {i+1}): {e}")
            time.sleep(delay)
    raise Exception("Gagal mengambil data elevasi setelah beberapa kali percobaan.")

def get_address_from_coords(lat, lon, retries=3, delay=2):
    def _clean_address(raw_address: str) -> str:
        parts = raw_address.split(", ")
        if "+" in parts[0]:  # buang plus code (misal: "4893+C43")
            parts = parts[1:]
        return ", ".join(parts[:4])  # ambil maksimal 4 bagian penting

    url = (
        f"https://maps.googleapis.com/maps/api/geocode/json"
        f"?latlng={lat},{lon}&key={GOOGLE_API_KEY}&language=id"
    )

    for i in range(retries):
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            data = res.json()

            status = data.get("status")
            if status != "OK":
                raise Exception(f"Google API status: {status}")

            results = data.get("results", [])
            if not results:
                raise Exception("Hasil kosong dari Google Geocoding")

            raw_address = results[0].get("formatted_address", "")
            return _clean_address(raw_address)

        except Exception as e:
            print(f"❌ Gagal ambil alamat (percobaan {i+1}): {e}")
            time.sleep(delay)

    return "Alamat tidak ditemukan"


@app.route("/predict", methods=["POST"])
def predict_from_coords():
    print("Received request for prediction")
    try:
        req = request.get_json()
        lat = req.get("Lintang")
        lon = req.get("Bujur")
        if lat is None or lon is None:
            return jsonify({"error": "Missing Lintang or Bujur"}), 400

        # Ambil elevasi
        elev = get_elevation(lat, lon)

        # Ambil curah hujan dari BMKG
        ADM4_CODE = "96.71.01.1001"
        bmkg_headers = {
            "User-Agent": "SiagaSorong/1.0 (https://github.com/AlitPurnama/SiagaSorong)"
        }
        bmkg_res = requests.get(
            f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={ADM4_CODE}",
            headers=bmkg_headers,
            timeout=10,
        )

        bmkg_data = bmkg_res.json()["data"][0]["cuaca"]
        

        hujan_3jam = []
        for hari in bmkg_data[:3]:
            hujan_3jam += [entry.get("tp", 0.0) for entry in hari]

        hujan_per_hari = [
            sum(hujan_3jam[i : i + 8]) for i in range(0, min(len(hujan_3jam), 24), 8)
        ]

        alamat = get_address_from_coords(lat, lon)
        # Final data buat prediksi
        data_input = {
            "Alamat": alamat,
            "Curah_Hujan_Harian_mm": hujan_per_hari[0] if hujan_per_hari else 0.0,
            "Curah_Hujan_Kumulatif_24_Jam_mm": sum(hujan_per_hari[:1]),
            "Curah_Hujan_Kumulatif_48_Jam_mm": sum(hujan_per_hari[:2]),
            "Curah_Hujan_Kumulatif_72_Jam_mm": sum(hujan_per_hari[:3]),
            "Lintang": lat,
            "Bujur": lon,
            "Elevasi_m": elev,
        }

        # Prediksi model
        input_df = pd.DataFrame([data_input])
        transformed_input = loaded_model.named_steps["preprocessor"].transform(input_df)
        pred_class = loaded_model.named_steps["classifier"].predict(transformed_input)[
            0
        ]
        pred_proba = (
            loaded_model.named_steps["classifier"]
            .predict_proba(transformed_input)[0]
            .tolist()
        )

        return jsonify(
            {
                "input": data_input,
                "kategori": int(pred_class),
                "label": label_mapping.get(int(pred_class), "Tidak diketahui"),
                "probabilitas": pred_proba,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
