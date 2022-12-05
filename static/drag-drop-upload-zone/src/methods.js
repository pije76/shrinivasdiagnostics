export default class SimpleDropitMethods {
    constructor() {}

    static isFiles(arg) {
        let r = false;
        if (arg.types === undefined && arg.files) {
            for(const [index, file] of Object.entries(arg.files)) {
                if(file.name !== '') {
                    r = true;
                }
            }
        } else {
            arg.types.forEach((file, index) => {
                if(file === "Files" || file === "application/x-moz-file") {
                    r = true;
                }
            });
        }
        return r;
    }
}