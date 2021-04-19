#include "Python.h"
#include <ctype.h>
#include <string.h>
#include <windows.h>

static PyObject* python_ext_hello(PyObject* self, PyObject* args) {
    return Py_BuildValue("s", "Hello World! from python_ext");
}

static PyMethodDef defs[] = {
{"hello", python_ext_hello, METH_VARARGS},
{NULL, NULL}
};

__declspec(dllexport) void APIENTRY initpython_ext(void) {
    Py_InitModule("python_ext", defs);
}