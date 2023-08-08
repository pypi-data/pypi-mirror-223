'''
Simple subclass wrapper around `threading.Thread` to get the return value
from a thread in python. Exact same interface as `threading.Thread`!

'''

# MIT License
#
# Copyright (c) 2023 Shail Shouryya
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import sys
import time
import threading
from datetime import datetime


__version__              = '0.1.1.post1'


_general_documentation = '''
    The `threading.Thread` subclass `ThreadWithResult` saves the result of a thread
    as its `result` attribute - i.e. call `thread_with_result_instance_1.result`
    after `thread_with_result_instance_1` finishes running to get the return
    value from the function that ran on that thread:

    >>> thread = ThreadWithResult(
        target = my_function,
        args   = (my_function_arg1, my_function_arg2, ...)
        kwargs = {my_function_kwarg1: kwarg1_value, my_function_kwarg2: kwarg2_value, ...}
    )
    >>> thread.start()
    >>> thread.join()
    >>> thread.result # returns value returned from function passed in to the `target` argument!




    NOTE: As of Release 0.0.3, you can also specify values for
    the `group`, `name`, and `daemon` arguments if you want to
    set those values manually.

    For details about the interface features available from `threading.Thread`,
    see documentation under "Method resolution order" - accessible
    from the python interpreter with:
    help(ThreadWithResult)




    OVERVIEW:
    `ThreadWithResult` is a `threading.Thread` subclass used to save the
    result of a function called through the threading interface, since

    >>> thread = threading.Thread(
        target = my_function,
        args   = (my_function_arg1, my_function_arg2, ...)
        kwargs = {my_function_kwarg1: kwarg1_value, my_function_kwarg2: kwarg2_value, ...}
    )
    >>> thread.start()
    >>> thread.join()
    >>> thread.result # does not work!

    executes and returns immediately after the thread finishes,
    WITHOUT providing any way to get the return value
    from the function that ran on that thread.




    USAGE:
    The name of the function to run on a separate thread should
    be passed to `ThreadWithResult` through the `target` argument,
    and any arguments for the function should be passed in
    through the `args` and `kwargs` arguments.

    You can also specify `threading.Thread` attributes such as
    `group`, `name`, and `daemon` by passing in the value you want to
    set them to as keyword arguments to `ThreadWithResult`




    NOTE that with release 0.0.7, you can also specify if
    you want the `ThreadWithResult` instance to log when the
    thread starts, ends, and how long the thread takes to execute!


    If you want to mute logging this message to the terminal for all
    `ThreadWithResult` instances, set the
    `log_thread_status` class attribute to False:

    >>> ThreadWithResult.log_thread_status = False


    If you only want to mute logging this message to the terminal for
    a specific instance of `ThreadWithResult`, set the
    `log_thread_status` attribute for the specific instance to False:

    >>> thread_with_result_instance.log_thread_status = False

    ------------------------------------------------------------------------------
    | Keep in mind python prioritizes the `log_thread_status` instance attribute |
    | over the `log_thread_status` class attribute!                              |
    ------------------------------------------------------------------------------



    If you want to log this message to an output file (or multiple output files)
    for all `ThreadWithResult` instances, set the
    `log_files` class attribute to an iterable object contatining
    objects that support the .write() method:

    >>> ThreadWithResult.log_files = [file_object_1, file_object_2]


    If you only want to log this message to an output file (or multiple output files)
    for a specific instance of `ThreadWithResult`, set the
    `log_files` attribute for the specific instance to an iterable
    object contatining objects that support the .write() method:

    >>> thread_with_result_instance.log_files = [file_object_1, file_object_2]

    ----------------------------------------------------------------------
    | Keep in mind python prioritizes the `log_files` instance attribute |
    | over the `log_files` class attribute!                              |
    ----------------------------------------------------------------------



    NOTE: since python prioritizes instance attributes over class attributes,
    if both the instance attribute and class attribute are set to different values,
    python uses the value set for the instance attribute.
    For more information, look up:
      - class attributes vs instance attributes in python
      - scope resolution using the LEGB rule for python

    Also note, by default the `log_thread_status`
    class attribute is set to `True`, and the `log_files`
    class attribute set to `None` - neither attributes
    exist as instance attributes by default!

    '''




