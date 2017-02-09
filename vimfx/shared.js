const EXPORTED_SYMBOLS = [
    'isEditableInput',
    // 'yank_',
    // 'unixLineDiscard',
    'cleanTagName',
    'readLineCallbacks',
    'readLineDataCallbacks',
    'READ_LINE',
];

var READ_LINE = [
    ['forward_char', '<c-f>'],
    ['backward_char', '<c-b>'],
    // ['next_history', '<c-n>'],
    // ['previous_history', '<c-p>'],
    ['delete_char', '<c-d>'],
    ['backward_delete_char', '<c-h>'],
    ['kill_line', '<c-k>'],
    ['yank', '<c-y>'],
    ['unix_line_discard', '<c-u>'],
    //    ['unix_word_rubout', '<c-w>'],
    ['beginning_of_line', '<c-a>'],
    ['end_of_line', '<c-e>'],
]

var readLineCallbacks = {
    'forward_char': (input, data) => {
	forwardChar(input);
    },
    'backward_char': (input, data) => {
	backwardChar(input);
    },
    'next_history':(input, data) => {
        nextHistory(input);
    },
    'previous_history': (input, data) => {
        previousHistory(input);
    },
    'delete_char': (input, data) => {
	deleteChar(input);
    },
    'backward_delete_char': (input, data) => {
	backwardDeleteChar(input);
    },
    'kill_line': (input) => {
	killLine(input);
    },
    'yank': (input, data) => {
        yank_(input, data);
    },
    'unix_line_discard': (input, data) => {
        unixLineDiscard(input);
    },
    // 'unix_word_rubout': (input, data) => {
    // 	unixWordRubout(input);
    // },
    'beginning_of_line': (input, data) => {
        beginningOfLine(input);
    },
    'end_of_line': (input, data) => {
        endOfLine(input);
    },
};

var readLineDataCallbacks = {
    'yank': (vim) => {
        return vim.window.readFromClipboard();
    },
};

function forwardChar(e) {
    e.selectionStart = e.selectionEnd =
	e.selectionEnd == e.value.length ? e.value.length : e.selectionEnd + 1;
}

function backwardChar(e) {
    e.selectionStart = e.selectionEnd =
	e.selectionStart == 0 ? 0 : e.selectionStart - 1;
}

function nextHistory(e) {
    console.log('dummy');
}

function previousHistory(e) {
    console.log('dummy');
}

function deleteChar(e) {
    var before = e.value.substring(0, e.selectionStart);
    var after = e.value.substring(e.selectionEnd, e.value.length);
    after && e.selectionStart == e.selectionEnd && (after =  after.substring(1, after.length));
    e.value = before + after;
    e.selectionStart = e.selectionEnd = before.length;
}

function backwardDeleteChar(e) {
    var before = e.value.substring(0, e.selectionStart);
    var after = e.value.substring(e.selectionEnd, e.value.length);
    before && e.selectionStart == e.selectionEnd && (before =  before.substring(0, before.length - 1));
    e.value = before + after;
    e.selectionStart = e.selectionEnd = before.length;
}

function killLine(e) {
    var before = e.value.substring(0, e.selectionStart);
    var after = e.value.substring(e.selectionEnd, e.value.length);
    var start = after.indexOf('\n') + 1 || after.length;
    after = after.substring(start, after.length);
    e.value = before + after;
    e.selectionStart = e.selectionEnd = before.length;
}

function yank_(e, text) {
    text = text || "";
    var before = e.value.substring(0, e.selectionStart);
    var after = e.value.substring(e.selectionEnd, e.value.length);
    e.value = before + text + after;
    e.selectionStart = e.selectionEnd = before.length + text.length;
}

function unixLineDiscard(e) {
    var before = e.value.substring(0, e.selectionStart);
    var start = before.lastIndexOf('\n') + 1;
    before = before.substring(0, start);
    var after = e.value.substring(e.selectionEnd, e.value.length);
    e.value = before + after;
    e.selectionStart = e.selectionEnd = start;
}

// function unixWordRubout(e) {
// }

function beginningOfLine(e) {
    var start = e.value.lastIndexOf('\n', e.selectionStart) + 1;
    e.selectionStart = e.selectionEnd = start;
}

function endOfLine(e) {
    var end = e.value.indexOf('\n', e.selectionEnd) + 1;
    if (end === 0) {
        end = e.value.length;
    }
    e.selectionStart = e.selectionEnd = end;
}

function cleanTagName(e) {
    return e.tagName.split(':').pop().toLowerCase();
}

function isEditableInput(e) {
    let tag = cleanTagName(e);
    // XXX
    return tag == "input" || tag == "textarea";
}
