import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const PYTHON_BACKEND_URL = 'http://127.0.0.1:5000/predict'; // Ganti sesuai IP Flask

export const POST: RequestHandler = async ({ request }) => {
	try {
		const { Lintang, Bujur } = await request.json();

		if (typeof Lintang !== 'number' || typeof Bujur !== 'number') {
			return json({ error: 'Koordinat tidak valid' }, { status: 400 });
		}

		// Kirim lon/lat ke backend Python
		const response = await fetch(PYTHON_BACKEND_URL, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ Lintang, Bujur })
		});

		if (!response.ok) {
			const errText = await response.text();
			console.error('❌ Flask error:', errText);
			return json({ error: 'Gagal memproses prediksi' }, { status: 500 });
		}

		const result = await response.json();
		return json(result);
	} catch (error) {
		console.error('❌ Server error:', error);
		return json({ error: 'Terjadi kesalahan server' }, { status: 500 });
	}
};
