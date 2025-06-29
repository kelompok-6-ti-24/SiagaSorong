<script lang="ts">
	import '../app.css';

	let { children } = $props();
</script>

<svelte:head>
	<title>Siaga Sorong - Home</title>
</svelte:head>

<header>
	<nav class="fixed top-0 right-0 left-0 z-50 p-10">
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
