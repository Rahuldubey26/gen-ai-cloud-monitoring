import * as vscode from 'vscode';
import axios from 'axios';

export function activate(context: vscode.ExtensionContext) {
    console.log('GenAI AWS Plugin activated');

    let disposable = vscode.commands.registerCommand('genai.awsQuery', async () => {
        console.log('Command genai.awsQuery triggered');

        const userPrompt = await vscode.window.showInputBox({ prompt: 'Enter your AWS Query (e.g., EC2 in us-east-1)' });
        if (!userPrompt) {
            vscode.window.showInformationMessage('No input provided.');
            return;
        }

        try {
            const res = await axios.post('http://localhost:8000/query', { prompt: userPrompt });
            vscode.window.showInformationMessage('GenAI Response: ' + JSON.stringify(res.data.genai_analysis));
            console.log('Response from backend:', res.data);
        } catch (error) {
            vscode.window.showErrorMessage('Error fetching GenAI response.');
            console.error('Error:', error);
        }
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
