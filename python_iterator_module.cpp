
// Compiled by "python setup.py build_ext --inplace"

// Allows us to support python 3.6+. No sense going older than 3.6.
#define Py_LIMITED_API 0x03060000


#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <iostream>


static PyObject*
python_iterator_module_yield_items(PyObject *self, PyObject *args) {

    std::cout << "Hello World using std::cout " << std::endl;

    /* We wish for our function to return None, the Python
    equivalent of returning void. We have to do the following
    to return None. */

    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef python_iterator_moduleMethods[] = {
    {"yield_items", python_iterator_module_yield_items, METH_VARARGS, "Print Hello World"},
    {NULL, NULL, 0, NULL} /* The sentinel value. */
};

static struct PyModuleDef python_iterator_modulemodule = {

    PyModuleDef_HEAD_INIT,
    "python_iterator_module",
    NULL, /*This is for documentation, which we won't use; so it is NULL. */
    -1,
    python_iterator_moduleMethods
};



PyMODINIT_FUNC
PyInit_python_iterator_module(void) {
    return PyModule_Create(&python_iterator_modulemodule);
}



