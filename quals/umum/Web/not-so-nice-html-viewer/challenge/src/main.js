
"use strict";

const HISTORY_STORAGE_KEY = "htmlViewer_history";
const THEME_STORAGE_KEY = "htmlViewer_theme";
const CACHE_KEY_STORAGE = "cache_key";

const DEFAULT_CONFIG = Object.freeze({
    autoRender: false,
    parentTextColor: null,
    parentBackgroundColor: null,
});

const SAFE_IFRAME_ATTRS = Object.freeze({
    title: "HTML preview",
    loading: "lazy",
    referrerpolicy: "no-referrer",
});

const ALLOWED_CONFIG_KEYS = new Set([
    "autoRender",
    "parentTextColor",
    "parentBackgroundColor",
]);

const elements = {
    output: document.getElementById("output"),
    status: document.getElementById("status"),
    statusText: document.getElementById("statusText"),
    htmlInput: document.getElementById("htmlInput"),
    renderBtn: document.getElementById("renderBtn"),
    clearBtn: document.getElementById("clearBtn"),
    copyUrlBtn: document.getElementById("copyUrlBtn"),
    themeBtn: document.getElementById("themeBtn"),
    themeIcon: document.getElementById("themeIcon"),
    historyBtn: document.getElementById("historyBtn"),
    historyPanel: document.getElementById("historyPanel"),
    historyList: document.getElementById("historyList"),
    charCount: document.getElementById("charCount"),
    toast: document.getElementById("toast"),
};

const randomHex = () =>
    Math.floor(Math.random() * 0xfff).toString(16).padStart(3, "0");

function setAttributes(el, attrs = {}) {
    for (const attr in attrs) {
        if (new RegExp("^on.*|src.*", "gi").test(attr)) {
            continue;
        } else if (attrs[attr].length > 10) {
            delete attrs[attr];
            continue;
        } else {
            el.setAttribute(attr, attrs[attr]);
        }
    }
    return el;
}

function showToast(message, duration = 2500) {
    elements.toast.textContent = message;
    elements.toast.classList.add("show");
    setTimeout(() => elements.toast.classList.remove("show"), duration);
}

function updateStatus(message, type = "") {
    elements.status.className = type ? type : "";
    elements.statusText.textContent = message;
}

function updateCharCount() {
    const length = elements.htmlInput.value.length;
    elements.charCount.textContent = `${length.toLocaleString()} characters`;
}

function isValidColor(color) {
    if (!color || typeof color !== "string") return false;
    const s = new Option().style;
    s.color = color;
    return s.color !== "";
}

const hasAttr = Element.prototype.hasAttribute;
const getAttr = Element.prototype.getAttribute;
const setAttr = Element.prototype.setAttribute;

DOMPurify.addHook("beforeSanitizeAttributes", (node) => {
    if (!(node instanceof Element)) return;

    if (hasAttr.call(node, "id")) {
        const id = getAttr.call(node, "id") || "";
        setAttr.call(node, "id", `${randomHex()}-${id}`);
    }

    if (hasAttr.call(node, "class")) {
        const classes = (getAttr.call(node, "class") || "")
            .split(/\s+/)
            .filter(Boolean);
        if (classes.length) {
            const hex = randomHex();
            setAttr.call(
                node,
                "class",
                classes.map((cls) => `${hex}-${cls}`).join(" ")
            );
        }
    }
});

function decodeHashPayload() {
    const encoded = location.hash.slice(1);
    if (!encoded) return null;

    try {
        const decoded = atob(decodeURIComponent(encoded));
        const parsed = JSON.parse(decoded);

        if (!parsed || typeof parsed !== "object") {
            throw new Error("Payload must be an object");
        }

        if (parsed?.html) {
            if (String(parsed?.html).length > 255) {
                parsed.html = "HTML is too big"
                throw new Error("HTML is too big");
            }
        }

        return parsed;
    } catch (err) {
        console.error("Failed to decode hash payload:", err.message);
        updateStatus(`Invalid payload: ${err.message}`, "error");
        return null;
    }
}

function encodePayload(html, config) {
    const payload = { html, config };
    return btoa(JSON.stringify(payload));
}

function isObject(value) {
    return value !== null && typeof value === "object";
}

function isArray(value) {
    return Array.isArray(value);
}

function sanitizeValue(val) {
    if (typeof val === "string") {
        return val.length > 256 ? val.slice(0, 256) : val;
    }
    if (isArray(val)) {
        // Sanitize each element in array
        return val.map(function (item) {
            if (typeof item === "string" && item.length > 256) {
                return item.slice(0, 256);
            }
            return item;
        });
    }
    return val;
}

function writeConfig(output, key, value, recurse) {
    var k, o;
    if (isObject(value) && !isArray(value)) {
        o = isObject(output[key]) ? output[key] : (output[key] = {});
        for (k in value) {
            if (recurse && (recurse === true || recurse[k])) {
                writeConfig(o, k, value[k]);
            } else {
                o[k] = sanitizeValue(value[k]);
            }
        }
    } else {
        output[key] = sanitizeValue(value);
    }
}

function mergeConfig(...configs) {
    return configs.reduce((out, source) => {
        if (!source) return out;
        for (var key in source) {
            var r = key === "style" ? true : key === "options" ? true : null;
            writeConfig(out, key, source[key], r);
        }
        return out;
    }, {});
}


