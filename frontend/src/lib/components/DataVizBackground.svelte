<script lang="ts">
	import { onMount } from 'svelte';

	let canvas: HTMLCanvasElement;
	let container: HTMLDivElement;

	onMount(() => {
		let animationId = 0;
		let teardown: (() => void) | undefined;

		async function init() {
			// Import three directly from its CDN to bypass Vite's dynamic import issues
			// We create a script tag that loads three.js from CDN
			try {
				// Try CDN import since Vite's dynamic import is struggling
				const THREE = await import('https://cdn.jsdelivr.net/npm/three@0.184.0/build/three.module.js');

				const rect = container.getBoundingClientRect();
				const w = rect.width;
				const h = rect.height;
				const PC = 300, CD = 140, SR = 180;

				const scene = new THREE.Scene();
				const camera = new THREE.PerspectiveCamera(60, w / h, 1, 2000);
				camera.position.z = 500;

				const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
				renderer.setSize(w, h);
				renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
				renderer.setClearColor(0x000000, 0);

				const P = new THREE.Color('#2563eb');
				const S = new THREE.Color('#6366f1');
				const A = new THREE.Color('#06b6d4');
				const G = new THREE.Color('#1e40af');

				const pos = new Float32Array(PC * 3);
				const cols = new Float32Array(PC * 3);
				for (let i = 0; i < PC; i++) {
					const isT = i < PC * 0.3;
					let x: number, y: number, z: number;
					if (isT) {
						const t = Math.random() * Math.PI * 2, p = Math.random() * Math.PI * 2;
						const R = SR * 1.1, r = SR * 0.3;
						x = (R + r * Math.cos(t)) * Math.cos(p);
						y = (R + r * Math.cos(t)) * Math.sin(p);
						z = r * Math.sin(t);
					} else {
						const t = Math.random() * Math.PI * 2, p = Math.acos(2 * Math.random() - 1);
						const rd = SR * (0.3 + 0.7 * Math.random());
						x = rd * Math.sin(p) * Math.cos(t);
						y = rd * Math.sin(p) * Math.sin(t);
						z = rd * Math.cos(p);
					}
					pos[i * 3] = x; pos[i * 3 + 1] = y; pos[i * 3 + 2] = z;
					const t = Math.random();
					const c = t < 0.5 ? P.clone().lerp(S, Math.random())
						: t < 0.8 ? A.clone().lerp(P, Math.random())
						: G.clone().lerp(P, Math.random());
					cols[i * 3] = c.r; cols[i * 3 + 1] = c.g; cols[i * 3 + 2] = c.b;
				}

				const geom = new THREE.BufferGeometry();
				geom.setAttribute('position', new THREE.BufferAttribute(pos, 3));
				geom.setAttribute('color', new THREE.BufferAttribute(cols, 3));

				const tc = document.createElement('canvas');
				tc.width = 32; tc.height = 32;
				const ctx = tc.getContext('2d')!;
				const grad = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
				grad.addColorStop(0, 'rgba(255,255,255,1)');
				grad.addColorStop(0.3, 'rgba(255,255,255,0.8)');
				grad.addColorStop(1, 'rgba(255,255,255,0)');
				ctx.fillStyle = grad; ctx.fillRect(0, 0, 32, 32);

				const mat = new THREE.PointsMaterial({
					size: 4, map: new THREE.CanvasTexture(tc),
					blending: THREE.AdditiveBlending, depthWrite: false,
					transparent: true, opacity: 0.9, vertexColors: true,
				});
				const pts = new THREE.Points(geom, mat);
				scene.add(pts);

				const maxL = PC * 2, lp = new Float32Array(maxL * 6);
				const lg = new THREE.BufferGeometry();
				lg.setAttribute('position', new THREE.BufferAttribute(lp, 3));
				lg.setDrawRange(0, 0);
				const ln = new THREE.LineSegments(lg, new THREE.LineBasicMaterial({
					vertexColors: true, transparent: true, opacity: 0.25,
					blending: THREE.AdditiveBlending, depthWrite: false,
				}));
				scene.add(ln);

				let mx = 0, my = 0;
				const mm = (e: MouseEvent) => {
					const r = container.getBoundingClientRect();
					mx = (e.clientX - r.left) / r.width - 0.5;
					my = (e.clientY - r.top) / r.height - 0.5;
				};
				document.addEventListener('mousemove', mm);
				const rs = () => {
					const r = container.getBoundingClientRect();
					camera.aspect = r.width / r.height;
					camera.updateProjectionMatrix();
					renderer.setSize(r.width, r.height);
				};
				window.addEventListener('resize', rs);

				function anim() {
					animationId = requestAnimationFrame(anim);
					const t = Date.now() * 0.00015;
					const rx = Math.sin(t * 0.3) * 0.15 + my * 0.005;
					const ry = t + mx * 0.005;
					pts.rotation.x = rx; pts.rotation.y = ry;
					ln.rotation.x = rx; ln.rotation.y = ry;

					const dsq = CD * CD;
					let lc = 0;
					for (let i = 0; i < PC && lc < PC * 2; i++)
						for (let j = i + 1; j < PC && lc < PC * 2; j++) {
							const dx = pos[i * 3] - pos[j * 3];
							const dy = pos[i * 3 + 1] - pos[j * 3 + 1];
							const dz = pos[i * 3 + 2] - pos[j * 3 + 2];
							if (dx * dx + dy * dy + dz * dz < dsq) {
								const ci = lc * 6;
								lp[ci] = pos[i * 3]; lp[ci + 1] = pos[i * 3 + 1]; lp[ci + 2] = pos[i * 3 + 2];
								lp[ci + 3] = pos[j * 3]; lp[ci + 4] = pos[j * 3 + 1]; lp[ci + 5] = pos[j * 3 + 2];
								lc++;
							}
						}
					lg.setDrawRange(0, lc * 2);
					lg.attributes.position.needsUpdate = true;
					renderer.render(scene, camera);
				}
				anim();

				teardown = () => {
					cancelAnimationFrame(animationId);
					document.removeEventListener('mousemove', mm);
					window.removeEventListener('resize', rs);
					renderer.dispose();
				};
			} catch (e) {
				console.warn('bajetAI 3D background failed to load:', e);
			}
		}

		init();
		return () => teardown?.();
	});
</script>

<div bind:this={container} class="data-viz">
	<canvas bind:this={canvas}></canvas>
</div>

<style>
	.data-viz {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100vh;
		z-index: 0;
		pointer-events: none;
		overflow: hidden;
	}
	canvas {
		display: block;
		width: 100%;
		height: 100%;
	}
</style>
