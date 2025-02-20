const vscode = require('vscode');
const cp = require('child_process');

function activate(context) {
    let disposable = vscode.commands.registerCommand('extension.runVassFile', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage("Brak aktywnego pliku.");
            return;
        }
        const filePath = editor.document.fileName;
        if (!filePath.endsWith('.vass')) {
            vscode.window.showErrorMessage("Plik nie ma rozszerzenia .vass.");
            return;
        }
        vscode.window.showInputBox({ prompt: "Podaj ścieżkę do interpretera (znajdującego się w PATH)" }).then(interpreterPath => {
            if (!interpreterPath) {
                vscode.window.showErrorMessage("Nie podano ścieżki do interpretera.");
                return;
            }
            const command = `${interpreterPath} ${filePath}`;
            cp.exec(command, (err, stdout, stderr) => {
                if (err) {
                    vscode.window.showErrorMessage(`Błąd uruchomienia: ${stderr}`);
                    return;
                }
                vscode.window.showInformationMessage(`Wynik:\n${stdout}`);
            });
        });
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
