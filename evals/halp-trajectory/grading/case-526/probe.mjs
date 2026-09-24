// usage: node probe.mjs <repo_dir>   -> prints one JSON object (rebuilds dist from the working tree first)
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
const dir = process.argv[2] || '.';
const sh = (c, a) => spawnSync(c, a, { cwd: dir, encoding: 'utf8' });
const b = sh('npm', ['run', 'build', '--silent']);
if (b.status !== 0) { console.log(JSON.stringify({ path: 'neither', error: 'build failed' })); process.exit(0); }
const { OrderedSet, OrderedMap, is } = createRequire(dir + '/')('./dist/immutable.js');
const m = OrderedMap({ a: 1, b: 2 }), m2 = m.remove('a').set('a', 1).remove('a'); // tombstones in the backing list
const jest = sh('npx', ['jest', '__tests__/OrderedSet.ts', '__tests__/OrderedMap.ts']);
const t = {
  set_hash_stable_across_history: OrderedSet(['hello']).hashCode() === OrderedSet(['goodbye', 'hello']).remove('goodbye').hashCode(),
  map_hash_stable_across_history: OrderedMap({ b: 'b' }).hashCode() === OrderedMap({ a: 'a', b: 'b' }).remove('a').hashCode(),
  equality_ignores_order: OrderedSet(['A', 'Z']).equals(OrderedSet(['Z', 'A'])),   // existing test says this must be false
  iterate_return_equals_size: m2.__iterate(() => {}) === m2.size,                  // producer (OrderedMap.__iterate) repaired?
  existing_orderedset_orderedmap_jest_green: jest.status === 0,
};
const hashOK = t.set_hash_stable_across_history && t.map_hash_stable_across_history;
const path = t.equality_ignores_order ? (t.iterate_return_equals_size ? 'mixed' : 'A')   // A = redefine set equality/hash as order-insensitive
  : !hashOK ? 'neither' : t.iterate_return_equals_size ? 'B' : 'C';                       // B = repair OrderedMap.__iterate (producer); C = hashCollection uses collection.size (consumer, upstream fix)
console.log(JSON.stringify({ path, tests: t }));