function getStoredTheme() {
    try {
        return localStorage.getItem(THEME_STORAGE_KEY);
    } catch {
        return null;
    }
}

function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    elements.themeIcon.innerHTML = theme === "light" ? "&#9788;" : "&#9790;";

    try {
        localStorage.setItem(THEME_STORAGE_KEY, theme);
    } catch {
    }
}

function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "light" ? "dark" : "light";
    setTheme(next);
    showToast(`Switched to ${next} theme`);
}

function initTheme() {
    const stored = getStoredTheme();
    if (stored) {
        setTheme(stored);
    } else if (window.matchMedia("(prefers-color-scheme: light)").matches) {
        setTheme("light");
    }
}

function validateCacheKey(cacheKey) {
    if (cacheKey.length >= 5) {
        return `${randomHex()}`;
    } else {
        return cacheKey;
    }
}

function cachePayload(payload) {
    try {
        let cacheKey = validateCacheKey(localStorage[CACHE_KEY_STORAGE]);
        if (!cacheKey) {
            cacheKey = `${randomHex()}`;
            localStorage.setItem(CACHE_KEY_STORAGE, cacheKey);
        }
        localStorage.setItem(cacheKey, payload);
        window[cacheKey] = payload;
    } catch (err) {
        console.warn("Could not cache payload:", err);
    }
}

function getCachedPayload() {
    try {
        const cacheKey = validateCacheKey(localStorage[CACHE_KEY_STORAGE]);
        const payload = window[cacheKey]
        if (!payload) {
            window[cacheKey] = localStorage.getItem(cacheKey);
        }
        return window[cacheKey];
    } catch {
        return null;
    }
}

function sanitizeHtml(html = "") {
    return DOMPurify.sanitize(html);
}

function applyParentStyles(config) {
    elements.output.style.backgroundColor = config.parentBackgroundColor || "";
    elements.output.style.color = config.parentTextColor || "";
}

function renderHtml(html, config, reason = "Rendered") {
    updateStatus("Rendering...", "loading");

    try {
        const sanitized = sanitizeHtml(html);

        const iframe = document.createElement("iframe");
        iframe.sandbox = ''
        iframe.srcdoc = sanitized
        setAttributes(iframe, {
            ...SAFE_IFRAME_ATTRS,
        });

        applyParentStyles(config);
        elements.output.innerHTML = "";
        elements.output.appendChild(iframe);

        cachePayload(html);

        updateStatus(
            'Rendered',
            "success"
        );

    } catch (err) {
        console.error("Render error:", err);
        updateStatus(`Render failed: ${err.message}`, "error");
    }
}

function fallbackCopyText(text) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    try {
        document.execCommand("copy");
        return true;
    } catch {
        return false;
    } finally {
        document.body.removeChild(textarea);
    }
}
async function copyShareableUrl() {
    const html = elements.htmlInput.value;
    if (!html) {
        showToast("Nothing to share - enter some HTML first");
        return;
    }

    try {
        const encoded = encodePayload(html, activeConfig);
        const url = `${location.origin}${location.pathname}#${encoded}`;

        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(url);
        } else if (!fallbackCopyText(url)) {
            throw new Error("Copy not supported");
        }
        showToast("URL copied to clipboard!");
    } catch (err) {
        console.error("Copy failed:", err);
        showToast("Failed to copy URL");
    }
}

function handleClear() {
    elements.htmlInput.value = "";
    elements.output.innerHTML = "";
    updateCharCount();
    updateStatus("Cleared", "");
    showToast("Editor cleared");
}

function handleRender() {
    const html = elements.htmlInput.value || initialHtml;
    if (!html) {
        updateStatus("Nothing to render", "error");
        return;
    }
    renderHtml(html, activeConfig, "Rendered from button");
}

function handleInput() {
    updateCharCount();
    renderHtml(elements.htmlInput.value, activeConfig, "Live preview updated");
}

const payload = decodeHashPayload();
const activeConfig = mergeConfig(DEFAULT_CONFIG, payload?.config || {});
const initialHtml = typeof payload?.html === "string"
    ? payload.html
    : (getCachedPayload() || "");

initTheme();

if (initialHtml) {
    elements.htmlInput.value = initialHtml;
    updateCharCount();
}

elements.renderBtn.addEventListener("click", handleRender);
elements.clearBtn.addEventListener("click", handleClear);
elements.copyUrlBtn.addEventListener("click", copyShareableUrl);
elements.themeBtn.addEventListener("click", toggleTheme);
elements.htmlInput.addEventListener("input", handleInput);

document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        handleRender();
    }
});

window.addEventListener("hashchange", () => {
    const newPayload = decodeHashPayload();
    if (newPayload?.html) {
        elements.htmlInput.value = newPayload.html;
        updateCharCount();
        const config = mergeConfig(DEFAULT_CONFIG, newPayload.config || {});
        if (config.autoRender) {
            renderHtml(newPayload.html, config, "Rendered from hash change");
        }
    }
});

if (initialHtml && activeConfig.autoRender) {
    const source = payload ? "hash" : "cache";
    updateStatus(`Payload detected in ${source}`, "success");
    renderHtml(initialHtml, activeConfig, `Rendered from ${source}`);
}