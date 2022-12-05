// Helper functions
export function getElementDocument(element) {
    if (!element || !element.ownerDocument) {
        return document;
    }  
    return element.ownerDocument;
}

export function hasClass(element, className) {
    if(element) {
        return element.classList.contains(className);
    } else {
        return null;
    }
}

export function triggerClick(element) {
    if(element.click) {
        element.click();
    } else if(document.createEvent) {
        var eventObj = document.createEvent('MouseEvents');
        eventObj.initEvent('click', true, true);
        element.dispatchEvent(eventObj);
    }
}