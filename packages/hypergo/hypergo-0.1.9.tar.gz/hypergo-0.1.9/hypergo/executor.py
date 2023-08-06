import importlib
import inspect
import re
from typing import Any, Callable, Generator, List, Mapping, Optional, Set, cast

from hypergo.config import ConfigType
from hypergo.context import ContextType
from hypergo.message import MessageType
from hypergo.storage import Storage
from hypergo.transform import Transform
from hypergo.utility import Utility


class Executor:
    @staticmethod
    def func_spec(fn_name: str) -> Callable[..., Any]:
        tokens: List[str] = fn_name.split(".")
        return cast(Callable[..., Any], (getattr(importlib.import_module(".".join(tokens[:-1])), tokens[-1])))

    @staticmethod
    def arg_spec(func: Callable[..., Any]) -> List[type]:
        params: Mapping[str, inspect.Parameter] = inspect.signature(func).parameters
        return [params[k].annotation for k in list(params.keys())]

    def __init__(self, config: ConfigType, storage: Optional[Storage] = None) -> None:
        self._config: ConfigType = config
        self._func_spec: Callable[..., Any] = Executor.func_spec(config["lib_func"])
        self._arg_spec: List[type] = Executor.arg_spec(self._func_spec)
        self._storage: Optional[Storage] = storage

    @property
    def storage(self) -> Optional[Storage]:
        return self._storage

    @property
    def config(self) -> ConfigType:
        return self._config

    def get_args(self, context: ContextType) -> List[Any]:
        def get_formatted_input_binding(input_binding: str, routing_key: str) -> str:
            formatted_input_binding: str = input_binding
            if "?" in input_binding:
                # Hypergo-209 if a component includes custom_properties key in the config, find the key
                # from custom_properties which is a subset of the routing key coming from the message
                # and use it to massage input_binding values containing ?
                input_message_routing_key_set: Set[str] = set(routing_key.split("."))
                for key in self._config.get("custom_properties", {}).keys():
                    key_set: Set[str] = set(key.split("."))
                    # key is a proper subset of the
                    # input_message_routing_key_set
                    if key_set.intersection(input_message_routing_key_set) == key_set:
                        formatted_input_binding = input_binding.replace("?", key.replace(".", "\\."))
                        break
            return formatted_input_binding

        args: List[Any] = []
        input_message_routing_key: str = Utility.deep_get(context, "message.routingkey")
        input_bindings: List[str] = [
            get_formatted_input_binding(input_binding=input_binding, routing_key=input_message_routing_key)
            for input_binding in self._config["input_bindings"]
        ]
        for arg, argtype in zip(input_bindings, self._arg_spec):
            # determine if arg binding is a literal denoted by '<literal>'
            val: Any = ((match := re.match(r"'(.*)'", arg)) and match.group(1)) or Utility.deep_get(context, arg)

            if argtype == inspect.Parameter.empty:  # inspect._empty:
                args.append(val)
            else:
                args.append(Utility.safecast(argtype, val))

        return args

    def get_output_routing_key(self, input_message_routing_key: str) -> str:
        routing_key_set: Set[str] = set(input_message_routing_key.split("."))
        tokens: List[str] = []
        for input_key in self._config["input_keys"]:
            # hypergo-144 dynamic routing key only for generic components
            # output key will contain context derived from the previous
            # producer routing key
            input_key_set: Set[str] = set(input_key.split("."))
            intersection_set: Set[str] = routing_key_set.intersection(input_key_set)
            # check if the routing key is in the input_key
            if intersection_set == input_key_set:
                # set difference operation to remove the subset of the routing key captured by the component
                # from its input_key and append it to tokens
                tokens.append(".".join(routing_key_set.difference(intersection_set)))
        token: str = self.organize_tokens(tokens)
        output_tokens: List[str] = [
            re.sub(r"(?<=\.)\?(?=\.)|^\?|(?<=\.)\?$|^\?$", token, output_key)
            for output_key in self._config["output_keys"]
        ]
        return self.organize_tokens(output_tokens)

    @Transform.pass_by_reference
    @Transform.compression("body")
    @Transform.serialization
    def execute(self, input_message: MessageType) -> Generator[MessageType, None, None]:
        context: ContextType = {"message": input_message, "config": self._config}
        if self._storage:
            context["storage"] = self._storage.use_sub_path(f"component/private/{self._config['name']}")
        args: List[Any] = self.get_args(context)
        execution: Any = self._func_spec(*args)
        output_routing_key: str = self.get_output_routing_key(input_message["routingkey"])
        return_values: List[Any] = list(execution) if inspect.isgenerator(execution) else [execution]
        for return_value in return_values:
            output_message: MessageType = {"routingkey": output_routing_key, "body": {}}
            output_context: ContextType = {"message": output_message, "config": self._config}

            def handle_tuple(dst: ContextType, src: Any) -> None:
                for binding, tuple_elem in zip(self._config["output_bindings"], src):
                    Utility.deep_set(dst, binding, tuple_elem)

            def handle_default(dst: ContextType, src: Any) -> None:
                for binding in self._config["output_bindings"]:
                    Utility.deep_set(dst, binding, src)

            if isinstance(return_value, tuple):
                handle_tuple(output_context, return_value)
            else:
                handle_default(output_context, return_value)

            yield output_message

    def organize_tokens(self, keys: List[str]) -> str:
        return ".".join(sorted(set(".".join(keys).split("."))))
