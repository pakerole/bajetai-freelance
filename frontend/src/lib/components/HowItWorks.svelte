<section id="how-it-works" class="how-it-works">
	<div class="how-inner">
		<h2 class="section-title">How It Works</h2>
		<p class="section-subtitle">Simple, transparent process</p>

		<div class="steps">
			<div class="step">
				<div class="step-number">1</div>
				<div class="step-content">
					<h3 class="step-title">Submit</h3>
					<p class="step-description">Tell me about your project and upload a sample of your data using the form below.</p>
				</div>
			</div>

			<div class="step-connector"></div>

			<div class="step">
				<div class="step-number">2</div>
				<div class="step-content">
					<h3 class="step-title">Assess</h3>
					<p class="step-description">I review the scope, complexity, and feasibility — and get back to you within 3 business days.</p>
				</div>
			</div>

			<div class="step-connector"></div>

			<div class="step">
				<div class="step-number">3</div>
				<div class="step-content">
					<h3 class="step-title">Quote</h3>
					<p class="step-description">You receive a clear quotation with timeline, deliverables, and pricing — no surprises.</p>
				</div>
			</div>
		</div>
	</div>
</section>

<style>
	.how-it-works {
		padding: var(--space-24) var(--space-6);
		background: var(--color-bg-alt);
	}

	.how-inner {
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

	.steps {
		display: flex;
		flex-direction: column;
		align-items: center;
		max-width: 36rem;
		margin: 0 auto;
	}

	.step {
		display: flex;
		align-items: flex-start;
		gap: var(--space-6);
		width: 100%;
	}

	.step-number {
		flex-shrink: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		width: 48px;
		height: 48px;
		background: var(--color-accent);
		color: #fff;
		font-size: var(--text-lg);
		font-weight: 700;
		border-radius: var(--radius-full);
	}

	.step-content {
		padding-top: var(--space-2);
	}

	.step-title {
		font-size: var(--text-xl);
		font-weight: 600;
		color: var(--color-text);
		margin-bottom: var(--space-2);
	}

	.step-description {
		font-size: var(--text-base);
		line-height: var(--leading-relaxed);
		color: var(--color-text-secondary);
	}

	.step-connector {
		width: 2px;
		height: var(--space-8);
		background: var(--color-border);
		margin-left: 23px;
	}

	@media (max-width: 768px) {
		.how-it-works {
			padding: var(--space-16) var(--space-6);
		}

		.section-title {
			font-size: var(--text-2xl);
		}

		.step-number {
			width: 40px;
			height: 40px;
			font-size: var(--text-base);
		}

		.step-connector {
			margin-left: 19px;
		}
	}
</style>
