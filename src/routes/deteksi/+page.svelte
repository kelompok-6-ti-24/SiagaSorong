<script lang="ts">
	import { browser } from '$app/environment';
	import MapGoogle from '$lib/components/MapGoogle.svelte';
	let selectedCoords: { lng: number; lat: number } | null = null;

	let showPopup = false;
	let loading = false;

	let textKategori = '';
	let textPrediksi = '';
	let textAlamat = 'Tidak diketahui';
	let textElevasi = '';
	let probabilitasList: string[] = [];

	const kategoriList = ['Sangat Aman', 'Aman', 'Waspada', 'Siaga', 'Bahaya'];
	function togglePopup() {
		showPopup = !showPopup;
	}

	async function handleButtonClick() {
		if (!browser) return;

		if (selectedCoords) {
			const { lng, lat } = selectedCoords;

			console.log(`Mengirim koordinat: Lng: ${lng}, Lat: ${lat}`);
			// loading = true;
			// showPopup = false; // Menutup popup jika terbuka

			// try {
			// 	const res = await fetch('/deteksi', {
			// 		method: 'POST',
			// 		headers: { 'Content-Type': 'application/json' },
			// 		body: JSON.stringify({
			// 			Lintang: lat,
			// 			Bujur: lng
			// 		})
			// 	});

			// 	if (!res.ok) {
			// 		const errText = await res.text();
			// 		console.error('Gagal:', errText);
			// 		alert('Gagal mendapatkan prediksi dari server.');
			// 		loading = false;
			// 		showPopup = false;
			// 		return;
			// 	}

			// 	const data = await res.json();
			// 	showPopup = true;
			// 	loading = false;
			// 	console.log('Data dari server:', data);
			// 	textKategori = data.label;
			// 	textAlamat = data.input.Alamat || 'Tidak diketahui';
			// 	textElevasi = data.input.Elevasi_m + 'm' || 'Tidak diketahui';
			// 	// probabilitas format = array [0: '0%', 1: '10%', ...]
			// 	probabilitasList = data.probabilitas;
			// 	probabilitasList = probabilitasList.map((p) => (p * 100).toFixed(2) + '%');
			// } catch (err) {
			// 	console.error('❌ Error:', err);
			// 	loading = false;
			// 	showPopup = false;
			// 	alert('Terjadi kesalahan saat mengirim permintaan.');
			// }
		} else {
			loading = false;
			showPopup = false;
			console.log('No coordinates selected');
			alert('Kamu belum pilih titik di peta!');
		}
	}
</script>

{#if showPopup}
	<div
		class="absolute top-0 left-0 z-50 flex h-screen w-screen items-center justify-center bg-slate-700/50"
	>
		<button
			class="absolute top-10 right-10 z-50 flex h-8 w-8 cursor-pointer items-center justify-center rounded-full border border-white bg-transparent p-2 text-xl font-bold text-red-500"
			on:click={() => {
				showPopup = false;
				textKategori = '';
				textAlamat = 'Tidak diketahui';
				textPrediksi = '';
				probabilitasList = [];
			}}
		>
			<span class="material-symbols-outlined"> close </span>
		</button>
		<div>
			{#if textKategori}
				<div class="bg-primary h-full w-full rounded-sm p-5 text-white">
					<h1 class="text-center text-xl font-bold">Hasil Deteksi</h1>
					<div>
						<p>Alamat: {textAlamat}</p>
						<p>Elevasi: {textElevasi}</p>
						<p>Kategori: <span class="font-bold">{textKategori}</span></p>
						<p>
							Probabilitas:<br />
						</p>
						<div class="ml-2">
							<span class="font-bold">
								{#each probabilitasList as prob, index}
									- {kategoriList[index]}: {prob}
									{#if index < probabilitasList.length - 1}<br />
									{/if}
								{/each}
							</span>
						</div>
					</div>
				</div>
			{:else}
				<p class="text-white">Tidak ada data yang tersedia.</p>
			{/if}
		</div>
	</div>
{/if}
<div class="p-10 pt-28">
	<div class="">
		<MapGoogle bind:longLat={selectedCoords}></MapGoogle>
	</div>

	<div class="mt-5 flex justify-end gap-5">
		<button
			on:click={handleButtonClick}
			type="button"
			disabled={!selectedCoords || loading}
			class:disabled={loading || !selectedCoords}
			class=" bg-primary font-inter mt-4 h-16 w-80 cursor-pointer rounded-md p-2 text-3xl text-white"
		>
			Cek Disini
		</button>
	</div>
</div>

<style lang="postcss">
	.disabled {
		@apply cursor-not-allowed opacity-60;
	}
</style>
