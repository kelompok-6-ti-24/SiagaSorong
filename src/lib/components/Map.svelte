<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import maplibregl from 'maplibre-gl';
	import 'maplibre-gl/dist/maplibre-gl.css';
	import { PUBLIC_VITE_MAPTILER_API_KEY } from '$env/static/public';

	let map: maplibregl.Map;
	let mapContainer: HTMLDivElement;
	const sorongBounds: maplibregl.LngLatBoundsLike = [
		[131.0, -1.0],
		[131.5, -0.5]
	];

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
			console.log(e.lngLat);
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
