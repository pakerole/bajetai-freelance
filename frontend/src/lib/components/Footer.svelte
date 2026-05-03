<footer class="footer">
	<div class="footer-inner">
		<div class="footer-left">
			&copy; 2026 <strong>bajetAI</strong> — Ahmad Fakrul Radzy
		</div>
		<div class="footer-right">
			<a href="mailto:hello@bajetai.my">hello@bajetai.my</a>
		</div>
	</div>
</footer>

<style>
	.footer {
		padding: var(--space-8) var(--space-6);
		border-top: 1px solid var(--color-border);
		background: var(--color-bg);
	}

	.footer-inner {
		max-width: var(--container-max);
		margin: 0 auto;
		display: flex;
		align-items: center;
		justify-content: space-between;
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	.footer-left strong {
		color: var(--color-text);
		font-weight: 600;
	}

	.footer-right a {
		color: var(--color-text-muted);
		font-weight: 500;
	}

	.footer-right a:hover {
		color: var(--color-accent);
	}

	@media (max-width: 768px) {
		.footer-inner {
			flex-direction: column;
			gap: var(--space-3);
			text-align: center;
		}
	}
</style>