class _runOverrideThreadWithResult(threading.Thread):
    __doc__ = _general_documentation

    log_thread_status = True
    log_files         = None

    def run(self):
        '''
        Method representing the thread's activity that is overriden to
        save the result of a thread (if the thread completes) in the
        `result` attribute of the instance.

        This is the only change to the functionality of the `run` method.
        This method still invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the `args` and `kwargs` arguments, respectively.
        '''
        # uses the try/finally blocks for consistency with the CPython implementation:
        # https://github.com/python/cpython/blob/89ac665891dec1988bedec2ce9b2c4d016502a49/Lib/threading.py#L987
        log_condition = self.log_thread_status is True or self.log_files is not None
        try:
            if self._target is not None:
                if log_condition: time_time_start, perf_counter_start = _log_start_of_thread(self)
                self.result                                           = self._target(*self._args, **self._kwargs)
                if log_condition: _                                   = _log_end_of_thread(self, time_time_start, perf_counter_start)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs





class ___init__OverrideThreadWithResult(threading.Thread):
    __doc__ = _general_documentation

    log_thread_status = True
    log_files         = None

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        '''
        IMPLEMENTATION EXPLANATION:
        We create a closure function inside the __init__ method to run the
        actual function we want to run on a separate thread, enclose the function passed to
        `target` - along with the arguments provided to `args` and `kwargs` -
        inside the closure function, and pass the CLOSURE FUNCTION
        as the function to the `target` argument in the
        `super.__init__()` call to `threading.Thread`:
        super().__init__(group=group, target=closure_function, name=name, daemon=daemon)

        Since the function we want to run on a separate thread is no longer
        the function passed directly to `threading.Thread` (remember,
        we pass the closure function instead!), we save the result of
        the enclosed function to the `self.result` attribute of the
        instance.

        We use inheritance to initialize this instance with the
        closure function as the `target` function and no arguments
        for `args` or `kwargs` (since we pass
        the `args` and `kwargs` arguments to the original
        `target` function INSIDE the closure function).

        All other attributes (`group`, `name`, and `daemon`)
        are initialized in the parent `threading.Thread` class
        during the `super().__init__()` call.
        '''
        def closure_function():
            log_condition = self.log_thread_status is True or self.log_files is not None
            if log_condition: time_time_start, perf_counter_start = _log_start_of_thread(self)
            self.result                                           = target(*args, **kwargs)
            if log_condition: _                                   = _log_end_of_thread(self, time_time_start, perf_counter_start)
        if sys.version_info.major == 3 and sys.version_info.minor >= 10:
            # commit 98c16c991d6e70a48f4280a7cd464d807bdd9f2b in the cpython repository starts adding
            # the function name of the `target` argument to the thread name:
            #     *name* is the thread name. By default, a unique name is constructed
            #     of the form "Thread-*N*" where *N* is a small decimal number,
            #     or "Thread-*N* (target)" where "target" is ``target.__name__`` if the
            #     *target* argument is specified BUT the *name* argument is omitted.
            # HOWEVER, since we pass the
            # original `target` argument to the `closure_function` here and then pass `closure_function`
            # as the new `target` argument in the `super()` call, the thread name (as seen by the base
            # `threading.Thread` class) will ALWAYS be "closure_function" regardless of what function
            # is running inside `closure_function` - to make the name more helpful, we manually overwrite
            # the `closure_function.__name__` attribute here to include the original `target` function's name
            #   - see the following for more information:
            #     - https://github.com/python/cpython/issues/85999
            #     - https://github.com/python/cpython/issues/59705
            #     - https://github.com/python/cpython/issues/85905
            #     - https://github.com/python/cpython/pull/22357
            #     - https://github.com/python/cpython/issues/85999
            #     - https://bugs.python.org/issue41833
            if name is None and target is not None:
                closure_function.__name__ = self.__class__.__name__ + '.' + 'closure_function' + '(' + str(target.__name__) + ')'
        super().__init__(group=group, target=closure_function, name=name, daemon=daemon)


def _log_start_of_thread(thread_with_result_instance):
    time_time_start, perf_counter_start = _measure_time()
    thread_name                         = format_thread_name()
    formatted_datetime_with_offset      = format_datetime_for_message()
    message                             = formatted_datetime_with_offset + thread_name + ' Starting thread...'
    _log(thread_with_result_instance, message)
    return time_time_start, perf_counter_start

