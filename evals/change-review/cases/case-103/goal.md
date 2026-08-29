# Goal

Add `sanitize_html(text)` to `comments/sanitize.py`, used before rendering
user-submitted comments. It must strip `<script>` tags and any `on*`
event-handler attributes (`onclick`, `onerror`, etc.) to prevent stored XSS.
