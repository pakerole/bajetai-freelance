<script lang="ts">
	const services = [
		{
			title: 'Data Analysis & Reporting',
			icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 16l4-8 4 4 5-6"/></svg>`,
			description: 'Raw data won\'t tell you much until someone asks the right questions. I analyze datasets — from CSV exports to database queries — and produce clear reports with actionable findings. Whether it\'s sales trends, operational metrics, or customer behavior patterns.'
		},
		{
			title: 'Data Pipelines & Automation',
			icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>`,
			description: 'Manual data processing is error-prone and slow. I build automated pipelines that ingest, clean, transform, and deliver your data on schedule. Web scraping scripts, ETL jobs, API integrations, report generators — whatever keeps your data flowing.'
		},
		{
			title: 'Data Visualization & Dashboards',
			icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>`,
			description: 'Numbers are easier to act on when you can see them. I create dashboards and visualizations — static reports or interactive views — that make your data speak at a glance. Matplotlib, Plotly, or custom-built solutions.'
		},
		{
			title: 'Custom Tooling & APIs',
			icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>`,
			description: 'Sometimes what you need is a tool that doesn\'t exist yet. I develop custom Python applications, REST APIs, and automation scripts tailored to your specific workflow. From file-processing utilities to full data platforms.'
		}
	];
</script>

<section id="services" class="services">
	<div class="services-inner">
		<h2 class="section-title">Services</h2>
		<p class="section-subtitle">What I can do for you</p>

		<div class="services-grid">
			{#each services as service}
				<article class="service-card">
					<div class="service-icon">
						{@html service.icon}
					</div>
					<h3 class="service-title">{service.title}</h3>
					<p class="service-description">{service.description}</p>
				</article>
			{/each}
		</div>
	</div>
</section>

<style>
	.services {
		padding: var(--space-24) var(--space-6);
	}

	.services-inner {
		max-width: var(--container-max);
		margin: 0 auto;
	}

	.section-title {
		font-size: var(--text-3xl);
		font-weight: 700;
		letter-spacing: -0.02em;
		color: var(--color-text);
		margin-bottom: var(--space-2);
	}

	.section-subtitle {
		font-size: var(--text-lg);
		color: var(--color-text-muted);
		margin-bottom: var(--space-12);
	}

	.services-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: var(--space-8);
	}

	.service-card {
		background: var(--color-bg-alt);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: var(--space-8);
		transition: border-color var(--transition-base), box-shadow var(--transition-base);
	}

	.service-card:hover {
		border-color: var(--color-accent);
		box-shadow: var(--shadow-md);
	}

	.service-icon {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 48px;
		height: 48px;
		background: var(--color-accent-light);
		color: var(--color-accent);
		border-radius: var(--radius-md);
		margin-bottom: var(--space-6);
	}

	.service-title {
		font-size: var(--text-xl);
		font-weight: 600;
		color: var(--color-text);
		margin-bottom: var(--space-4);
	}

	.service-description {
		font-size: var(--text-base);
		line-height: var(--leading-relaxed);
		color: var(--color-text-secondary);
	}

	@media (max-width: 768px) {
		.services {
			padding: var(--space-16) var(--space-6);
		}

		.section-title {
			font-size: var(--text-2xl);
		}

		.services-grid {
			grid-template-columns: 1fr;
		}

		.service-card {
			padding: var(--space-6);
		}
	}
</style>
