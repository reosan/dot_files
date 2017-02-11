let {commands} = vimfx.modes.normal;

const {classes: Cc, interfaces: Ci, utils: Cu} = Components;
const mm = Cc['@mozilla.org/globalmessagemanager;1']
    .getService(Ci.nsIMessageListenerManager);

let {
    isEditableInput,
    cleanTagName,
    // yank_,
    // unixLineDiscard,
    readLineCallbacks,
    readLineDataCallbacks,
    READ_LINE,
} = Cu.import(`${__dirname}/shared.js`, {});

vimfx.on('modeChange', ({vim}) => {
  let mode = vimfx.modes[vim.mode].name
  vim.notify(`Entering mode: ${mode}`) // 通知
})

let {Preferences} = Cu.import('resource://gre/modules/Preferences.jsm', {});
Preferences.set({
    'browser.urlbar.maxRichResults': 10,
    'dom.popup_allowed_events': '',
    'extensions.VimFx.config_file_directory': '~/dot_files/vimfx',
    // 'dom.popup_maximum': 20,
    // 'dom.ipc.processCount': 1,

    //     'accessibility.typeaheadfind.enablesound': false,
    //     'devtools.chrome.enabled': true,
    //     'privacy.donottrackheader.enabled': true,
    //     'toolkit.scrollbox.verticalScrollDistance': 1,
});

const CUSTOM_COMMANDS = [
    [{	name: 'pocket',
	description: 'Save to Pocket',
	category: 'misc',
     },{	 key: ',s',
		 func: ({vim}) => { vim.window.document.getElementById('pocket-button').click(); },
       }],
    [{	name: 'open_about_config',
	description: 'open about:config',
	category: 'misc',
     },{	 key: ',c',
		 func: ({vim}) => { vim.window.open('about:config'); },
       }],
    [{	name: 'open_about_addons',
	    description: 'open about:addons',
	    category: 'misc',
     },{	 key: ',a',
		     func: ({vim}) => { vim.window.open('about:addons'); },
       }],
];

