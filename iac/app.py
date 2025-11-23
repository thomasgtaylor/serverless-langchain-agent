from aws_cdk import App

from .stack import ServerlessLangChainAgentStack

app = App()
ServerlessLangChainAgentStack(app, "ServerlessLangChainAgentStack")

app.synth()
