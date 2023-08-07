import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useRef, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { basicSetup } from 'codemirror';
import { EditorState, Compartment } from '@codemirror/state';
import { keymap, EditorView } from '@codemirror/view';
import { python } from '@codemirror/lang-python';
import codeMirrorTheme from './CodeMirrorTheme';
import CodeMirrorOutputToolbar from './CodeMirrorOutputToolbar';
import { selectDataset, selectJupyterSetSource, outputActions } from '../output/OutputState';
export const CodeMirrorEditor = (props) => {
    const { code, codePre, outputAdapter, autoRun, disableRun, sourceId, toolbarPosition, insertText, kernel } = props;
    const dispatch = useDispatch();
    const [view, setView] = useState();
    const dataset = selectDataset(sourceId);
    const setSource = selectJupyterSetSource(sourceId);
    const editorDiv = useRef();
    const setEditorSource = (source) => {
        if (view && source) {
            view.dispatch({
                changes: {
                    from: 0,
                    to: view.state.doc.length,
                    insert: source,
                }
            });
        }
    };
    const doInsertText = (payload) => {
        if (view && insertText) {
            view.dispatch({
                changes: {
                    from: 0,
                    insert: insertText(payload)
                }
            });
        }
    };
    const executeCode = (editorView, code) => {
        if (disableRun) {
            alert('Code execution is disabled for this editor. There should be a button on the page to run this editor.');
            return true;
        }
        if (code) {
            outputAdapter.execute(code);
        }
        else {
            outputAdapter.execute(editorView.state.doc.toString());
        }
        return true;
    };
    useEffect(() => {
        dispatch(outputActions.source({
            sourceId,
            source: code,
        }));
        let editorView;
        const language = new Compartment();
        const keyBinding = [
            {
                key: 'Shift-Enter',
                run: () => executeCode(editorView),
                preventDefault: true,
            },
        ];
        const state = EditorState.create({
            doc: code,
            extensions: [
                basicSetup,
                language.of(python()),
                EditorView.lineWrapping,
                keymap.of([...keyBinding]),
                codeMirrorTheme,
                EditorView.updateListener.of((viewUpdate) => {
                    if (viewUpdate.docChanged) {
                        const source = viewUpdate.state.doc.toString();
                        dispatch(outputActions.source({
                            sourceId,
                            source,
                        }));
                    }
                })
            ],
        });
        editorView = new EditorView({
            state: state,
            parent: editorDiv.current,
        });
        setView(editorView);
        if (autoRun) {
            executeCode(editorView);
        }
        return () => {
            editorView.destroy();
        };
    }, [code]);
    useEffect(() => {
        doInsertText(dataset?.dataset);
    }, [dataset]);
    useEffect(() => {
        setEditorSource(setSource?.source);
    }, [setSource]);
    return (_jsxs(_Fragment, { children: [kernel && toolbarPosition === 'up' &&
                _jsx(CodeMirrorOutputToolbar, { editorView: view, codePre: codePre, kernel: kernel, outputAdapter: outputAdapter, executeCode: executeCode }), _jsx("div", { ref: editorDiv }), kernel && toolbarPosition === 'middle' &&
                _jsx(CodeMirrorOutputToolbar, { editorView: view, codePre: codePre, kernel: kernel, outputAdapter: outputAdapter, executeCode: executeCode })] }));
};
export default CodeMirrorEditor;
//# sourceMappingURL=CodeMirrorEditor.js.map