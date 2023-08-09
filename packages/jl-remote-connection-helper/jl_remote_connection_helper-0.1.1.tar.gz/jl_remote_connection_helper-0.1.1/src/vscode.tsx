import React from 'react';
import { ReactWidget } from '@jupyterlab/ui-components';
import { Divider } from '@jupyter/react-components';

type Props = {
  url: string;
  token: string;
};

const VisualStudioCodeInstructions = (props: Props) => (
  <div>
    <p>
      Jupyter Server URL:{' '}
      <pre>
        {props.url}?token={props.token}
      </pre>
    </p>
    <Divider />
    <h2>Instructions</h2>
    <ol>
      <li>
        Install the{' '}
        <a
          href="https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter"
          rel="noopener noreferrer nofollow"
          target="_blank"
        >
          Jupyter extension
        </a>{' '}
        in Visual Studio Code
      </li>
      <li>
        Copy the above URL and follow{' '}
        <a
          href="https://code.visualstudio.com/docs/datascience/jupyter-notebooks#_connect-to-a-remote-jupyter-server"
          rel="noopener noreferrer nofollow"
          target="_blank"
        >
          these instructions
        </a>{' '}
        to connect to the Jupyter server
      </li>
    </ol>
  </div>
);

export class VisualStudioCodeInstructionsWidget extends ReactWidget {
  private url: string;
  private token: string;

  constructor(url: string, token: string) {
    super();
    this.url = url;
    this.token = token;
  }

  render(): JSX.Element {
    return <VisualStudioCodeInstructions url={this.url} token={this.token} />;
  }
}
