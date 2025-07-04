<script lang="ts">
	import Map from '$lib/components/Map.svelte';
	let selectedCoords: { lng: number; lat: number } | null = null;

	let showPopup = false;

	let textKategori = '';
	let textPrediksi = '';
	let textProbabilitas = '';
	function togglePopup() {
		showPopup = !showPopup;
	}

	async function handleButtonClick() {
		if (selectedCoords) {
			const { lng, lat } = selectedCoords;

			console.log(`Mengirim koordinat: Lng: ${lng}, Lat: ${lat}`);

			try {
				const res = await fetch('/deteksi', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({
						Lintang: lat,
						Bujur: lng
					})
				});

				if (!res.ok) {
					const errText = await res.text();
					console.error('Gagal:', errText);
					alert('Gagal mendapatkan prediksi dari server.');
					return;
				}

				const data = await res.json();
				showPopup = true;
				console.log('Data dari server:', data);
				textKategori = data.label;
			} catch (err) {
				console.error('❌ Error:', err);
				alert('Terjadi kesalahan saat mengirim permintaan.');
			}
		} else {
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
			class="text-primary absolute top-10 right-10 z-50 flex h-8 w-8 items-center justify-center rounded-full bg-white p-2 text-2xl font-bold"
			on:click={() => {
				showPopup = false;
				textKategori = '';
				textPrediksi = '';
				textProbabilitas = '';
			}}>X</button
		>
		<div>
			{#if textKategori}
				<div class="rounded-lg bg-white p-5 shadow-lg">
					<h2 class="text-primary text-3xl font-bold">Hasil Deteksi</h2>
					<p class="mt-4 text-xl">Kategori: <span class="font-bold">{textKategori}</span></p>
					<!-- Tambahkan informasi lain jika perlu -->
				</div>
			{:else}
				<p class="text-white">Tidak ada data yang tersedia.</p>
			{/if}
		</div>
	</div>
{/if}
<div class="p-10 pt-28">
	<div class="">
		<Map bind:selectedCoords></Map>
	</div>

	<div class="mt-5 flex justify-end gap-5">
		<button
			on:click={handleButtonClick}
			type="button"
			class=" bg-primary font-inter mt-4 h-16 w-80 cursor-pointer rounded-md p-2 text-3xl text-white"
		>
			Cek Disini
		</button>
	</div>
</div>

<style lang="postcss">
</style>
