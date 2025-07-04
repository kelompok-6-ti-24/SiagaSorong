<script lang="ts">
</script>

<div class="flex h-screen w-screen flex-row">
	<div class="section-1 flex flex-col justify-center gap-20 pt-20 pr-20 pl-10">
		<div class="font-montserrat">
			<h1 class="text-secondary text-[64px] leading-[64px]">
				<span class="text-primary font-bold">Siaga </span><br /> Sorong
			</h1>
			<div class="mb-10">
				<p class="font-inter mt-6 text-justify text-2xl">
					<span class="text-primary pr-7 font-bold">Siaga Sorong</span>
					adalah platform interaktif yang dirancang khusus untuk membantu warga dan pemerintah Kota Sorong
					untuk mendeteksi ancaman banjir
				</p>
			</div>
			<button
				type="button"
				class=" bg-primary font-inter mt-4 h-14 w-64 cursor-pointer rounded-md p-2 text-3xl text-white"
			>
				<a href="/deteksi"> Cek Disini </a>
			</button>
		</div>
		<div class="font-inter text-primary fixed bottom-10 left-10 text-2xl font-bold">
			<button class="underline">
				<a href="/tentang">Tentang Kami</a>
			</button>
		</div>
	</div>
	<div class="section-2 bg-primary p-16">
		<div class="flex h-full w-full items-center justify-center rounded bg-white"></div>
	</div>
</div>

<style lang="postcss">
	.section-1,
	.section-2 {
		@apply h-screen w-[50vw];
	}
</style>
