<script>
	import CardProfile from '$lib/components/CardProfile.svelte';
</script>

<div class="overflow-x flex h-screen w-screen flex-col items-center justify-center gap-2 px-10">
	<!-- <section>
		<h2 class="font-inter text-primary text-center text-4xl font-bold uppercase">tentang kami</h2>
		<p class="font-inter mt-6 px-42 text-justify text-xl">
			<span class="font-montserrat text-primary font-bold"
				>Siaga <span class="text-secondary font-normal">Sorong</span></span
			> adalah platform interaktif yang dirancang khusus untuk membantu warga dan pemerintah Kota Sorong
			untuk membantu mendeteksi daerah rawan banjir. Platform ini menggabungkan teknologi pemetaan dan
			data cuaca untuk memberikan informasi yang cukup akurat dan real-time tentang potensi banjir di
			wilayah Sorong. Dengan Siaga Sorong, warga dapat dengan mudah mendapatkan informasi tentang kondisi
			cuaca, tingkat curah hujan, dan potensi banjir di daerah mereka.
		</p>
	</section> -->
	<section id="team" class="mt-20">
		<h2 class="font-inter text-primary text-center text-4xl font-bold uppercase">team</h2>
		<div class="mt-12 flex w-full items-center justify-center gap-5">
			<CardProfile
				name="Yullia Renalda"
				image="Nalda"
				instagram="naldaftngl16"
				description=" saya sebagai ketua kelompok dan yang membuat laporan"
			/>
			<CardProfile
				name="Alit Purnama"
				image="Alit"
				instagram="alit_.p"
				description=" saya sebagai anggota dan developer utama untuk implementasi dan website SiagaSorong"
			/>
			<CardProfile
				name="Yosua Hode"
				image="Yosua"
				instagram="yosua_hd"
				description=" saya sebagai anggota kelompok dan yang membuat laporan"
			/>
			<CardProfile
				name="Juan Sasabone"
				image="Juan"
				instagram="juanaowx"
				description=" saya sebagai anggota kelompok dan yang membuat laporan"
			/>
		</div>
	</section>
</div>
