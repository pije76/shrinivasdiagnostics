# SimpleDropit
A simple drag-n-drop file upload vanilla js library, easy to use across modern browsers.

## 1. Documentation
### Installation
```html
<link
    rel="stylesheet"
    href="dist/css/simpledropit.min.css"
/>
<script src="dist/js/simpledropit.min.js"></script>
```
### Usage
Your input field will be

```html
<input type="file" name="files[]" id="myInput" multiple>
```

And you start SimpleDropit manually:

```js
new SimpleDropit(document.getElementById('myInput'));
```

If you want to use jQuery:

```js
new SimpleDropit($('#myInput')[0]);
```

Your input field html structure will be similar to this:
```html
<div class="sd-box">
    <div class="sd-box-wrapper">
        <div class="sd-label">
            <span class="sd-box-dragndrop">Drag &amp; Drop file or&nbsp;</span>
            <span class="sd-box-file-name"></span>
            <label class="sd-label">Browse <span class="sd-box-browse-file">File</span></label>
            <input type="file" name="files[]" id="myInput" multiple>
        </div>
    </div>
</div>
```

## 2. Browser support
SimpleDropit is tested on the following browsers: Chrome, Firefox, Safari, Edge.

:warning: **IE is not supported.**

---

## Demo
https://nishantk02.github.io/SimpleDropit/