import {getElementDocument, hasClass, triggerClick } from './helpers';
import SimpleDropitMethods from './methods';

class SimpleDropit extends SimpleDropitMethods {

    /**
     * SimpleDropit Object
     * @param {String} selector Element object
     * @param {Object} options User options
     */
    constructor(selector, options) {
        super();
        try {
            if(typeof selector === 'string') {
                throw new Error('Invalid Element Object');
            } else if(typeof selector === 'object' && selector !== null) {
                this.el = selector;
            } else {
                throw new Error('Element Object does not exists');
            }
        } catch(error) {
            console.error(error.name + ': ' + error.message);
            return;
        }

        this.options = { ...SimpleDropit.defaultOptions, ...options };
        this.classNames = {
            ...SimpleDropit.defaultOptions.classNames,
            ...this.options.classNames
        };

        if (SimpleDropit.instances.has(this.el)) {
            return;
        }
        this.init();
    }

    isAdvancedUpload = () => {
        var div = document.createElement('div');
        return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
    };

    onChange = (event) => {
        if(!SimpleDropit.isFiles(event.target)) {
            return;
        }
        SimpleDropit.showFiles(this.filenameEl, event.target.files)
        this.boxEl.classList.add('is-dropped');
    };

    dragIn = (event) => {
        // Check the dragged elements are Files
        if(!SimpleDropit.isFiles(event.dataTransfer)) {
            return;
        }
        if(!hasClass(this.boxEl, 'is-dragover')) this.boxEl.classList.add('is-dragover');
    };

    dragOut = (event) => {
        // Check the dragged elements are Files
        if(!SimpleDropit.isFiles(event.dataTransfer)) {
            return;
        }
        if(hasClass(this.boxEl, 'is-dragover')) this.boxEl.classList.remove('is-dragover');
    };

    drop = (event) => {
        // Check the dropped elements are Files
        if(!SimpleDropit.isFiles(event.dataTransfer)) {
            return;
        }
        
        this.droppedFiles = event.dataTransfer.files;
        SimpleDropit.showFiles(this.filenameEl, this.droppedFiles);
        this.boxEl.classList.add('is-dropped');
    };

    preventEventPropagation = (event) => {
        event.preventDefault();
        event.stopPropagation();
    };

    static instances = new WeakMap();

    init() {
        // Save a reference to the instance, so we know this DOM node has already been instanciated
        SimpleDropit.instances.set(this.el, this);

        this.initDom();
        this.initListeners();
    }

    initDom() {

        // Assuring this element doesn't have the wrapper elements yet
        if(this.el.closest('.' + this.classNames.boxEl) !== null) {
            // Assume that element has his DOM already initiated
            this.boxEl = this.el.closest('.' + this.classNames.boxEl);
            this.boxWrapperEl = this.boxEl.querySelector('.' + this.classNames.boxWrapperEl);
            this.labelWrapperEl = this.boxEl.querySelector('.' + this.classNames.labelWrapperEl);
            this.supportedLabelEl = this.boxEl.querySelector('.' + this.classNames.supportedLabelEl);
            this.filenameEl = this.boxEl.querySelector('.' + this.classNames.filenameEl);
            this.browseLabelEl = this.boxEl.querySelector('.' + this.classNames.browseLabelEl);
        } else {
            // Prepare DOM
            const elClone = this.el.cloneNode(true);

            this.boxEl = document.createElement('div');
            this.boxWrapperEl = document.createElement('div');
            this.labelWrapperEl = document.createElement('div');
            this.supportedLabelEl = document.createElement('span');
            this.filenameEl = document.createElement('span');
            this.browseLabelEl = document.createElement('label');

            this.boxEl.classList.add(this.classNames.boxEl);
            this.boxWrapperEl.classList.add(this.classNames.boxWrapperEl);
            this.labelWrapperEl.classList.add(this.classNames.labelWrapperEl);
            this.supportedLabelEl.classList.add(this.classNames.supportedLabelEl);
            this.filenameEl.classList.add(this.classNames.filenameEl);
            this.browseLabelEl.classList.add(this.classNames.browseLabelEl);

            this.el.classList.add('sd-file-input', 'sd-file-input-hide');

            this.supportedLabelEl.innerHTML = this.options.supportedLabel+'&nbsp;';
            this.labelWrapperEl.appendChild(this.supportedLabelEl);
            this.labelWrapperEl.appendChild(this.filenameEl);
            this.browseLabelEl.innerHTML = 'Browse <span class="sd-box-browse-file">File</span></span>';
            this.labelWrapperEl.appendChild(this.browseLabelEl);
            this.labelWrapperEl.appendChild(elClone);
            this.boxWrapperEl.appendChild(this.labelWrapperEl);
            this.boxEl.appendChild(this.boxWrapperEl);

            this.el.after(this.boxEl);
            
            this.el.remove();
            this.el = elClone;
        }

        if(this.isAdvancedUpload) {
            this.boxEl.classList.add('sd-advanced-upload');
        }
    }

    initListeners() {
        ['drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop'].forEach(e => {
            getElementDocument(this.boxEl).addEventListener(e, this.preventEventPropagation, false);
            this.boxEl.addEventListener(e, this.preventEventPropagation, false);
        });
        ['dragenter', 'dragover'].forEach(e => {
            getElementDocument(this.boxEl).addEventListener(e, this.dragIn, true);
        });
        ['dragleave', 'drop'].forEach(e => {
            getElementDocument(this.boxEl).addEventListener(e, this.dragOut, true);
        });
        this.boxEl.addEventListener('drop', this.drop, true);
        this.el.addEventListener('change', this.onChange, true);
        this.browseLabelEl.addEventListener('click', event => { triggerClick(this.el); });
    }

    static showFiles(el, files) {
        let fileName = files[0].name;

        if(fileName !== '' && fileName !== undefined) {
            el.innerText = files.length > 1 ? (files.length + ' files selected / ') : fileName + ' / ';
            return true;
        } else {
            return false;
        }
    }

    static defaultOptions = {
        classNames: {
            boxEl: 'sd-box',
            boxWrapperEl: 'sd-box-wrapper',
            browseLabelEl: 'sd-label',
            filenameEl: 'sd-box-file-name',
            labelWrapperEl: 'sd-label-wrapper',
            supportedLabelEl: 'sd-box-dragndrop',
        },
        supportedLabel: 'Drop file here /',
    };
}

export default SimpleDropit;