<script lang="ts">
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import '../app.css';

	// import current page
	onMount(() => {});

	let { children } = $props();
</script>

<svelte:head>
	<title>Siaga Sorong - Home</title>
</svelte:head>

<header>
	<nav
		class:bg-transparent={page.url.pathname === '/'}
		class="bg-surface fixed top-0 right-0 left-0 z-50 px-10 pt-10"
	>
		<button class="font-montserrat text-3xl">
			<a href="/" class="text-secondary"><span class="text-primary font-bold">Siaga</span> Sorong</a
			>
		</button>
	</nav>
</header>
<main class="">
	{@render children()}
</main>

<style lang="postcss">
</style>