const SHORTCUTS = [
    // shortcuts =
    //   'normal':
    //     'location':
    //       'o':         'focus_location_bar'
    //       'O':         'focus_search_bar'
    //       'p':         'paste_and_go'
    //       'P':         'paste_and_go_in_tab'
    //       'yy':        'copy_current_url'
    //       'gu':        'go_up_path'
    //       'gU':        'go_to_root'
    //       'gh':        'go_home'
    //       'H':         'history_back'
    //       'L':         'history_forward'
    //       'gH':        'history_list'
    //       'r':         'reload'
    //       'R':         'reload_force'
    //       'ar':        'reload_all'
    //       'aR':        'reload_all_force'
    //       's':         'stop'
    //       'as':        'stop_all'

    //     'scrolling':
    //       'h':         'scroll_left'
    //       'l':         'scroll_right'
    ['scroll_left', '<c-H>'],
    ['scroll_right', '<c-L>'],
    //       'j':         'scroll_down'
    //       'k':         'scroll_up'
    ////['scroll_down', 'j  <force><c-n>'],
    ////['scroll_up', 'k  <force><c-p>'],
    //       '<space>':   'scroll_page_down'
    //       '<s-space>': 'scroll_page_up'
    //       'd':         'scroll_half_page_down'
    //       'u':         'scroll_half_page_up'
    //       'gg':        'scroll_to_top'
    //       'G':         'scroll_to_bottom'
    //       '0  ^':      'scroll_to_left'
    //       '$':         'scroll_to_right'
    //       'm':         'mark_scroll_position'
    //       "'":         'scroll_to_mark'
    //       'g[':        'scroll_to_previous_position'
    //       'g]':        'scroll_to_next_position'

    //     'tabs':
    //       't':         'tab_new'
    //       'T':         'tab_new_after_current'
    //       'yt':        'tab_duplicate'
    //       'J    gT':   'tab_select_previous'
    //       'K    gt':   'tab_select_next'
    ['tab_select_previous', 'h'],
    ['tab_select_next', 'l'],
    //       'gl':        'tab_select_most_recent'
    //       'gL':        'tab_select_oldest_unvisited'
    //       'gJ':        'tab_move_backward'
    //       'gK':        'tab_move_forward'
    //       'gw':        'tab_move_to_window'
    //       'g0':        'tab_select_first'
    //       'g^':        'tab_select_first_non_pinned'
    //       'g$':        'tab_select_last'
    //       'gp':        'tab_toggle_pinned'
    //       'x':         'tab_close'
    //       'X':         'tab_restore'
    //       'gX':        'tab_restore_list'
    //       'gx$':       'tab_close_to_end'
    //       'gxa':       'tab_close_other'

    //     'browsing':
    //       'f':         'follow'
    //       'F':         'follow_in_tab'
    //       'et':        'follow_in_focused_tab'
    ['follow_in_tab', 'et'],
    ['follow_in_focused_tab', 'F'],
    //       'ew':        'follow_in_window'
    //       'ep':        'follow_in_private_window'
    //       'af':        'follow_multiple'
    //       'yf':        'follow_copy'
    //       'ef':        'follow_focus'
    //       'ec':        'open_context_menu'
    //       'eb':        'click_browser_element'
    //       '[':         'follow_previous'
    //       ']':         'follow_next'
    //       'gi':        'focus_text_input'
    //       'v':         'element_text_caret'
    //       'av':        'element_text_select'
    //       'yv':        'element_text_copy'

    //     'find':
    //       '/':         'find'
    //       'a/':        'find_highlight_all'
    //       'g/':        'find_links_only'
    //       'n':         'find_next'
    //       'N':         'find_previous'

    //     'misc':
    //       'w':         'window_new'
    //       'W':         'window_new_private'
    //       'i':         'enter_mode_ignore'
    //       'I':         'quote'
    //       'gr':        'enter_reader_view'
    //       'gB':        'edit_blacklist'
    //       'gC':        'reload_config_file'
    //       '?':         'help'
    //       ':':         'dev'
    //       '<force><escape>': 'esc'

    //   'caret':
    //     '':
    //       'h':         'move_left'
    //       'l':         'move_right'
    //       'j':         'move_down'
    //       'k':         'move_up'
    //       'b':         'move_word_left'
    //       'w':         'move_word_right'
    //       '0    ^':    'move_to_line_start'
    //       '$':         'move_to_line_end'
    //       'v':         'toggle_selection'
    //       'o':         'toggle_selection_direction'
    //       'y':         'copy_selection_and_exit'
    //       '<escape>':  'exit'

    //   'hints':
    //     '':
    //       '<escape>':        'exit'
    //       '<enter>    \
    //        <c-enter>    \
    //        <a-enter>':       'activate_highlighted'
    //       '<c-space>':       'rotate_markers_forward'
    //       '<s-space>':       'rotate_markers_backward'
    //       '<backspace>':     'delete_char'
    //       '<c-backspace>':   'toggle_complementary'
    //       '<up>':            'increase_count'

    //   'ignore':
    //     '':
    //       '<s-escape>':      'exit'
    //       '<s-f1>':          'unquote'

    //   'find':
    //     '':
    //       '<escape>    <enter>': 'exit'

    //   'marks':
    //     '':
    //       '<escape> ':       'exit'
];

