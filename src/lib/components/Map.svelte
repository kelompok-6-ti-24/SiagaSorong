<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import maplibregl from 'maplibre-gl';
	import 'maplibre-gl/dist/maplibre-gl.css';
	import { PUBLIC_VITE_MAPTILER_API_KEY } from '$env/static/public';

	let map: maplibregl.Map;
	let mapContainer: HTMLDivElement;
	let currentMarker: maplibregl.Marker | null = null;
	const sorongBounds: maplibregl.LngLatBoundsLike = [
		[131.0, -1.0],
		[131.5, -0.5]
	];

	export let selectedCoords: { lng: number; lat: number } | null = null;

	function getCurrentLocation() {
		if (map) {
			navigator.geolocation.getCurrentPosition(
				(position) => {
					const { latitude, longitude } = position.coords;
					map.flyTo({
						center: [longitude, latitude],
						zoom: 15,
						duration: 1000
					});
					if (currentMarker) {
						currentMarker?.remove();
					}
					selectedCoords = { lng: longitude, lat: latitude };
					currentMarker = new maplibregl.Marker({ color: '#1B263B' })
						.setLngLat([longitude, latitude])
						.addTo(map);
				},
				(error) => {
					console.error('Error getting current location:', error);
				}
			);
		} else {
			console.error('Map is not initialized');
		}
	}

	onMount(() => {
		const initialState = { lng: 131.30522577272714, lat: -0.885490120264698, zoom: 14 };

		map = new maplibregl.Map({
			container: mapContainer,
			style: `https://api.maptiler.com/maps/streets-v2/style.json?key=${PUBLIC_VITE_MAPTILER_API_KEY}`,
			center: [initialState.lng, initialState.lat],
			zoom: initialState.zoom,
			maxBounds: sorongBounds
		});
		map.addControl(new maplibregl.NavigationControl(), 'top-right');
		map.on('click', (e) => {
			const { lng, lat } = e.lngLat;
			console.log(`Clicked at: ${lng}, ${lat}`);
			if (currentMarker) {
				currentMarker?.remove();
			}

			selectedCoords = { lng, lat };
			currentMarker = new maplibregl.Marker({ color: '#1B263B' }) // Bisa custom icon juga kalau mau
				.setLngLat([lng, lat])
				.addTo(map);
		});
	});

	onDestroy(async () => {
		try {
			map.remove();
		} catch (error) {
			console.log('Error: ', error);
		}
	});
</script>

<div class="map-wrap border-primary overflow-hidden rounded border">
	<button
		class="absolute bottom-2 left-2 z-10 rounded bg-white p-2 shadow transition-colors hover:bg-gray-100"
		on:click={getCurrentLocation}
	>
		Lokasi Saya
	</button>
	<div class="map" bind:this={mapContainer}></div>
</div>

<style>
	.map-wrap {
		position: relative;
		width: 100%;
		height: calc(100vh - 300px);
	}

	.map {
		position: absolute;
		width: 100%;
		height: 100%;
	}
</style>
