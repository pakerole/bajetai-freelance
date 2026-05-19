import type { Handle } from '@sveltejs/kit';

// Known bot/scanner paths — return immediately without rendering
const BLOCKED_PATHS = [
	'/wp-admin', '/wp-login', '/wp-content', '/wp-includes', '/xmlrpc.php',
	'/.env', '/.git', '/.DS_Store', '/.htaccess', '/.config',
	'/admin', '/backup', '/database', '/db',
	'/config.php', '/info.php', '/phpmyadmin', '/pma',
	'/actuator', '/.well-known/security.txt',
	'/robots.txt', '/sitemap.xml', // Not needed for this landing page
];

// Suspicious query strings
const BLOCKED_QUERY = ['=http', '=ftp', '=//', 'redirect=', '../', '..\\'];

function isBotPath(url: URL): boolean {
	const path = url.pathname.toLowerCase();
	const query = url.search.toLowerCase();

	if (BLOCKED_PATHS.some(p => path.startsWith(p) || path === p)) return true;
	if (path.includes('wp-') || path.includes('wordpress')) return true;
	if (path.includes('win.ini') || path.includes('etc/passwd')) return true;
	if (path.endsWith('.php') && !path.startsWith('/api/')) return true;
	if (BLOCKED_QUERY.some(q => query.includes(q))) return true;

	// Block paths with double slashes (path traversal attempt)
	if (url.pathname.includes('//')) return true;

	return false;
}

export const handle: Handle = async ({ event, resolve }) => {
	// Block scanner/bot junk at the edge — no SvelteKit render needed
	if (isBotPath(event.url)) {
		return new Response(null, { status: 404 });
	}

	return resolve(event);
};
