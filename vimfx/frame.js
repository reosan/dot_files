let {utils: Cu} = Components;
let {
    isEditableInput,
    // yank_,
    // unixLineDiscard,
    cleanTagName,
    readLineCallbacks,
    READ_LINE,
} = Cu.import(`${__dirname}/shared.js`, {});

let findActiveElement = (document) => {
    let inner = (document) => {
        let active = document.activeElement;
        if (active) {
            let tag = cleanTagName(active);
            if (tag == "iframe") {
                return inner(active.contentDocument);
            }
            else {
                return active;
            }
        }
    };
    return inner(document);
};

// let readLineBinding = (name) => {
//     vimfx.listen(name, (data, cb) => {
//         let active = findActiveElement(content.document);
//         if (active && isEditableInput(active)) {
//             readLineCallbacks[name](active, data);
//         }
//     });
// };

let readLineBinding = (name) => {
    vimfx.listen(name, (data) => {
        let active = findActiveElement(content.document);
        if (active && isEditableInput(active)) {
            readLineCallbacks[name](active, data);
        }
    });
};

READ_LINE.forEach(a => {
    readLineBinding(a[0]);
});
// lineEditingBinding('yank');
// lineEditingBinding('kill_backward');
// lineEditingBinding('start_of_line');
// lineEditingBinding('end_of_line');

// sendAsyncMessage('VimFx-config:tabCreated');

// frame.js

let {sendKey} = Cu.import(`${__dirname}/shared.js`, {})

vimfx.listen('sendKey', ({key}) => {
  sendKey(content, key)
})

//sendAsyncMessage('VimFx-config:sendKey')
