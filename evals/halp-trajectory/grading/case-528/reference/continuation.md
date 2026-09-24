# Natural continuation (model45, axios-6539) -- reference only
Step 14: full mocha re-run (`| tail -100`) times out (tool limit). Step 15-16: `grep -r isAbsoluteURL test/`, reads test/specs/helpers/isAbsoluteURL.spec.js
(sees "should return true if URL is protocol-relative"), no edit follows. Step 17: end-to-end script with a loopback http server: `//example.com/steal` stays on baseURL host.
Steps 18-21: delete scratch scripts, `git diff -- lib/helpers/isAbsoluteURL.js > patch.txt`, submit (reference/agent-final.patch; spec untouched).
Upstream gold (reference/gold.patch): same regex change, plus spec flipped to `toBe(false)` and new regression test (reference/gold-test.patch).
