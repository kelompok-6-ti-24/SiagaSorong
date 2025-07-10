<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { PUBLIC_GOOGLE_MAPS_API_KEY } from '$env/static/public';
	import { getBMKGRainStatsWithWeather } from '$lib/library/weather';

	let mapDiv: HTMLDivElement;
	let inputRef: HTMLInputElement;

	export let longLat: { lng: number; lat: number } | null = null;

	let Cuaca: Awaited<ReturnType<typeof getBMKGRainStatsWithWeather>>['Cuaca_Hari_Ini'];

	onMount(async () => {
		if (!browser) return;

		const { Cuaca_Hari_Ini } = await getBMKGRainStatsWithWeather('96.71.01.1001');
		Cuaca = Cuaca_Hari_Ini;

		const module = await import('@googlemaps/js-api-loader');

		const loader = new module.Loader({
			apiKey: PUBLIC_GOOGLE_MAPS_API_KEY,
			libraries: ['places']
		});

		await loader.load();

		const sorongBounds = new window.google.maps.LatLngBounds(
			{ lat: -1.1, lng: 131.2 }, // Southwest
			{ lat: -0.7, lng: 131.5 } // Northeast
		);

		const map = new window.google.maps.Map(mapDiv, {
			center: { lat: -0.89, lng: 131.3 },
			zoom: 13,
			restriction: {
				latLngBounds: sorongBounds,
				strictBounds: true // Kalau `true`, map bener² gak bisa keluar
			},
			mapTypeControl: false,
			cameraControl: false,
			streetViewControl: false
		});

		const autocomplete = new window.google.maps.places.Autocomplete(inputRef);
		autocomplete.bindTo('bounds', map);

		const marker = new window.google.maps.Marker({
			map,
			draggable: true
		});

		autocomplete.addListener('place_changed', () => {
			const place = autocomplete.getPlace();
			if (!place.geometry || !place.geometry.location) return;

			const loc = place.geometry.location;
			map.setCenter(loc);
			map.setZoom(15);
			marker.setPosition(loc);
			longLat = {
				lat: loc.lat(),
				lng: loc.lng()
			};
		});

		map.addListener('click', (e: any) => {
			const lngLat = e.latLng;
			marker.setPosition(e.latLng);
			longLat = {
				lat: lngLat.lat(),
				lng: lngLat.lng()
			};
		});
	});
</script>

<div class="border-primary h-[63vh] w-full overflow-hidden rounded border-2 drop-shadow-2xl">
	{#if Cuaca && Cuaca?.image}
		<div class="absolute top-2 left-4 z-10 flex flex-col items-center justify-center">
			<img src={Cuaca.image} class="w-14 drop-shadow-2xl" alt={Cuaca?.weather_desc} />
			<p class="font-montserrat text-primary text-shadow-xs">{Cuaca.weather_desc}</p>
		</div>
	{/if}
	<input
		bind:this={inputRef}
		class="border-secondary absolute top-2 left-1/2 z-10 mb-4 w-full max-w-[200px] -translate-x-1/2 transform rounded-4xl border bg-white p-2 px-5 opacity-80 outline-0 transition-all duration-200 ease-in-out hover:max-w-md hover:opacity-100 focus:max-w-md active:max-w-md"
		placeholder="Cari alamat..."
	/>
	<div bind:this={mapDiv} class="h-full w-full"></div>
</div>

<style>
</style>
