<script lang="ts">
	let name = $state('');
	let email = $state('');
	let company = $state('');
	let inquiryType = $state('');
	let description = $state('');
	let file = $state<File | null>(null);
	let formStatus = $state<'idle' | 'loading' | 'success' | 'error'>('idle');
	let errorMessage = $state('');

	const inquiryTypes = [
		'Quotation Request',
		'General Inquiry'
	];

	const maxFileSize = 10 * 1024 * 1024; // 10MB

	let fileName = $derived(file?.name ?? 'No file chosen');

	function handleFileChange(e: Event) {
		const input = e.target as HTMLInputElement;
		const selected = input.files?.[0] ?? null;

		if (selected) {
			const allowedTypes = [
				'text/csv',
				'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
				'application/vnd.ms-excel',
				'application/json'
			];
			const allowedExts = ['.csv', '.xlsx', '.xls', '.json'];
			const ext = '.' + selected.name.split('.').pop()?.toLowerCase();

			if (!allowedTypes.includes(selected.type) && !allowedExts.includes(ext)) {
				errorMessage = 'Invalid file type. Please upload CSV, Excel, or JSON files only.';
				file = null;
				input.value = '';
				return;
			}

			if (selected.size > maxFileSize) {
				errorMessage = 'File too large. Maximum size is 10MB.';
				file = null;
				input.value = '';
				return;
			}

			errorMessage = '';
			file = selected;
		}
	}

	function validate(): boolean {
		if (!name.trim()) { errorMessage = 'Name is required.'; return false; }
		if (!email.trim()) { errorMessage = 'Email is required.'; return false; }
		if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) { errorMessage = 'Please enter a valid email address.'; return false; }
		if (!inquiryType) { errorMessage = 'Please select an inquiry type.'; return false; }
		if (!description.trim()) { errorMessage = 'Project description is required.'; return false; }
		if (description.trim().length < 20) { errorMessage = 'Please provide a more detailed description (at least 20 characters).'; return false; }
		errorMessage = '';
		return true;
	}

	async function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		if (!validate()) return;

		formStatus = 'loading';
		errorMessage = '';

		try {
			const formData = new FormData();
			formData.append('name', name.trim());
			formData.append('email', email.trim());
			if (company.trim()) formData.append('company', company.trim());
			formData.append('inquiry_type', inquiryType);
			formData.append('description', description.trim());
			if (file) formData.append('file', file);

			const response = await fetch('/api/submit', {
				method: 'POST',
				body: formData
			});

			if (!response.ok) {
				const data = await response.json().catch(() => ({}));
				throw new Error(data.detail || data.message || `Server error (${response.status})`);
			}

			formStatus = 'success';
		} catch (err) {
			formStatus = 'error';
			errorMessage = err instanceof Error ? err.message : 'Something went wrong. Please try again.';
		}
	}

	function resetForm() {
		name = '';
		email = '';
		company = '';
		inquiryType = '';
		description = '';
		file = null;
		formStatus = 'idle';
		errorMessage = '';
	}
</script>

