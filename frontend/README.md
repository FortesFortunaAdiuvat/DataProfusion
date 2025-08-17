# Svelte + TypeScript Frontend

This folder contains a minimal Svelte setup compiled with Vite. The output is written directly into the Flask application's static directory so the component can be embedded in existing templates without touching existing scripts.

## Development

```
npm install
npm run dev
```

## Build

```
npm install
npm run build
```

The build step creates `app/static/js/svelte/bundle.js` which can be loaded in a Jinja template with:

```html
<div id="svelte-app"></div>
<script type="module" src="{{ url_for('static', filename='js/svelte/bundle.js') }}"></script>
```

Include `templates/svelte_component.html` where needed to render the component.
