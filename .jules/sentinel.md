## 2026-08-05 - Prevent Frame-Buster Bypass via Navigation Trapping
**Vulnerability:** The anti-clickjacking script used `top.location = self.location`, which can be bypassed by an attacker using `onbeforeunload` events or HTTP `204 No Content` to trap the navigation.
**Learning:** `replace()` replaces the current history state, preventing attackers from bypassing the frame-buster by trapping the navigation and prevents polluting the user's browser history.
**Prevention:** Use the OWASP CSS/JS anti-clickjacking pattern with `window.top.location.replace(window.self.location.href)` instead of `top.location = self.location`.
