import argparse
import json
from cgi import print_exception
import datetime
import hjson
import re
from ast import literal_eval
from typing import Union

import libcst as cst
from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand
from libcst.metadata import ParentNodeProvider


# TODO: support all different form options
def parse_colab_form_param(param_comment):
    _, left_of_param = param_comment.split("@param")
    configObject = None
    configChoices = None
    if "{" in left_of_param:
        configObject = hjson.loads(
            left_of_param[left_of_param.index("{") : left_of_param.index("}") + 1]
        )
    if "[" in left_of_param:
        configChoices = hjson.loads(
            left_of_param[left_of_param.index("[") : left_of_param.index("]") + 1]
        )
    return (configObject, configChoices)


class ConvertColabMetadataCommand(VisitorBasedCodemodCommand):
    METADATA_DEPENDENCIES = (ParentNodeProvider,)

    # Add a description so that future codemodders can see what this does.
    DESCRIPTION: str = (
        "Converts colab metadata into something that can be used for execution."
    )

    @staticmethod
    def add_args(arg_parser: argparse.ArgumentParser) -> None:
        # Add command-line args that a user can specify for running this
        # codemod.
        ConvertColabMetadataCommand.arg_parser = arg_parser

    def __init__(self, context: CodemodContext, gather=False, **params) -> None:
        # Initialize the base class with context, and save our args. Remember, the
        # "dest" for each argument we added above must match a parameter name in
        # this init.
        super().__init__(context)
        self.gather = gather
        self.params = params

    def leave_Assign(
        self,
        orig_node: cst.Assign,
        updated_node: cst.Assign,
    ) -> Union[cst.SimpleString, cst.Name]:
        configVariableNameNode = updated_node.targets[0].target
        if not hasattr(configVariableNameNode, "value"):
            return updated_node
        configVariableName = configVariableNameNode.value
        parent_node = self.get_metadata(ParentNodeProvider, orig_node)
        # now we are rewriting the assignment values
        if configVariableName in self.params and "@param" in cst.parse_module(
            ""
        ).code_for_node(parent_node):
            # user is trying to pass us this config, so use it
            return updated_node.with_changes(
                value=cst.parse_expression(repr(self.params[configVariableName])),
            )

        return updated_node

    def visit_Comment(
        self,
        node: cst.Comment,
    ) -> Union[cst.SimpleString, cst.Name]:
        if "@param" in node.value:
            parent_node = self.get_metadata(
                ParentNodeProvider,
                self.get_metadata(ParentNodeProvider, node),
            )

            if not hasattr(parent_node, "body"):
                return node
            assignmentNode = parent_node.body[0]
            configVariableName = assignmentNode.targets[0].target.value
            configDefaultNode = assignmentNode.value
            configDefaultValue = cst.parse_module("").code_for_node(configDefaultNode)
            configMetadata = node.value
            parsedParamConfigObject, parsedParamConfigChoices = parse_colab_form_param(
                configMetadata
            )

            # TODO: need better way to clean help message values
            cleanedConfigMetadata = re.sub(r"[^a-zA-Z0-9]", " ", configMetadata)
            cleanedConfigDefaultValue = re.sub(r"[^a-zA-Z0-9]", " ", configDefaultValue)

            if self.gather:
                # we are gathering the params for the argument parser
                configType = None
                if parsedParamConfigObject and "type" in parsedParamConfigObject:
                    configTypeName = parsedParamConfigObject["type"]
                    configType = {
                        "string": str,
                        "boolean": bool,
                        "raw": lambda s: literal_eval(s),
                        "date": lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
                        "number": float,
                        "integer": int,
                        "slider": int,
                    }[configTypeName]

                try:
                    # TODO: when assignment target is a tuple add arguments individually
                    ConvertColabMetadataCommand.arg_parser.add_argument(
                        "--" + configVariableName,
                        dest=configVariableName,
                        default=literal_eval(configDefaultValue),
                        help=f"{cleanedConfigMetadata} ({cleanedConfigDefaultValue})",
                        type=configType,
                        choices=parsedParamConfigChoices,
                        required=False,
                    )
                except:
                    print("exception constructing arguments")
        else:
            pass
