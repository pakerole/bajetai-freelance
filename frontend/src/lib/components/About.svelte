<section id="about" class="about">
	<div class="about-inner">
		<h2 class="section-title">About</h2>

		<div class="about-text">
			<p>
				With a strong foundation in Python-driven data analysis and machine learning, I help businesses extract meaningful insights from their data — whether it's cleaning messy datasets, building predictive models, fine-tuning large language models, or creating automated reporting pipelines.
			</p>
			<p>
				My work spans from telecommunications analytics (network performance, KPI monitoring, log analysis) to applied ML (LLM fine-tuning, computer vision, speech processing). I bring data science techniques to real-world operational problems, not just academic exercises.
			</p>
			<p>
				Every project starts with understanding your data. I work across industries — from telecom to finance to e-commerce — to build solutions that are practical, scalable, and actually useful.
			</p>
		</div>

		<div class="skills-section">
			<h3 class="skills-heading">Tools &amp; Skills</h3>
			<div class="skills-grid">
				{#each ['Python', 'pandas', 'NumPy', 'SQL', 'Elasticsearch', 'PyTorch', 'Scikit-learn', 'FastAPI', 'Docker', 'Git'] as skill}
					<span class="skill-badge">{skill}</span>
				{/each}
			</div>
		</div>
	</div>
</section>

<style>
	.about {
		padding: var(--space-24) var(--space-6);
		background: var(--color-bg-alt);
	}

	.about-inner {
		max-width: var(--container-max);
		margin: 0 auto;
	}

	.section-title {
		font-size: var(--text-3xl);
		font-weight: 700;
		letter-spacing: -0.02em;
		margin-bottom: var(--space-10);
		color: var(--color-text);
	}

	.about-text {
		max-width: 48rem;
	}

	.about-text p {
		font-size: var(--text-base);
		line-height: var(--leading-relaxed);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-6);
	}

	.about-text p:last-child {
		margin-bottom: var(--space-12);
	}

	.skills-heading {
		font-size: var(--text-lg);
		font-weight: 600;
		color: var(--color-text);
		margin-bottom: var(--space-6);
	}

	.skills-grid {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-3);
	}

	.skill-badge {
		font-size: var(--text-sm);
		font-weight: 500;
		color: var(--color-text-secondary);
		background: var(--color-bg);
		border: 1px solid var(--color-border);
		padding: var(--space-2) var(--space-4);
		border-radius: var(--radius-full);
		transition: border-color var(--transition-fast), color var(--transition-fast);
	}

	.skill-badge:hover {
		border-color: var(--color-accent);
		color: var(--color-accent);
	}

	@media (max-width: 768px) {
		.about {
			padding: var(--space-16) var(--space-6);
		}

		.section-title {
			font-size: var(--text-2xl);
		}
	}
</style>
