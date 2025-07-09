type BMKGWeatherResult = {
	Curah_Hujan_Harian_mm: number;
	Curah_Hujan_Kumulatif_24_Jam_mm: number;
	Curah_Hujan_Kumulatif_48_Jam_mm: number;
	Curah_Hujan_Kumulatif_72_Jam_mm: number;
	Detail_Curah_Hujan_Per_Hari: number[];
	Cuaca_Hari_Ini?: {
		weather_desc: string;
		image: string;
		local_datetime: string;
	};
};

export async function getBMKGRainStatsWithWeather(adm4Code: string): Promise<BMKGWeatherResult> {
	try {
		const res = await fetch(
			`https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=${adm4Code}`,
			{ headers: { Accept: 'application/json' }, method: 'GET' }
		);

		if (!res.ok) throw new Error(`BMKG fetch failed: ${res.statusText}`);

		const json = await res.json();
		const cuaca: any[][] | undefined = json?.data?.[0]?.cuaca;

		if (!cuaca || !Array.isArray(cuaca)) throw new Error('Invalid BMKG format');

		// Hujan 3-jam
		const hujan3jam: number[] = cuaca
			.slice(0, 3)
			.flatMap((hari) => hari.map((entry) => Number(entry?.tp ?? 0)));

		// Hujan per hari
		const hujanPerHari: number[] = [];
		for (let i = 0; i < Math.min(hujan3jam.length, 24); i += 8) {
			hujanPerHari.push(hujan3jam.slice(i, i + 8).reduce((a, b) => a + b, 0));
		}

		// Cuaca pertama (biasanya jam 03:00 waktu lokal)
		const firstWeather = cuaca?.[0]?.[0];
		let cuacaHariIni;

		if (firstWeather) {
			cuacaHariIni = {
				weather_desc: firstWeather.weather_desc,
				image: firstWeather.image,
				local_datetime: firstWeather.local_datetime
			};
		}

		return {
			Curah_Hujan_Harian_mm: hujanPerHari[0] ?? 0,
			Curah_Hujan_Kumulatif_24_Jam_mm: hujanPerHari.slice(0, 1).reduce((a, b) => a + b, 0),
			Curah_Hujan_Kumulatif_48_Jam_mm: hujanPerHari.slice(0, 2).reduce((a, b) => a + b, 0),
			Curah_Hujan_Kumulatif_72_Jam_mm: hujanPerHari.slice(0, 3).reduce((a, b) => a + b, 0),
			Detail_Curah_Hujan_Per_Hari: hujanPerHari,
			Cuaca_Hari_Ini: cuacaHariIni
		};
	} catch (err) {
		console.error('❌ BMKG API error:', err);
		return {
			Curah_Hujan_Harian_mm: 0,
			Curah_Hujan_Kumulatif_24_Jam_mm: 0,
			Curah_Hujan_Kumulatif_48_Jam_mm: 0,
			Curah_Hujan_Kumulatif_72_Jam_mm: 0,
			Detail_Curah_Hujan_Per_Hari: []
		};
	}
}
