<script lang="ts">
	function scrollToContact() {
		const el = document.querySelector('#contact');
		if (el) el.scrollIntoView({ behavior: 'smooth' });
	}
</script>

<section class="hero">
	<div class="hero-inner">
		<div class="hero-badge">Open for projects</div>
		<h1 class="hero-name">Ahmad Fakrul Radzy<br /><span class="hero-nickname">(Radzy)</span></h1>
		<p class="hero-tagline">Data Scientist &amp; Analytics Engineer</p>
		<p class="hero-one-liner">"Turning complex data into clear decisions"</p>
		<button class="hero-cta" onclick={scrollToContact}>
			Start a Project
			<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
				<path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
			</svg>
		</button>
	</div>
</section>

<style>
	.hero {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: calc(var(--nav-height) + var(--space-16)) var(--space-6) var(--space-16);
	}

	.hero-inner {
		max-width: var(--container-max);
		text-align: center;
	}

	.hero-badge {
		display: inline-block;
		font-size: var(--text-xs);
		font-weight: 600;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: var(--color-accent);
		background: var(--color-accent-light);
		padding: var(--space-2) var(--space-4);
		border-radius: var(--radius-full);
		margin-bottom: var(--space-8);
	}

	.hero-name {
		font-size: var(--text-5xl);
		font-weight: 700;
		line-height: var(--leading-tight);
		letter-spacing: -0.03em;
		color: var(--color-text);
		margin-bottom: var(--space-6);
	}

	.hero-nickname {
		font-weight: 400;
		color: var(--color-text-muted);
	}

	.hero-tagline {
		font-size: var(--text-xl);
		font-weight: 500;
		color: var(--color-text-secondary);
		margin-bottom: var(--space-4);
	}

	.hero-one-liner {
		font-size: var(--text-lg);
		color: var(--color-text-muted);
		font-style: italic;
		margin-bottom: var(--space-10);
	}

	.hero-cta {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-base);
		font-weight: 600;
		font-family: var(--font-sans);
		color: #fff;
		background: var(--color-accent);
		border: none;
		border-radius: var(--radius-md);
		padding: var(--space-3) var(--space-8);
		cursor: pointer;
		transition: background var(--transition-fast), transform var(--transition-fast);
	}

	.hero-cta:hover {
		background: var(--color-accent-hover);
		transform: translateY(-1px);
	}

	.hero-cta:active {
		transform: translateY(0);
	}

	@media (max-width: 768px) {
		.hero-name {
			font-size: var(--text-3xl);
		}

		.hero-tagline {
			font-size: var(--text-lg);
		}

		.hero-one-liner {
			font-size: var(--text-base);
		}
	}
</style>
