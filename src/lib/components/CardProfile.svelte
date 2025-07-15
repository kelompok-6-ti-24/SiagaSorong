<script lang="ts">
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	let IsHovered = false;
	export let image: string = '/images/Placeholder-Person.jpg';
	export let name: string = 'John Doe';
	export let description: string = '';
	function MouseEnter() {
		IsHovered = true;
	}
	function MouseLeave() {
		IsHovered = false;
	}

	export let instagram: string = '@username';

	onMount(() => {
		if (!browser) return;
		if (image === 'Nalda') {
			image = '/images/Nalda.jpg';
		} else if (image === 'Alit') {
			image = '/images/AlitP.jpg';
		} else if (image === 'Yosua') {
			image = '/images/Yosua.jpg';
		} else if (image === 'Juan') {
			image = '/images/Juan.jpg';
		}
	});
</script>

<div
	class=" border-primary relative flex h-[20em] w-[14em] flex-col overflow-hidden rounded border-2"
>
	<div
		class="text-secondary pointer-events-none absolute top-0 left-0 h-full w-full bg-amber-50/30 bg-cover bg-center bg-no-repeat p-4 opacity-0 backdrop-blur-sm transition-all select-none"
		class:opacity-100={IsHovered}
	>
		Perkenalkan nama saya <span class="font-bold">{name}</span>,{description}
	</div>

	<div
		on:mouseenter={MouseEnter}
		on:mouseleave={MouseLeave}
		role="region"
		class:bg-alit={image === '/images/AlitP.jpg'}
		class:bg-nalda={image === '/images/Nalda.jpg'}
		class:bg-juan={image === '/images/Juan.jpg'}
		class:bg-yosua={image === '/images/Yosua.jpg'}
		class="h-full w-full bg-cover bg-center bg-no-repeat hover:bg-transparent"
	></div>
	<button
		class="font-inter bold bg-primary h-12 cursor-pointer text-white transition-all hover:scale-110"
	>
		<a
			href="https://instagram.com/{instagram.replace('@', '')}"
			target="_blank"
			rel="noopener noreferrer"
		>
			@{instagram}
		</a>
	</button>
</div>

<style lang="postcss">
	.bg-nalda {
		@apply bg-[url('/images/Nalda.jpg')];
	}
	.bg-alit {
		@apply bg-[url('/images/AlitP.jpg')];
	}
	.bg-juan {
		@apply bg-[url('/images/Juan.jpg')];
	}
	.bg-yosua {
		@apply bg-[url('/images/Yosua.jpg')];
	}
</style>