def _log_end_of_thread(thread_with_result_instance, time_time_start, perf_counter_start):
    time_time_end, perf_counter_end     = _measure_time()
    thread_name                         = format_thread_name()
    formatted_time_time                 = str(time_time_end - time_time_start) + ' time.time() seconds'
    formatted_time_perf_counter         = _format_perf_counter_info(perf_counter_start, perf_counter_end)
    formatted_datetime_with_offset      = format_datetime_for_message()
    message                             = formatted_datetime_with_offset + thread_name + ' Finished thread! This thread took ' + formatted_time_time + formatted_time_perf_counter + ' to complete.'
    _log(thread_with_result_instance, message)

def _measure_time():
    current_time         = time.time()
    current_perf_counter = _time_perf_counter()
    return current_time, current_perf_counter

# use helper function to check if time.perf_counter() can be called since function became available only after python release 3.3
def _time_perf_counter():
    if sys.version_info.major == 3 and sys.version_info.minor >= 3:
        return time.perf_counter()
    return None

def _format_perf_counter_info(perf_counter_start, perf_counter_end):
    if sys.version_info.major == 3 and sys.version_info.minor >= 3:
        return ' (' + str(perf_counter_end - perf_counter_start) + ' time.perf_counter() seconds)'
    return ''

def format_thread_name():
    thread_name        = '[' + threading.current_thread().name + ']'
    return thread_name.rjust(12)

def format_datetime_for_message():
    utc_offset                     = time.strftime('%z')
    formatted_datetime_with_offset = datetime.now().isoformat() + utc_offset + ' '
    return formatted_datetime_with_offset



def _log(thread_with_result_instance, message):
    '''
    Helper function to print when the thread
    starts, ends, and how long the thread takes to execute.

    This function runs and prints the thread information to the
    terminal when any of the following statements are true:
        * the instance attribute `log_thread_status` is `True`
        * the instance attribute `log_thread_status` is unset but
            the class attribute `log_thread_status` is `True`
        * the instance attribute `log_files` is
        an iterable object containing objects that support the .write() method
        * the instance attribute `log_files` is unset but
            the class attribute is an iterable object containing objects that support the .write() method

    This function also logs the information to every location in
    `log_files` in addition to printing the thread information
    to the terminal if the instance or class attribute `log_files` is an
    iterable object containing objects that support the .write() method.
    '''
    if thread_with_result_instance.log_files is not None:
        try:
            for file in thread_with_result_instance.log_files:
                try:
                    file.write(message + '\n')
                except AttributeError as error_message:
                    # example exception:
                    # AttributeError: 'str' object has no attribute 'write'
                    print('ERROR! Could not write to ' + str(file) + '. Please make sure that every object in ' + str(thread_with_result_instance.log_files) + ' supports the .write() method. The exact error was:\n' + str(error_message))
        except TypeError as error_message:
            # example exception:
            # TypeError: 'int' object is not iterable
            print('ERROR! Could not write to ' + str(thread_with_result_instance.log_files) + '. Please make sure that the log_files attribute for ' + str(thread_with_result_instance.__class__.name) + ' is an iterable object containing objects that support the .write() method. The exact error was:\n' + str(error_message))
    if thread_with_result_instance.log_thread_status is True:
        print(message)






ThreadWithResult = _runOverrideThreadWithResult

# without the `_runOverrideThreadWithResult` assignment to `ThreadWithResult`:
#   any existing code already using this module trying to use the new changes in release 0.1.1
#   would require updating all references to `ThreadWithResult` to either
#   `_runOverrideThreadWithResult` or `___init__OverrideThreadWithResult`
# binding `ThreadWithResult` to `_runOverrideThreadWithResult` avoids this problem
# `ThreadWithResult` can also be bound to `___init__OverrideThreadWithResult` but
#    `_runOverrideThreadWithResult` is the chosen default since
#    the threading.Thread class does additional work in the __init__ method,
#    such as attribute modifications (https://github.com/python/cpython/blob/89ac665891dec1988bedec2ce9b2c4d016502a49/Lib/threading.py#L892)
#    and private attribute additions (https://github.com/python/cpython/blob/89ac665891dec1988bedec2ce9b2c4d016502a49/Lib/threading.py#L905)
#    that `___init__OverrideThreadWithResult` does not currently do, and therefore
#    using `___init__OverrideThreadWithResult` might cause difficult-to-debug bugs
