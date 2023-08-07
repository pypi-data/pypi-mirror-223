# FletBox, written in 08/03/2023 to 08/05/2023
# typing decorators is extremely confusing so decorators are not type hinted in this project

import time

start_total = time.time()

from typing import (
    Callable,
)

from types import (
    ModuleType,
)

import functools
from contextlib import contextmanager

from easydict import EasyDict as edict

import flet as ft

from rich import print

import inspect

class Builder():

    all_elements, filtered_elements = [], []

    # filter elements with nonstandard controls inputs
    @staticmethod
    def get_controls_from_module(m: ModuleType) -> (list, list):
        all_elements, filtered_elements = [], []
        for name, cls in vars(m).items():
            if inspect.isclass(cls):
                if issubclass(cls, ft.Control):
                    all_elements.append(cls)
                    if len([*set(dir(cls)).intersection(["controls", "actions", "content"])]) >= 1:
                        filtered_elements.append(cls)
        return all_elements, filtered_elements

    modules = [ft]
    for m in modules:
        tup = get_controls_from_module(m)
        all_elements += tup[0]
        filtered_elements += tup[1]

    #layout/items/extra distinction no longer neccessary due to smart pattern matching of controls/actions/content kwargs
    def __init__(self, extra_layout_elements:list=[], extra_items_elements:list=[]) -> None:
        class _attribs: pass
        self.layout = _attribs()

        self.root = ft.View()
        self.current = self.root

        def layout(self, func: Callable):
            @functools.wraps(func)
            @contextmanager
            def context_manager(*args, **kwargs):
                old_current = self.current
                if hasattr(self.current, "controls"):
                    self.current.controls.append(func(*args, **kwargs))
                    self.current = self.current.controls[-1]
                elif hasattr(self.current, "actions"):
                    self.current.actions.append(func(*args, **kwargs))
                    self.current = self.current.actions[-1]
                elif hasattr(self.current, "content"):
                    self.current.content = func(*args, **kwargs)
                    self.current = self.current.content
                yield self.current
                self.current = old_current
            return context_manager

        def items(self, func:Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if hasattr(self.current, "controls"):
                    self.current.controls.append(func(*args, **kwargs))
                    return self.current.controls[-1]
                elif hasattr(self.current, "actions"):
                    self.current.actions.append(func(*args, **kwargs))
                    return self.current.actions[-1]
                elif hasattr(self.current, "content"):
                    self.current.content = func(*args, **kwargs)
                    return self.current.content
            return wrapper

        #create layout elements
        for element in self.filtered_elements + extra_layout_elements:
            self.layout.__setattr__(element.__name__, layout(self, element))

        #create items elements
        for element in self.all_elements + extra_items_elements:
            setattr(self, element.__name__, items(self, element))

    def modules(self):
        return self, self.layout

class Factory():
    def __init__(self) -> None:
        self.name_index = {}
        self.extra_layout_elements = []
        self.extra_items_elements = []
        self.get_controls_from_module = Builder.get_controls_from_module

    def Builder(self) -> Builder:
        return Builder(extra_layout_elements=self.extra_layout_elements, extra_items_elements=self.extra_items_elements)

    def set_controls_from_module(self, m) -> None:
        tup = self.get_controls_from_module(m)
        for cls in tup[0]:
            cname = f"{m.__name__}.{cls.__name__}"
            for orig_cls in self.extra_items_elements:
                if cls.__name__ == orig_cls.__name__:
                    if orig_cls in self.extra_layout_elements:
                        print(f"[bold red]WARNING[/bold red] {cname} overwrote {orig_cls.__name__} in \[extra_items_elements & extra_layout_elements]")
                    else:
                        print(f"[bold red]WARNING[/bold red] {cname} overwrote {orig_cls.__name__} in \[extra_items_elements]")
        self.extra_items_elements += tup[0]
        self.extra_layout_elements += tup[1]

class FletBox():
    @staticmethod
    def stub(page: ft.Page) -> None:
        pass

    def __init__(self, factory:Factory=Factory(), verbose:bool=True, target:Callable=stub, view:ft.AppView=ft.AppView.WEB_BROWSER, web_renderer:ft.WebRenderer=ft.WebRenderer.HTML, port:int=8550, **kwargs) -> None:
        #fletbox values
        self.factory = factory
        self.verbose = verbose
        #flet values
        self.target = target
        self.kwargs = edict({**kwargs})
        self.kwargs.update({"view": view, "web_renderer": web_renderer, "port": port})
        #internal values
        self.funcs = {}

    def app(self, target:Callable=stub, **kwargs) -> None:
        #target again
        self.target = target
        #merge app kwargs with init kwargs
        self.kwargs = {**kwargs, **self.kwargs}
        #repopulate funcs via wrappers
        for wrapper in self.funcs.values(): wrapper()

        def wrapped_target(page: ft.Page):
            #routing functions
            def route_change(e: ft.RouteChangeEvent):
                start = time.time()
                page.views.clear()
                page.views.append(self.funcs[e.route](page))
                page.go(e.route)
                end = time.time()
                if self.verbose: print(f"{page.client_ip} connected to route {e.route} in {round(end - start, 8)}")
            def view_pop(view):
                page.views.pop()
                top_view = page.views[-1]
                page.go(top_view.route)

            #run provided target
            self.target(page)

            #routing
            page.on_route_change = route_change
            page.on_view_pop = view_pop
            page.go(page.route)

        self.kwargs["target"] = wrapped_target

        end_total = time.time()
        if self.verbose: print(f"[bold green]SETUP[/bold green] completed in {round(end_total - start_total, 8)}")
        ft.app(**self.kwargs)

    #wrap method to provide builder, return ft.View
    @staticmethod
    def _view(path: str, factory: Factory):
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(page: ft.Page, *args, **kwargs):
                builder = factory.Builder()
                ret = func(*args, page=page, builder=builder, **kwargs); builder = ret if isinstance(ret, Builder) else builder
                return ft.View(path, controls=builder.root.controls)
            return wrapper
        return decorator

    #replace method with function creator, initial update with wrapper
    def view(self, path: str):
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                self.funcs.update({path: self._view(path, self.factory)(func)})
            self.funcs.update({path: wrapper})
            return wrapper
        return decorator