const OPTIONS = [
    // options =
    //   'prevent_autofocus':      false
    ['prevent_autofocus', true],
    //   'ignore_keyboard_layout': false
    //   'blacklist':              '*example.com*  http://example.org/editor/*'
    //   'hints.chars':            'fjdkslaghrueiwonc mv'
    //   'hints.auto_activate':    true
    //   'hints.timeout':          400
    //   'timeout':                2000
    //   'prev_patterns':          'prev  previous  ‹  «  ◀  ←  <<  <  back  newer'
    //   'next_patterns':          'next  ›  »  ▶  →  >>  >  more  older'

    // advanced_options =
    //   'notifications_enabled':              true
    //   'notify_entered_keys':                true
    //   'prevent_target_blank':               true
    //   'counts_enabled':                     true
    //   'find_from_top_of_viewport':          true
    //   'browsewithcaret':                    false
    //   'ignore_ctrl_alt':                    (Services.appinfo.OS == 'WINNT')
    //   'prevent_autofocus_modes':            'normal'
    //   'config_file_directory':              ''
    //   'blur_timeout':                       50
    //   'refocus_timeout':                    100
    //   'smoothScroll.lines.spring-constant': '1000'
    //   'smoothScroll.pages.spring-constant': '2500'
    //   'smoothScroll.other.spring-constant': '2500'
    //   'scroll.reset_timeout':               1000
    //   'scroll.repeat_timeout':              65
    //   'scroll.horizontal_boost':            6
    //   'scroll.vertical_boost':              3
    //   'scroll.full_page_adjustment':        40
    //   'scroll.half_page_adjustment':        20
    //   'scroll.last_position_mark':          "'"
    //   'scroll.last_find_mark':              '/'
    //   'pattern_selector':                   ':-moz-any(
    //                                            a, button, input[type="button"]
    //                                          ):not([role="menu"]):not([role="tab"])'
    //   'pattern_attrs':                      'rel  role  data-tooltip  aria-label'
    //   'hints.matched_timeout':              200
    //   'hints.sleep':                        15
    //   'hints.match_text':                   true
    //   'hints.peek_through':                 '<c-s->'
    //   'hints.toggle_in_tab':                '<c-'
    //   'hints.toggle_in_background':         '<a-'
    //   'activatable_element_keys':           '<enter>'
    //   'adjustable_element_keys':            '<arrowup>  <arrowdown>  <arrowleft>
    //                                          <arrowright>  <space>  <enter>'
    //   'focus_previous_key':                 '<s-tab>'
    //   'focus_next_key':                     '<tab>'
    //   'options.key.quote':                  '<c-q>'
    //   'options.key.insert_default':         '<c-d>'
    //   'options.key.reset_default':          '<c-r>'

    // parsed_options =
    //   'translations': {}
    //   'categories':   {} # Will be filled in below.

    // # The above easy-to-read data is transformed in to easy-to-consume (for
    // # computers) formats below.

    // # coffeelint: enable=colon_assignment_spacing
    // # coffeelint: enable=no_implicit_braces

    // translate = require('./translate')
    // utils = require('./utils')

    // addCategory = (category, order) ->
    //   uncategorized = (category == '')
    //   categoryName = if uncategorized then '' else translate("category.#{category}")
    //   parsed_options.categories[category] = {
    //     name: categoryName
    //     order: if uncategorized then 0 else order
    //   }

    // shortcut_prefs = {}
    // categoryMap = {}
    // mode_order = {}
    // command_order = {}

    // createCounter = -> new utils.Counter({step: 100})
    // modeCounter = createCounter()
    // categoryCounter = createCounter()

    // for modeName, modeCategories of shortcuts
    //   mode_order[modeName] = modeCounter.tick()
    //   for categoryName, modeShortcuts of modeCategories
    //     addCategory(categoryName, categoryCounter.tick())
    //     commandIndex = createCounter()
    //     for shortcut, commandName of modeShortcuts
    //       pref = "mode.#{modeName}.#{commandName}"
    //       shortcut_prefs[pref] = shortcut
    //       command_order[pref] = commandIndex.tick()
    //       categoryMap[pref] = categoryName

    // # All options, excluding shortcut customizations.
    // all_options = Object.assign({}, options, advanced_options, parsed_options)
    // # All things that are saved in Firefox’s prefs system.
    // all_prefs   = Object.assign({}, options, advanced_options, shortcut_prefs)

    // module.exports = {
    //   options
    //   advanced_options
    //   parsed_options
    //   all_options
    //   shortcut_prefs
    //   all_prefs
    //   categoryMap
    //   mode_order
    //   command_order
    //   BRANCH: 'extensions.VimFx.'
    // }
];

let categories = vimfx.get('categories');
categories.insert = {
    name: '.inputrc',
    order: categories.misc.order - 1,
};

let readLineBinding = (opts) => {
    opts.category = 'insert';
    vimfx.addCommand(
        opts,
        ({vim}) => {
            let cb = readLineCallbacks[opts.name];
            let data_cb = readLineDataCallbacks[opts.name];
            let data = data_cb ? data_cb(vim) : null;
            let active = vim.window.document.activeElement;
            if (active && isEditableInput(active)) {
                cb(active, data);
            }
            else {
                vimfx.send(vim, opts.name, data, null);
            }
        }
    );
};

READ_LINE.forEach(a => {
    ((name, key) => {
	readLineBinding({
	    name: name,
	    description: name.replace(/_/g, '-'),
	});
	vimfx.set(`custom.mode.normal.${name}`, `<force>${key}`);
    })(a[0], a[1]);
});

SHORTCUTS.forEach(a => {
    ((name, key) => {
	vimfx.set(`mode.normal.${name}`, key);
    })(a[0], a[1]);
});

OPTIONS.forEach(a => {
    ((name, key) => {
	vimfx.set(name, key);
    })(a[0], a[1]);
});

CUSTOM_COMMANDS.forEach(a => {
    vimfx.addCommand(a[0],a[1]['func']);
    vimfx.set(`custom.mode.normal.${a[0]['name']}`, a[1]['key']);
});


let {sendKey} = Cu.import(`${__dirname}/shared.js`, {})

// vimfx.addCommand({
//     name: 'send_up',
//     description: 'Send the <up> key',
//     category: 'insert',
// }, helper_send_key.bind(null, 'up'));
// vimfx.set('custom.mode.normal.send_up', '<force><c-p>');

