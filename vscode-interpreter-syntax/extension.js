const vscode = require('vscode');

function activate(context) {
  let runFileCommand = vscode.commands.registerCommand('vass-extension.runFile', (uri) => {
    let fileUri;
    
    // Sprawdź, czy argument to instancja vscode.Uri
    if (uri instanceof vscode.Uri) {
      fileUri = uri;
    } else if (vscode.window.activeTextEditor) {
      fileUri = vscode.window.activeTextEditor.document.uri;
    } else {
      vscode.window.showErrorMessage("Brak otwartego pliku!");
      return;
    }
    
    const filePath = fileUri.fsPath;
    // Konstruujemy polecenie uruchomienia – upewnij się, że 'vass_interpreter' odpowiada Twojemu interpreterowi.
    const command = `vass_interpreter "${filePath}"`;
    
    // Szukamy terminala o stałej nazwie, aby ponownie wykorzystywać już otwarty terminal.
    let terminal = vscode.window.terminals.find(t => t.name === 'Uruchamianie pliku');
    if (!terminal) {
      terminal = vscode.window.createTerminal('Uruchamianie pliku');
    }
    terminal.show();
    terminal.sendText(command);
  });

  context.subscriptions.push(runFileCommand);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};
