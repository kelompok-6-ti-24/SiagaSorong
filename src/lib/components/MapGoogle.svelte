<script lang="ts">
	import { onMount } from 'svelte';
	import { Loader } from '@googlemaps/js-api-loader';

	import { PUBLIC_GOOGLE_MAPS_API_KEY as apiKey } from '$env/static/public';

	let mapDiv: HTMLDivElement;
	let inputRef: HTMLInputElement;

	onMount(async () => {
		const loader = new Loader({
			apiKey,
			libraries: ['places']
		});

		await loader.load();

		const map = new google.maps.Map(mapDiv, {
			center: { lat: -0.89, lng: 131.3 },
			zoom: 13
		});

		const autocomplete = new google.maps.places.Autocomplete(inputRef);
		autocomplete.bindTo('bounds', map);

		autocomplete.addListener('place_changed', () => {
			const place = autocomplete.getPlace();
			if (!place.geometry || !place.geometry.location) {
				alert('Alamat tidak valid.');
				return;
			}
			const location = place.geometry.location;
			map.setCenter(location);
			map.setZoom(15);

			new google.maps.Marker({
				position: location,
				map
			});

			console.log('📍 Lokasi dipilih:', {
				lat: location.lat(),
				lng: location.lng()
			});
		});
	});
</script>

<input bind:this={inputRef} placeholder="Cari alamat..." class="input" />
<div bind:this={mapDiv} id="map" />

<style>
	#map {
		width: 100%;
		height: 400px;
		margin-top: 0.5rem;
	}
</style>