vimfx.addCommand({
    name: 'send_up',
    description: 'Send the <up> key',
    category: 'insert',
}, double_send_key.bind(null, 'up'));
vimfx.set('custom.mode.normal.send_up', '<force><c-p>');

vimfx.addCommand({
    name: 'send_down',
    description: 'Send the <down> key',
    category: 'insert',
}, double_send_key.bind(null, 'down'));
vimfx.set('custom.mode.normal.send_down', '<force><c-n>');

function double_send_key(key, {vim, uiEvent}) {
    helper_send_key(key, {vim, uiEvent});
    url_send_key(key, {vim});
}

function helper_send_key(key, {vim, uiEvent}) {
    if (uiEvent) {
        sendKey(vim.window, key)
    } else {
        vimfx.send(vim, 'sendKey', {key})
    }
}

function url_send_key(key, {vim}) {
    var u = vim.window.document.activeElement;
    //    if(isEditableInput(cleanTagName(u))){
    if(true){
        ['keydown', 'keypress', 'keyup'].forEach(name => {
            var event = new vim.window.KeyboardEvent(name, {
                get keyCode(){return key == 'up' ? 38 : 40;},
            });
            u.dispatchEvent(event);
        });
    }
}

// vimfx.addCommand({
//     name: 'pocket',
//     description: 'Save to Pocket',
// }, ({vim}) => {
//     vim.window.document.getElementById('pocket-button').click();
// });
// vimfx.set('custom.mode.normal.pocket', 's');

// vimfx.addCommand({
//     name: 'open_about_config',
//     description: 'open about:config',
// }, ({vim}) => {
//     vim.window.open('about:config');
// });
// vimfx.set('custom.mode.normal.open_about_config', ',c');

// vimfx.set('mode.normal.focus_search_bar', '');
// vimfx.set('mode.normal.copy_current_url', 'y');
// vimfx.set('mode.normal.history_back', '<force><C-h>');
// vimfx.set('mode.normal.history_forward', '<force><C-l>');
// vimfx.set('mode.normal.stop', '<force><C-c>');

// vimfx.set('mode.normal.scroll_half_page_down', 'J');
// vimfx.set('mode.normal.scroll_half_page_up', 'K');
// vimfx.set('mode.normal.scroll_to_left', '0 ) _');
// vimfx.set('mode.normal.scroll_to_mark', '\'');

// vimfx.set('mode.normal.tab_new_after_current', '');
// vimfx.set('mode.normal.tab_select_previous', 'H');
// vimfx.set('mode.normal.tab_select_next', 'L');
// vimfx.set('mode.normal.tab_close', 'd');
// vimfx.set('mode.normal.tab_restore', 'u');

// vimfx.set('mode.normal.quote', '<force><C-v>');
// vimfx.set('mode.normal.enter_mode_ignore', '<force><C-z>');
// vimfx.set('mode.normal.dev', ': ,');

// vimfx.set('notify_entered_keys', true);
// vimfx.set('scroll.last_position_mark', '\'');

// let new_tab_url = null;
// (function () {
//     let onTabCreated = ({target: browser}) => {
//         if (new_tab_url) {
//             browser.ownerGlobal.gURLBar.value = new_tab_url;
//             new_tab_url = null;
//         }
//     };
//     mm.addMessageListener('VimFx-config:tabCreated', onTabCreated);
//     vimfx.on('shutdown', () => {
//         mm.removeMessageListener('VimFx-config:tabCreated', onTabCreated);
//     });

//     vimfx.addCommand({
//         name: 'tab_new_with_url',
//         description: 'New tab with URL',
//         category: 'tabs',
//         order: commands.tab_new_after_current.order + 1,
//     }, (args) => {
//         new_tab_url = args.vim.browser.currentURI.spec;
//         commands.tab_new.run(args);
//     });
//     vimfx.set('custom.mode.normal.tab_new_with_url', 'T');
// })();

// vimfx.addCommand({
//     name: 'tab_groups',
//     description: 'Toggle tab groups',
//     category: 'tabs',
// }, ({vim}) => {
//     vim.window.tabGroups.TabView.toggle();
// });
// vimfx.set('custom.mode.normal.tab_groups', '<BS>');

// vimfx.addCommand({
//     name: 'goto_tab',
//     description: 'Goto tab',
//     category: 'tabs',
// }, (args) => {
//     commands.focus_location_bar.run(args);
//     args.vim.window.gURLBar.value = '% ';
// });
// vimfx.set('custom.mode.normal.goto_tab', 'b');

