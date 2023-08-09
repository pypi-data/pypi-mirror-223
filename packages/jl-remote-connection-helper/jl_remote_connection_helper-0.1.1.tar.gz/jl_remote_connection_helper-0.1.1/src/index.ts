import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { Dialog, ICommandPalette, showDialog } from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import { LabIcon } from '@jupyterlab/ui-components';

import { requestAPI } from './handler';
import { VisualStudioCodeInstructionsWidget } from './vscode';

import vscodeIcon from '../style/vscode.svg';

type InfoResponse = {
  token: string;
};

/**
 * Initialization data for the jl-remote-connection-helper extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jl-remote-connection-helper:plugin',
  description:
    'A JupyterLab extension to help set up a remote connection to the Jupyter server.',
  autoStart: true,
  requires: [ICommandPalette],
  optional: [ILauncher],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    launcher: ILauncher | null
  ) => {
    console.log(
      'JupyterLab extension jl-remote-connection-helper is activated!'
    );

    const command = 'jl-remote-connection-helper:vscode';
    const icon = new LabIcon({
      name: 'launcher:vscode-icon',
      svgstr: vscodeIcon
    });

    app.commands.addCommand(command, {
      label: 'Connect using Visual Studio Code',
      caption: 'Connect using Visual Studio Code',
      icon: args => (args['icon'] ? icon : undefined),
      execute: async () => {
        const { token } = await requestAPI<InfoResponse>('info');
        const url = window.location.href.split('/lab')[0];
        await showDialog({
          title: 'Connect using Visual Studio Code',
          body: new VisualStudioCodeInstructionsWidget(url, token),
          buttons: [Dialog.okButton()]
        });
      }
    });

    palette.addItem({
      command,
      category: 'Remote Connection'
    });

    if (launcher) {
      launcher.add({
        command,
        category: 'Remote Connection',
        args: { icon: true }
      });
    }
  }
};

export default plugin;
