"""The code for the Agenta SDK"""
import argparse
import functools
import inspect
import os
import sys
import traceback
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Callable, Optional

from fastapi import Depends, FastAPI, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .context import get_contexts, save_context
from .types import FloatParam, InFile, TextParam, Context, MultipleChoiceParam
from .router import router as router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://0.0.0.0:3000",
    "http://0.0.0.0:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix='')


def ingest_file(upfile: UploadFile):
    temp_file = NamedTemporaryFile(delete=False)
    temp_file.write(upfile.file.read())
    temp_file.close()
    return InFile(file_name=upfile.filename,
                  file_path=temp_file.name)


def ingest(func: Callable[..., Any]):
    sig = inspect.signature(func)
    func_params = sig.parameters

    # find the optional parameters for the app
    app_params = {name: param for name, param in func_params.items()
                  if param.annotation in {TextParam, FloatParam}}
    # find the default values for the optional parameters
    for name, param in app_params.items():
        default_value = param.default if param.default is not param.empty else None
        app_params[name] = default_value

    ingestible_files = {name: param for name, param in func_params.items()
                        if param.annotation is InFile}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for name in ingestible_files:
            if name in kwargs and kwargs[name] is not None:
                kwargs[name] = ingest_file(kwargs[name])
        try:
            return func(*args, **kwargs)
        except Exception as e:
            traceback_str = ''.join(traceback.format_exception(None, e, e.__traceback__))
            return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback_str})

    new_params = []
    for name, param in sig.parameters.items():
        if name in app_params:
            new_params.append(
                inspect.Parameter(
                    name,
                    inspect.Parameter.KEYWORD_ONLY,
                    default=Body(app_params[name]),
                    annotation=Optional[param.annotation]

                )
            )
        elif name in ingestible_files:
            new_params.append(
                inspect.Parameter(
                    name,
                    param.kind,
                    annotation=UploadFile
                )
            )
        else:
            new_params.append(
                inspect.Parameter(
                    name,
                    inspect.Parameter.KEYWORD_ONLY,
                    default=Body(...),
                    annotation=param.annotation
                )
            )

    wrapper.__signature__ = sig.replace(parameters=new_params)

    route = "/ingest"
    app.post(route)(wrapper)

    # check if the module is being run as the main script
    if os.path.splitext(os.path.basename(sys.argv[0]))[0] == os.path.splitext(os.path.basename(inspect.getfile(func)))[0]:
        parser = argparse.ArgumentParser()
        # add arguments to the command-line parser
        for name, param in sig.parameters.items():
            if name in app_params:
                # For optional parameters, we add them as options
                parser.add_argument(f"--{name}", type=type(param.default),
                                    default=param.default)
            elif name in ingestible_files:
                parser.add_argument(name, type=str)
            else:
                # For required parameters, we add them as arguments
                parser.add_argument(name, type=param.annotation)

        args = parser.parse_args()
        args_dict = vars(args)
        for name in ingestible_files:
            args_dict[name] = InFile(file_name=Path(args_dict[name]).stem,
                                     file_path=args_dict[name])
        print(func(**vars(args)))

    return wrapper


def post(func: Callable[..., Any]):
    sig = inspect.signature(func)
    func_params = sig.parameters

    # find the optional parameters for the app
    app_params = {
        name: param
        for name, param in func_params.items()
        if param.annotation in {TextParam, FloatParam, MultipleChoiceParam}
    }

    # find the default values for the optional parameters
    for name, param in app_params.items():
        default_value = (
            param.default if param.default is not param.empty else None
        )
        app_params[name] = default_value

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        kwargs = {**app_params, **kwargs}
        try:
            result = func(*args, **kwargs)
            if isinstance(result, Context):
                save_context(result)
            return result
        except Exception as e:
            if sys.version_info.major == 3 and sys.version_info.minor < 10:
                traceback_str = "".join(
                    traceback.format_exception(None, e, e.__traceback__)
                )
            else:
                traceback_str = "".join(
                    traceback.format_exception(e, value=e, tb=e.__traceback__)
                )
            return JSONResponse(
                status_code=500,
                content={"error": str(e), "traceback": traceback_str},
            )

    new_params = []
    instances_to_override = []
    for name, param in sig.parameters.items():
        if name in app_params:
            if param.annotation is MultipleChoiceParam:
                # we save the MultipleChoiceParams for later to update the openai schema
                instances_to_override.append((name, app_params[name]))
                new_params.append(
                    inspect.Parameter(
                        name,
                        inspect.Parameter.KEYWORD_ONLY,
                        default=Body(app_params[name]),
                        annotation=Optional[param.annotation],
                    )
                )
            else:
                new_params.append(
                    inspect.Parameter(
                        name,
                        inspect.Parameter.KEYWORD_ONLY,
                        default=Body(app_params[name]),
                        annotation=Optional[param.annotation],
                    )
                )
        else:
            new_params.append(
                inspect.Parameter(
                    name,
                    inspect.Parameter.KEYWORD_ONLY,
                    default=Body(...),
                    annotation=param.annotation,
                )
            )

    wrapper.__signature__ = sig.replace(parameters=new_params)

    route = "/generate"
    func_name = func.__name__
    app.post(route)(wrapper)
    schema = app.openapi()  # or app.openapi_schema
    schemas = schema["components"]["schemas"][f"Body_{func_name}_generate_post"]["properties"]

    # Update schema for multichoice objects
    override_schema_for_multichoice(schemas, instances_to_override)

    # check if the module is being run as the main script
    if (
        os.path.splitext(os.path.basename(sys.argv[0]))[0]
        == os.path.splitext(os.path.basename(inspect.getfile(func)))[0]
    ):
        parser = argparse.ArgumentParser()
        # add arguments to the command-line parser
        for name, param in sig.parameters.items():
            if name in app_params:
                if param.annotation is MultipleChoiceParam:
                    parser.add_argument(
                        f"--{name}",
                        type=str,
                        default=param.default,
                        choices=param.default.choices
                    )
                else:
                    parser.add_argument(
                        f"--{name}",
                        type=type(param.default),
                        default=param.default,
                    )
            else:
                # For required parameters, we add them as arguments
                parser.add_argument(name, type=param.annotation)

        args = parser.parse_args()
        print(func(**vars(args)))

    return wrapper


def override_schema_for_multichoice(
        parameters: dict, instances_to_override: list):
    """
    This function updates the "enum" and "default" values of each MultiChoiceParam instance in the dictionary based 
    on its choices and default value. If the default value is not present in the choices, it adds the default 
    value to the beginning of the choices list and sets it as the new default value. 

    This ensures that the generated API documentation reflects the available choices and default values for 
    MultiChoiceParam instances.

    Arguments:
        parameters -- A dictionary containing parameter schema. Keys are parameter names, values hold parameter details.
        instances_to_override -- A list of tuples each containing a parameter name (param_name) and its instance
        (param_instance).
    """

    for param_name, param_instance in instances_to_override:
        for _, value in parameters.items():
            value_title_lower = str(value.get("title")).lower()
            value_title = (
                "_".join(value_title_lower.split())
                if len(value_title_lower.split()) >= 2
                else value_title_lower
            )

            if (
                isinstance(value, dict)
                and value.get("x-parameter") == "choice"
                and value_title == param_name
            ):
                default = str(param_instance)
                param_choices = param_instance.choices
                choices = [default] + param_choices if default not in param_choices else param_choices

                value["enum"] = choices
                value["default"] = (
                    default if default in choices else choices[0]
                )