// vimfx.addCommand({
//     name: 'focus_unhighlighted_location_bar',
//     description: 'Focus the location bar with the URL unhighlighted',
//     category: 'location',
//     order: commands.focus_location_bar.order + 1,
// }, (args) => {
//     commands.focus_location_bar.run(args);
//     let active = args.vim.window.document.activeElement;
//     active.selectionStart = active.selectionEnd;
// });
// vimfx.set('custom.mode.normal.focus_unhighlighted_location_bar', 'O');



// // config - based on
// const {classes: Cc, interfaces: Ci, utils: Cu} = Components
// Cu.import("resource://gre/modules/XPCOMUtils.jsm")
// XPCOMUtils.defineLazyModuleGetter(this, "Preferences", "resource://gre/modules/Preferences.jsm")
// const gClipboardHelper = Cc["@mozilla.org/widget/clipboardhelper;1"].getService(Ci.nsIClipboardHelper);
// // override default settings
// Preferences.set({
//     "devtools.chrome.enabled" : true,
//     "browser.urlbar.filter.javascript" : false,           // bookmarklet を使うのに必要
//     "findbar.modalHighlight": false,
//     "findbar.highlightAll": false,
// });
// // helper functions
// let {commands} = vimfx.modes.normal
// let set = (pref, valueOrFunction) => {
//     let value = typeof valueOrFunction === "function"
//         ? valueOrFunction(vimfx.getDefault(pref))
//         : valueOrFunction
//     vimfx.set(pref, value)
// }
// let map = (shortcuts, command, custom=false) => {
//     vimfx.set(`${custom ? "custom." : ""}mode.normal.${command}`, shortcuts)
// }
// // options
// set("prevent_autofocus", true)
// set("mode.normal.copy_current_url", "y");
// // custom command
// vimfx.addCommand({
//     name: "goto_addons",
//     description: "Addons",
// }, ({vim}) => {
//     vim.window.BrowserOpenAddonsMgr()
// })
// map(",a", "goto_addons", true)
// //
// vimfx.addCommand({
//     name: "goto_preferences",
//     description: "Preferences",
// }, ({vim}) => {
//     vim.window.openPreferences()
// })
// map(",p", "goto_preferences", true)
// //
// vimfx.addCommand({
//     name: "goto_downloads",
//     description: "Downloads",
// }, ({vim}) => {
//     vim.window.DownloadsPanel.showDownloadsHistory()
// })
// map(",d", "goto_downloads", true)
// //
// vimfx.addCommand({
//     name: "goto_config",
//     description: "Config",
// }, ({vim}) => {
//     vim.window.switchToTabHavingURI("about:config", true)
// })
// map(",c", "goto_config", true)
// //
// vimfx.addCommand({
//     name: "search_bookmarks",
//     description: "Search bookmarks",
//     order: commands.focus_location_bar.order + 1,
// }, (args) => {
//     let {vim} = args
//     let {gURLBar} = vim.window
//     gURLBar.value = ""
//     commands.focus_location_bar.run(args)
//     gURLBar.value = "* "
//     gURLBar.onInput(new vim.window.KeyboardEvent("input"))
// })
// map("b", "search_bookmarks", true)
// //
// vimfx.addCommand({
//     name: "copy_org",
//     description: ""[[URL][title]]"でURLコピー",
//     category: "location",
// }, ({vim}) => {
//     let url = vim.window.gBrowser.selectedBrowser.currentURI.spec
//     let title = vim.window.gBrowser.selectedBrowser.contentTitle
//     let fmt = "[["+url+"]["+title+"]]"
//     gClipboardHelper.copyString(fmt)
//     vim.notify("Copied String: "+ fmt)
// })
// map("co", "copy_org", true)
// //
// vimfx.addCommand({
//     name: "copy_rd",
//     description: ""((<"title"|URL:URL>))"でURLコピー",
//     category: "location",
// }, ({vim}) => {
//     let url = vim.window.gBrowser.selectedBrowser.currentURI.spec
//     let title = vim.window.gBrowser.selectedBrowser.contentTitle
//     let fmt = "((<\""+title+"\"|URL:"+url+">))"
//     gClipboardHelper.copyString(fmt)
//     vim.notify("Copied String: "+ fmt)
// })
// map("cr", "copy_rd", true)
// //
// vimfx.addCommand({
//     name: "foxyproxy_click_toolbar_button",
//     description: "FoxyProxy",
// }, ({vim}) => {
//     vim.window.document.getElementById("foxyproxy-toolbar-icon").click()
// })
// map(".p", "foxyproxy_click_toolbar_button", true)
