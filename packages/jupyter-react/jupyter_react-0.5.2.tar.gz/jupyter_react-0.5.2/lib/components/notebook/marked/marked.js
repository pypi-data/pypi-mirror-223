import { marked } from 'marked';
export const getMarked = (languages) => {
    Private.initializeMarked(languages);
    return {
        render: (content) => new Promise((resolve, reject) => {
            marked(content, (err, content) => {
                if (err) {
                    reject(err);
                }
                else {
                    resolve(content);
                }
            });
        })
    };
};
var Private;
(function (Private) {
    let markedInitialized = false;
    function initializeMarked(languages) {
        if (markedInitialized) {
            return;
        }
        else {
            markedInitialized = true;
        }
        marked.setOptions({
            gfm: true,
            sanitize: false,
            // breaks: true; We can't use GFM breaks as it causes problems with tables
            langPrefix: `language-`,
            highlight: (code, lang, callback) => {
                const cb = (err, code) => {
                    if (callback) {
                        callback(err, code);
                    }
                    return code;
                };
                if (!lang) {
                    // no language, no highlight
                    return cb(null, code);
                }
                const el = document.createElement('div');
                try {
                    languages
                        .highlight(code, languages.findBest(lang), el)
                        .then(() => {
                        return cb(null, el.innerHTML);
                    })
                        .catch(reason => {
                        return cb(reason, code);
                    });
                }
                catch (err) {
                    console.error(`Failed to highlight ${lang} code`, err);
                    return cb(err, code);
                }
            }
        });
    }
    Private.initializeMarked = initializeMarked;
})(Private || (Private = {}));
export default getMarked;
//# sourceMappingURL=marked.js.map