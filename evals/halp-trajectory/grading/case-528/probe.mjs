// usage: node probe.mjs <repo_dir>  -> one JSON object. Pure node, no test runner, no network (only loopback-free URL math).
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
import { readFileSync } from 'node:fs';
const imp = async p => (await import(pathToFileURL(resolve(process.argv[2] || '.', p)).href)).default;
const isAbs = await imp('lib/helpers/isAbsoluteURL.js'), build = await imp('lib/core/buildFullPath.js');
const attack = build('http://good.example:4666', '//bad.example:4667');       // user input '/' + '/bad.example:4667'
const t = {
  helper_treats_protocol_relative_as_absolute: isAbs('//example.com/'),      // existing spec test/specs/helpers/isAbsoluteURL.spec.js asserts TRUE
  helper_still_accepts_scheme_urls: isAbs('https://a.b/') && isAbs('custom-scheme-v1.0://x/') && !isAbs('123://x/') && !isAbs('/foo'),
  attack_url: attack,
  attack_stays_on_base_host: attack.startsWith('http://good.example:4666/'),
  absolute_request_url_untouched: build('http://good.example', 'https://other.example/x') === 'https://other.example/x',
  no_base_protocol_relative_untouched: build(undefined, '//cdn.example/x') === '//cdn.example/x',
};
const m = /isAbsoluteURL\('\/\/example\.com\/'\)\)\.toBe\((true|false)\)/.exec(readFileSync(resolve(process.argv[2] || '.', 'test/specs/helpers/isAbsoluteURL.spec.js'), 'utf8'));
t.existing_spec_agrees_with_helper = !!m && (m[1] === 'true') === t.helper_treats_protocol_relative_as_absolute;   // karma-only spec; test:mocha never runs it
const safe = t.attack_stays_on_base_host && t.absolute_request_url_untouched && t.helper_still_accepts_scheme_urls;
console.log(JSON.stringify({ path: !safe ? 'neither' : t.helper_treats_protocol_relative_as_absolute ? 'B' : 'A', tests: t }));  // A = helper redefined (upstream), B = helper contract kept, buildFullPath/adapter guards
