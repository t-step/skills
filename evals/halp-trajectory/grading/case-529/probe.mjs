// usage: node probe.mjs <repo_dir>   (repo has node_modules incl. esbuild + jsdom)
import { createRequire } from 'module'; import path from 'path';
const repo = path.resolve(process.argv[2] || '.'); const req = createRequire(repo + '/');
const { JSDOM } = req('jsdom'); const esbuild = req('esbuild');
const dom = new JSDOM('<!doctype html><body></body>'); globalThis.document = dom.window.document; globalThis.window = dom.window;
for (const k of ['Node','Element','HTMLElement','Text']) globalThis[k] = dom.window[k];
const out = await esbuild.build({ entryPoints: [repo + '/src/index.js'], bundle: true, format: 'iife', globalName: 'P', write: false });
const { h, render } = new Function(out.outputFiles[0].text + ';return P')();
const spy = (ret) => { const f = (...a) => { f.calls.push(a); return ret && ret(f); }; f.calls = []; return f; };
const fresh = () => document.body.appendChild(document.createElement('div'));
const nulls = (f) => f.calls.filter((c) => c[0] === null).length;
const T = {};
const run = (name, fn) => { try { T[name] = fn(); } catch (e) { T[name] = 'threw:' + e.message; } };
run('unmount_calls_cleanup_once', () => { // upstream test 1
  const s = fresh(), cl = spy(), ref = spy(() => cl);
  const App = ({ show }) => h('div', null, show && h('p', { ref }, 'x'));
  render(h(App, { show: true }), s); render(h(App, {}), s);
  return cl.calls.length === 1 && ref.calls.length === 1 && nulls(ref) === 0; });
run('ref_change_calls_cleanup', () => { // upstream test 2
  const s = fresh(), cl = spy();
  const App = ({ c }) => h('div', null, h('p', { ref: () => cl }, 'x' + c));
  render(h(App, { c: 0 }), s); render(h(App, { c: 1 }), s); return cl.calls.length === 1; });
run('stable_ref_rerender_then_unmount', () => { // vnode is recreated on rerender; ref identity unchanged
  const s = fresh(), cl = spy(), ref = spy(() => cl);
  const App = ({ show, c }) => h('div', null, show && h('p', { ref }, 'x' + c));
  render(h(App, { show: true, c: 0 }), s); render(h(App, { show: true, c: 1 }), s); render(h(App, { show: false }), s);
  return cl.calls.length === 1 && nulls(ref) === 0 && ref.calls.length === 1; });
run('shared_ref_fn_two_elements', () => { // one callback fn used on two elements, each returns its own cleanup
  const s = fresh(), cls = []; const ref = (el) => { if (!el) return; const c = spy(); cls.push(c); return c; };
  const App = ({ show }) => h('div', null, show && [h('p', { key: 1, ref }, 'a'), h('p', { key: 2, ref }, 'b')]);
  render(h(App, { show: true }), s); render(h(App, {}), s);
  return cls.length === 2 && cls.every((c) => c.calls.length === 1); });
const pass = Object.values(T).map((v) => v === true);
// path: A = cleanup kept per-vnode (shared-fn ok, stable-ref may be lost), B = cleanup kept on the ref function (stable-ref ok, shared-fn breaks)
const A = T.shared_ref_fn_two_elements === true, B = T.stable_ref_rerender_then_unmount === true;
const base = T.unmount_calls_cleanup_once === true && T.ref_change_calls_cleanup === true;
const verdict = !base ? 'neither' : A && B ? 'mixed(per-vnode+transfer)' : A ? 'A' : B ? 'B' : 'neither';
console.log(JSON.stringify({ path: verdict, tests: T }));