<section id="contact" class="contact">
	<div class="contact-inner">
		<h2 class="section-title">Get in Touch</h2>
		<p class="section-subtitle">Questions or project ideas? Drop me a message.</p>

		{#if formStatus === 'success'}
			<div class="success-card">
				<div class="success-icon">
					<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
						<path d="M20 6L9 17l-5-5"/>
					</svg>
				</div>
				<h3>Message sent!</h3>
				<p>Thank you for reaching out! I've received your requirements and will review the scope within 3 business days. You'll receive a tailored quotation via email.</p>
				<button class="btn-secondary" onclick={resetForm}>Send another inquiry</button>
			</div>
		{:else}
			<form class="contact-form" onsubmit={handleSubmit} novalidate>
				{#if errorMessage}
					<div class="form-error">
						{errorMessage}
					</div>
				{/if}

				<div class="form-row">
					<div class="form-group">
						<label for="name">Name <span class="required">*</span></label>
						<input id="name" type="text" bind:value={name} placeholder="Your name" required disabled={formStatus === 'loading'} />
					</div>
					<div class="form-group">
						<label for="email">Email <span class="required">*</span></label>
						<input id="email" type="email" bind:value={email} placeholder="you@example.com" required disabled={formStatus === 'loading'} />
					</div>
				</div>

				<div class="form-group">
					<label for="company">Company</label>
					<input id="company" type="text" bind:value={company} placeholder="Your company (optional)" disabled={formStatus === 'loading'} />
				</div>

				<div class="form-group">
					<label for="inquiry-type">Inquiry Type <span class="required">*</span></label>
					<select id="inquiry-type" bind:value={inquiryType} required disabled={formStatus === 'loading'}>
						<option value="" disabled>Select inquiry type</option>
						{#each inquiryTypes as type}
							<option value={type}>{type}</option>
						{/each}
					</select>
				</div>

				<div class="form-group">
					<label for="description">Project Description <span class="required">*</span></label>
					<textarea id="description" bind:value={description} rows="5" placeholder="Describe your project, data sources, and what you'd like to achieve..." required disabled={formStatus === 'loading'}></textarea>
				</div>

				<div class="form-group">
					<label for="file">Sample Data (optional)</label>
					<div class="file-upload">
						<input id="file" type="file" accept=".csv,.xlsx,.xls,.json" onchange={handleFileChange} disabled={formStatus === 'loading'} />
						<label for="file" class="file-label">
							<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
								<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
								<polyline points="17 8 12 3 7 8"/>
								<line x1="12" y1="3" x2="12" y2="15"/>
							</svg>
							<span>Choose file or drag &amp; drop</span>
						</label>
						{#if file}
							<span class="file-name">{fileName}</span>
						{/if}
					</div>
					<p class="file-hint">CSV, Excel, or JSON — max 10MB</p>
				</div>

				<button type="submit" class="submit-btn" disabled={formStatus === 'loading'}>
					{#if formStatus === 'loading'}
						<span class="spinner"></span>
						Sending...
					{:else}
						Send Inquiry
					{/if}
				</button>
			</form>
		{/if}
	</div>
</section>

<style>
	.contact {
		padding: var(--space-24) var(--space-6);
	}

	.contact-inner {
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
		margin-bottom: var(--space-10);
	}

	.contact-form {
		max-width: 40rem;
	}

	.form-error {
		background: #fef2f2;
		border: 1px solid #fecaca;
		color: #dc2626;
		padding: var(--space-3) var(--space-4);
		border-radius: var(--radius-md);
		font-size: var(--text-sm);
		margin-bottom: var(--space-6);
	}

	.form-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--space-6);
	}

	.form-group {
		margin-bottom: var(--space-6);
	}

	.form-group label {
		display: block;
		font-size: var(--text-sm);
		font-weight: 500;
		color: var(--color-text);
		margin-bottom: var(--space-2);
	}

	.required {
		color: var(--color-accent);
	}

	.form-group input[type="text"],
	.form-group input[type="email"],
	.form-group select,
	.form-group textarea {
		width: 100%;
		font-family: var(--font-sans);
		font-size: var(--text-base);
		color: var(--color-text);
		background: var(--color-bg);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		padding: var(--space-3) var(--space-4);
		transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
	}

	.form-group input:focus,
	.form-group select:focus,
	.form-group textarea:focus {
		outline: none;
		border-color: var(--color-accent);
		box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
	}

	.form-group input:disabled,
	.form-group select:disabled,
	.form-group textarea:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.form-group textarea {
		resize: vertical;
		min-height: 120px;
	}

	.form-group select {
		cursor: pointer;
		appearance: none;
		background-image: url("data:image/svg+xml,%3Csvg width='12' height='8' viewBox='0 0 12 8' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1.5L6 6.5L11 1.5' stroke='%236b7280' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
		background-repeat: no-repeat;
		background-position: right var(--space-4) center;
		padding-right: var(--space-10);
	}

	.file-upload {
		position: relative;
	}

	.file-upload input[type="file"] {
		position: absolute;
		width: 1px;
		height: 1px;
		overflow: hidden;
		clip: rect(0, 0, 0, 0);
	}

	.file-label {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-sm);
		font-weight: 500;
		color: var(--color-accent);
		background: var(--color-accent-light);
		border: 1px dashed var(--color-accent);
		border-radius: var(--radius-md);
		padding: var(--space-3) var(--space-4);
		cursor: pointer;
		transition: background var(--transition-fast);
	}

	.file-label:hover {
		background: #dbeafe;
	}

	.file-name {
		display: inline-block;
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		margin-left: var(--space-3);
	}

	.file-hint {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		margin-top: var(--space-2);
	}

	.submit-btn {
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
		padding: var(--space-3) var(--space-10);
		cursor: pointer;
		transition: background var(--transition-fast), transform var(--transition-fast);
	}

	.submit-btn:hover:not(:disabled) {
		background: var(--color-accent-hover);
		transform: translateY(-1px);
	}

	.submit-btn:disabled {
		opacity: 0.7;
		cursor: not-allowed;
	}

	.spinner {
		display: inline-block;
		width: 18px;
		height: 18px;
		border: 2px solid rgba(255, 255, 255, 0.3);
		border-top-color: #fff;
		border-radius: 50%;
		animation: spin 0.6s linear infinite;
	}

	@keyframes spin {
		to { transform: rotate(360deg); }
	}

	.success-card {
		max-width: 40rem;
		text-align: center;
		padding: var(--space-12) var(--space-8);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		background: var(--color-bg-alt);
	}

	.success-icon {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 64px;
		height: 64px;
		background: #ecfdf5;
		color: #059669;
		border-radius: var(--radius-full);
		margin-bottom: var(--space-6);
	}

	.success-card h3 {
		font-size: var(--text-2xl);
		font-weight: 600;
		color: var(--color-text);
		margin-bottom: var(--space-4);
	}

	.success-card p {
		font-size: var(--text-base);
		line-height: var(--leading-relaxed);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-8);
	}

	.btn-secondary {
		font-family: var(--font-sans);
		font-size: var(--text-sm);
		font-weight: 500;
		color: var(--color-accent);
		background: transparent;
		border: 1px solid var(--color-accent);
		border-radius: var(--radius-md);
		padding: var(--space-2) var(--space-6);
		cursor: pointer;
		transition: background var(--transition-fast);
	}

	.btn-secondary:hover {
		background: var(--color-accent-light);
	}

	@media (max-width: 768px) {
		.contact {
			padding: var(--space-16) var(--space-6);
		}

		.section-title {
			font-size: var(--text-2xl);
		}

		.form-row {
			grid-template-columns: 1fr;
		}
	}
</style>
