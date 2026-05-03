<script lang="ts">
	import Hero from '$lib/components/Hero.svelte';
	import About from '$lib/components/About.svelte';
	import Services from '$lib/components/Services.svelte';
	import HowItWorks from '$lib/components/HowItWorks.svelte';
	import ContactForm from '$lib/components/ContactForm.svelte';
	import Footer from '$lib/components/Footer.svelte';
</script>

<svelte:head>
	<title>bajetAI — Data Scientist &amp; Analytics Engineer</title>
</svelte:head>

<main>
	<Hero />
	<About />
	<Services />
	<HowItWorks />
	<ContactForm />
</main>

<Footer />
