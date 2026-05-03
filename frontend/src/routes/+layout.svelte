<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();

	let mobileMenuOpen = $state(false);
	let activeSection = $state('');

	const navLinks = [
		{ label: 'About', href: '#about' },
		{ label: 'Services', href: '#services' },
		{ label: 'How It Works', href: '#how-it-works' },
		{ label: 'Contact', href: '#contact' }
	];

	function scrollTo(href: string) {
		const el = document.querySelector(href);
		if (el) {
			el.scrollIntoView({ behavior: 'smooth' });
			mobileMenuOpen = false;
		}
	}

	function scrollToTop(e: MouseEvent) {
		e.preventDefault();
		window.scrollTo({ top: 0, behavior: 'smooth' });
	}

	$effect(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				for (const entry of entries) {
					if (entry.isIntersecting) {
						activeSection = entry.target.id;
					}
				}
			},
			{ rootMargin: '-40% 0px -55% 0px' }
		);

		const sections = document.querySelectorAll('section[id]');
		for (const section of sections) {
			observer.observe(section);
		}

		return () => observer.disconnect();
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<nav class="nav">
	<div class="nav-inner">
		<a href="#" class="nav-logo" onclick={scrollToTop}>bajet<span class="logo-accent">AI</span></a>

		<!-- Desktop nav -->
		<ul class="nav-links">
			{#each navLinks as link}
				<li>
					<a
						href={link.href}
						class:active={activeSection === link.href.slice(1)}
						onclick={(e) => { e.preventDefault(); scrollTo(link.href); }}
					>
						{link.label}
					</a>
				</li>
			{/each}
		</ul>

		<!-- Mobile hamburger -->
		<button
			class="hamburger"
			aria-label="Toggle menu"
			onclick={() => mobileMenuOpen = !mobileMenuOpen}
		>
			<span class="hamburger-line" class:open={mobileMenuOpen}></span>
			<span class="hamburger-line" class:open={mobileMenuOpen}></span>
			<span class="hamburger-line" class:open={mobileMenuOpen}></span>
		</button>
	</div>

	<!-- Mobile menu -->
	{#if mobileMenuOpen}
		<ul class="mobile-menu">
			{#each navLinks as link}
				<li>
					<a
						href={link.href}
						onclick={(e) => { e.preventDefault(); scrollTo(link.href); }}
					>
						{link.label}
					</a>
				</li>
			{/each}
		</ul>
	{/if}
</nav>

{@render children()}

<style>
	.nav {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		z-index: 1000;
		height: var(--nav-height);
		background: var(--color-bg);
		border-bottom: 1px solid var(--color-border);
		backdrop-filter: blur(8px);
		background: rgba(255, 255, 255, 0.92);
	}

	.nav-inner {
		max-width: var(--container-max);
		margin: 0 auto;
		padding: 0 var(--space-6);
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.nav-logo {
		font-size: var(--text-xl);
		font-weight: 700;
		color: var(--color-text);
		letter-spacing: -0.02em;
	}

	.nav-logo:hover {
		color: var(--color-text);
	}

	.logo-accent {
		color: var(--color-accent);
	}

	.nav-links {
		display: flex;
		list-style: none;
		gap: var(--space-8);
	}

	.nav-links a {
		font-size: var(--text-sm);
		font-weight: 500;
		color: var(--color-text-secondary);
		transition: color var(--transition-fast);
	}

	.nav-links a:hover,
	.nav-links a.active {
		color: var(--color-accent);
	}

	.hamburger {
		display: none;
		flex-direction: column;
		justify-content: center;
		gap: 5px;
		background: none;
		border: none;
		cursor: pointer;
		padding: var(--space-2);
	}

	.hamburger-line {
		display: block;
		width: 22px;
		height: 2px;
		background: var(--color-text);
		transition: all var(--transition-fast);
		border-radius: 1px;
	}

	.hamburger-line.open:nth-child(1) {
		transform: rotate(45deg) translate(5px, 5px);
	}

	.hamburger-line.open:nth-child(2) {
		opacity: 0;
	}

	.hamburger-line.open:nth-child(3) {
		transform: rotate(-45deg) translate(5px, -5px);
	}

	.mobile-menu {
		display: none;
		list-style: none;
		padding: var(--space-4) var(--space-6) var(--space-6);
		border-bottom: 1px solid var(--color-border);
		background: var(--color-bg);
	}

	.mobile-menu a {
		display: block;
		padding: var(--space-3) 0;
		font-size: var(--text-base);
		font-weight: 500;
		color: var(--color-text-secondary);
		border-bottom: 1px solid var(--color-border);
	}

	.mobile-menu li:last-child a {
		border-bottom: none;
	}

	@media (max-width: 768px) {
		.nav-links {
			display: none;
		}

		.hamburger {
			display: flex;
		}

		.mobile-menu {
			display: block;
		}
	}
</style>
